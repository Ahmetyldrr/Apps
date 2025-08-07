from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import pandas as pd
from .models import AnalysisReport
import os
from django.conf import settings

def analysis_list(request):
    # --- Otomatik Senkronizasyon Başlangıcı ---
    data_path = settings.MEDIA_ROOT
    if os.path.exists(data_path):
        # Veritabanındaki ve diskteki dosyaları karşılaştır
        db_files = set(AnalysisReport.objects.values_list('excel_file', flat=True))
        disk_files = set(f for f in os.listdir(data_path) if f.endswith(('.xlsx', '.xls')))

        # Yeni dosyaları veritabanına ekle
        new_files = disk_files - db_files
        for filename in new_files:
            report_title = os.path.splitext(filename)[0].replace('_', ' ').title()
            AnalysisReport.objects.create(title=report_title, excel_file=filename)

        # Silinmiş dosyaları veritabanından kaldır
        deleted_files = db_files - disk_files
        if deleted_files:
            AnalysisReport.objects.filter(excel_file__in=deleted_files).delete()
    # --- Otomatik Senkronizasyon Sonu ---

    # Veritabanındaki güncel raporları al
    reports = AnalysisReport.objects.all().order_by('title')
    analysis_data = []

    for report in reports:
        try:
            # pandas'ın dosyayı okuyabilmesi için tam yolunu kullan
            df = pd.read_excel(report.excel_file.path, nrows=1)
            if not df.empty:
                summary_row = df.iloc[0]
                analysis_data.append({
                    'report_obj': report,
                    'start_date': summary_row.get('Tarih', 'N/A').strftime('%Y-%m-%d') if pd.notna(summary_row.get('Tarih')) else 'N/A',
                    'initial_demand': summary_row.get('Talep_Miktari', 'N/A'),
                    'initial_stock': summary_row.get('Stok_Seviyesi', 'N/A')
                })
        except Exception as e:
            print(f"Dosya okunurken hata: {report.title}, Hata: {e}")
            # Hatalı dosyayı da listede göster ama özet bilgisi olmadan
            analysis_data.append({
                'report_obj': report,
                'start_date': 'Okunamadı',
                'initial_demand': 'Okunamadı',
                'initial_stock': 'Okunamadı'
            })
            
    context = {'analysis_data': analysis_data}
    return render(request, 'reports/analysis_list.html', context)

def download_analysis(request, pk):
    report = get_object_or_404(AnalysisReport, pk=pk)
    
    # Dosya yolunu al ve varlığını kontrol et
    file_path = report.excel_file.path
    if not os.path.exists(file_path):
        return HttpResponse("Dosya sunucuda bulunamadı.", status=404)

    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
        return response
