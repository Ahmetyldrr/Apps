import glob
import PyPDF2
import pandas as pd

# PDF dosyasını bul
pdf_files = glob.glob('*.pdf')
print("Bulunan PDF dosyaları:")
for i, pdf in enumerate(pdf_files):
    print(f"{i+1}. {pdf}")

# Montaj kitapçığını bul
montaj_pdf = None
for pdf in pdf_files:
    if any(word in pdf.upper() for word in ['MONTAJ', 'KİTAP', 'TEMEL']):
        montaj_pdf = pdf
        break

if not montaj_pdf and pdf_files:
    montaj_pdf = pdf_files[0]  # İlk PDF'i al

if montaj_pdf:
    print(f"\nSeçilen PDF: {montaj_pdf}")
    
    # PDF'den örnek metin çıkar
    try:
        with open(montaj_pdf, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            print(f"Toplam sayfa sayısı: {len(reader.pages)}")
            
            # İlk birkaç sayfadan örnek metinler
            for i in range(min(3, len(reader.pages))):
                print(f"\n=== SAYFA {i+1} ===")
                text = reader.pages[i].extract_text()
                print(text[:500])  # İlk 500 karakter
                print("...")
                
    except Exception as e:
        print(f"PDF okuma hatası: {e}")
else:
    print("PDF dosyası bulunamadı!")
