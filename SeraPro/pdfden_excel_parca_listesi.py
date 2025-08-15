import PyPDF2
import pandas as pd

# PDF ve Excel dosya adları
dosya_pdf = 'MONTAJ KİTAPÇIĞI-TEMEL.pdf'
dosya_excel = 'Parca_Listesi.xlsx'

# PDF'den metin çıkarma
def pdfden_parca_listesi_cek(pdf_yolu):
    reader = PyPDF2.PdfReader(pdf_yolu)
    tum_sayfalar = []
    for i, sayfa in enumerate(reader.pages):
        metin = sayfa.extract_text()
        tum_sayfalar.append({'Sayfa': i+1, 'Metin': metin})
    return tum_sayfalar

# Parça listelerini bölümlere ayırma (örnek, gerçek bölümlendirme için metin yapısına bakmak gerekir)
def bolumlere_ayir(sayfa_metinleri):
    bolumler = []
    for sayfa in sayfa_metinleri:
        # Burada gerçek bölümlendirme için metin analizi yapılmalı
        bolumler.append({'Sayfa': sayfa['Sayfa'], 'Bolum': 'Bölüm', 'Parca': sayfa['Metin']})
    return bolumler

# Ana akış
def main():
    sayfa_metinleri = pdfden_parca_listesi_cek(dosya_pdf)
    bolumler = bolumlere_ayir(sayfa_metinleri)
    df = pd.DataFrame(bolumler)
    df.to_excel(dosya_excel, index=False)
    print(f"{dosya_excel} dosyasına yazıldı.")

if __name__ == "__main__":
    main()
