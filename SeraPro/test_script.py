print("Script başlıyor...")

import os
import sys

print(f"Python versiyon: {sys.version}")
print(f"Çalışma dizini: {os.getcwd()}")

# Dosya varlığını kontrol et
pdf_dosya = 'MONTAJ KİTAPÇIĞI-TEMEL.pdf'
if os.path.exists(pdf_dosya):
    print(f"✓ {pdf_dosya} dosyası bulundu")
    print(f"Dosya boyutu: {os.path.getsize(pdf_dosya)} byte")
else:
    print(f"✗ {pdf_dosya} dosyası bulunamadı")

# Modülleri test et
try:
    import PyPDF2
    print("✓ PyPDF2 modülü yüklendi")
except ImportError as e:
    print(f"✗ PyPDF2 hatası: {e}")

try:
    import pandas
    print("✓ pandas modülü yüklendi")
except ImportError as e:
    print(f"✗ pandas hatası: {e}")

try:
    import openpyxl
    print("✓ openpyxl modülü yüklendi")
except ImportError as e:
    print(f"✗ openpyxl hatası: {e}")

print("Test tamamlandı.")
