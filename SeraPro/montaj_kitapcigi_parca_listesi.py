import PyPDF2
import pandas as pd
import re
import os

# PDF ve Excel dosya adları
import glob
pdf_dosyalari = glob.glob('*.pdf')
dosya_pdf = None
for pdf in pdf_dosyalari:
    if 'MONTAJ' in pdf.upper() or 'KİTAP' in pdf.upper() or 'TEMEL' in pdf.upper():
        dosya_pdf = pdf
        break

if not dosya_pdf:
    # Fallback - ilk PDF dosyasını al
    dosya_pdf = pdf_dosyalari[0] if pdf_dosyalari else 'MONTAJ KİTAPÇIĞI-TEMEL.pdf'

dosya_excel = 'Montaj_Kitapcigi_Parca_Listesi.xlsx'

def pdf_metin_cikart(pdf_yolu):
    """PDF'den tüm sayfaların metnini çıkarır"""
    try:
        with open(pdf_yolu, 'rb') as dosya:
            reader = PyPDF2.PdfReader(dosya)
            tum_metinler = []
            
            print(f"Toplam sayfa sayısı: {len(reader.pages)}")
            
            for sayfa_no, sayfa in enumerate(reader.pages, 1):
                try:
                    metin = sayfa.extract_text()
                    if metin.strip():  # Boş olmayan metinler
                        tum_metinler.append({
                            'Sayfa_No': sayfa_no,
                            'Metin': metin.strip()
                        })
                        print(f"Sayfa {sayfa_no} işlendi")
                    else:
                        print(f"Sayfa {sayfa_no} boş")
                except Exception as e:
                    print(f"Sayfa {sayfa_no} işlenirken hata: {e}")
                    continue
                    
            return tum_metinler
    except Exception as e:
        print(f"PDF okuma hatası: {e}")
        return []

def parca_bul_ve_ayir(metin):
    """Metinden parça listelerini ve bölümleri ayırır"""
    parcalar = []
    
    # Farklı parça formatlarını tanımlama desenleri
    desenler = [
        r'(\d+)\s*[.)\-]\s*([A-ZÜĞŞÇÖI][a-züğşçöıA-ZÜĞŞÇÖI\s\d\-\(\)]+)',  # Numaralı listeler
        r'([A-ZÜĞŞÇÖI][a-züğşçöıA-ZÜĞŞÇÖI\s\d\-\(\)]{10,})',  # Uzun parça adları
        r'(PARÇA|PARCA|MALZEME|ELEMAN)[\s:]*([A-ZÜĞŞÇÖI][a-züğşçöıA-ZÜĞŞÇÖI\s\d\-\(\)]+)',  # Parça etiketli
    ]
    
    for desen in desenler:
        eslesme = re.findall(desen, metin, re.MULTILINE | re.IGNORECASE)
        for eslesen in eslesme:
            if len(eslesen) == 2:  # Tuple ise
                parcalar.append({
                    'Sira_No': eslesen[0] if eslesen[0].isdigit() else '',
                    'Parca_Adi': eslesen[1].strip()
                })
            else:  # Tek string ise
                parcalar.append({
                    'Sira_No': '',
                    'Parca_Adi': eslesen.strip()
                })
    
    return parcalar

def bolum_belirle(metin):
    """Metinden bölüm adını belirlemeye çalışır"""
    bolum_desenleri = [
        r'(BÖLÜM|BOLUM|CHAPTER|SECTION)\s*(\d+)',
        r'(\d+)\.\s*(BÖLÜM|BOLUM)',
        r'([A-ZÜĞŞÇÖI\s]{5,})(?=\n|\r)',  # Büyük harfli başlıklar
    ]
    
    for desen in bolum_desenleri:
        eslesen = re.search(desen, metin[:200], re.IGNORECASE)  # İlk 200 karakter
        if eslesen:
            return eslesen.group().strip()
    
    return "Belirsiz Bölüm"

def main():
    print("PDF'den parça listesi çıkarma işlemi başlıyor...")
    
    print(f"Hedef PDF dosyası: {dosya_pdf}")
    
    if not dosya_pdf or not os.path.exists(dosya_pdf):
        print(f"HATA: PDF dosyası bulunamadı!")
        print("Klasördeki PDF dosyaları:")
        for pdf in glob.glob('*.pdf'):
            print(f"  - {pdf}")
        return
    
    # PDF'den metin çıkarma
    sayfa_metinleri = pdf_metin_cikart(dosya_pdf)
    
    if not sayfa_metinleri:
        print("PDF'den metin çıkarılamadı!")
        return
    
    # Tüm parçaları toplama
    tum_parcalar = []
    
    for sayfa in sayfa_metinleri:
        sayfa_no = sayfa['Sayfa_No']
        metin = sayfa['Metin']
        
        # Bölüm belirleme
        bolum = bolum_belirle(metin)
        
        # Parçaları bulma
        parcalar = parca_bul_ve_ayir(metin)
        
        for parca in parcalar:
            tum_parcalar.append({
                'Sayfa_No': sayfa_no,
                'Bolum': bolum,
                'Sira_No': parca['Sira_No'],
                'Parca_Adi': parca['Parca_Adi'],
                'Tam_Metin': metin[:500] + "..." if len(metin) > 500 else metin  # İlk 500 karakter
            })
    
    # Excel'e yazma
    if tum_parcalar:
        df = pd.DataFrame(tum_parcalar)
        
        # Excel dosyasını oluşturma
        with pd.ExcelWriter(dosya_excel, engine='openpyxl') as writer:
            # Ana sayfa - tüm parçalar
            df.to_excel(writer, sheet_name='Tum_Parcalar', index=False)
            
            # Sayfa bazında ayrım
            for sayfa_no in sorted(df['Sayfa_No'].unique()):
                sayfa_df = df[df['Sayfa_No'] == sayfa_no]
                sheet_name = f'Sayfa_{sayfa_no}'
                sayfa_df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"\n✓ İşlem tamamlandı!")
        print(f"✓ Toplam {len(tum_parcalar)} parça bulundu")
        print(f"✓ {len(sayfa_metinleri)} sayfa işlendi")
        print(f"✓ Sonuç dosyası: {dosya_excel}")
        
        # Özet bilgi
        print(f"\n--- ÖZET ---")
        for sayfa_no in sorted(df['Sayfa_No'].unique()):
            sayfa_parca_sayisi = len(df[df['Sayfa_No'] == sayfa_no])
            print(f"Sayfa {sayfa_no}: {sayfa_parca_sayisi} parça")
            
    else:
        print("Hiç parça bulunamadı!")

if __name__ == "__main__":
    main()
