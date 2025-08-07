from django.shortcuts import render



from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

import os
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def detail(request):
    data_dir = os.path.join(settings.BASE_DIR, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage(location=data_dir)
        filename = fs.save(excel_file.name, excel_file)
    # Tüm dosyaları listele
    files = os.listdir(data_dir)
    file_urls = [
        {'name': f, 'url': f'/data/{f}'}
        for f in files
    ]
    return render(request, 'detail.html', {'file_urls': file_urls})



def contact(request):
    return render(request, 'contact.html')

def products(request):
    return render(request, 'products.html')



import os
import pandas as pd
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Kisi

def addData(request):
    message = ""
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'data'))
        filename = fs.save(excel_file.name, excel_file)
        file_path = os.path.join(settings.BASE_DIR, 'data', filename)
        try:
            df = pd.read_excel(file_path)
            for _, row in df.iterrows():
                idx = int(row['idx'])
                adi_soyadi = str(row['adi_soyadi'])
                Kisi.objects.update_or_create(
                    idx=idx,
                    defaults={'adi_soyadi': adi_soyadi}
                )
            message = "Veriler başarıyla eklendi veya güncellendi."
        except Exception as e:
            message = f"Hata: {e}"
    return render(request, 'addData.html', {'message': message})

def home(request):
    kisiler = Kisi.objects.all()[:10]
    kisiler = [kisi for kisi in kisiler if kisi.adi_soyadi]  # Boş isimleri filtrele
    if not kisiler:
        message = "Henüz kayıtlı kişi yok."
        return render(request, 'home.html', {'message': message})
    
    return render(request, 'home.html', {'kisiler': kisiler})