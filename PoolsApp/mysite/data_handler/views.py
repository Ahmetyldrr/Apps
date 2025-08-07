from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from polls.models import Question, Choice  # Assuming you have a 'polls' app with these models
import pandas as pd
import io

def upload_polls(request):
    if request.method == 'POST':
        if 'excel_file' not in request.FILES:
            messages.error(request, 'Lütfen bir dosya seçin.')
            return redirect('data_handler:upload_polls')

        excel_file = request.FILES['excel_file']
        if not excel_file.name.endswith(('.xls', '.xlsx')):
            messages.error(request, 'Geçersiz dosya formatı. Lütfen bir Excel dosyası yükleyin.')
            return redirect('data_handler:upload_polls')

        try:
            df = pd.read_excel(excel_file)

            if 'question_text' not in df.columns:
                messages.error(request, "Excel dosyasında 'question_text' sütunu bulunmalıdır.")
                return redirect('data_handler:upload_polls')

            choice_cols = [col for col in df.columns if col.startswith('choice')]
            if not choice_cols:
                messages.error(request, "Excel dosyasında 'choice' ile başlayan en az bir seçenek sütunu bulunmalıdır.")
                return redirect('data_handler:upload_polls')

            for index, row in df.iterrows():
                if pd.notna(row['question_text']):
                    question = Question.objects.create(
                        question_text=row['question_text'],
                        pub_date=timezone.now()
                    )
                    for col in choice_cols:
                        if pd.notna(row[col]):
                            Choice.objects.create(question=question, choice_text=row[col])
            
            messages.success(request, 'Anketler başarıyla yüklendi.')
        except Exception as e:
            messages.error(request, f'Dosya işlenirken bir hata oluştu: {e}')
        
        return redirect('data_handler:upload_polls')

    return render(request, 'data_handler/upload_page.html')

def download_template(request):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    
    df = pd.DataFrame({
        'question_text': ['Örnek Soru: En sevdiğiniz renk nedir?'],
        'choice1': ['Kırmızı'],
        'choice2': ['Mavi'],
        'choice3': ['Yeşil']
    })
    df.to_excel(writer, index=False, sheet_name='Polls')
    writer.close()
    output.seek(0)

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="polls_template.xlsx"'
    return response
