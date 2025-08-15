import pandas as pd

try:
    # Excel dosyasını oku
    df = pd.read_excel('Montaj_Kitapcigi_Parca_Listesi.xlsx')
    
    print("=== EXCEL DOSYASI ANALİZİ ===")
    print(f"Toplam satır sayısı: {len(df)}")
    print(f"Sütunlar: {list(df.columns)}")
    
    print("\n=== İLK 10 SATIR ===")
    print(df.head(10))
    
    if 'Parca_Adi' in df.columns:
        print("\n=== ÖRNEK PARÇA ADLARI ===")
        unique_parts = df['Parca_Adi'].dropna().unique()[:20]
        for i, part in enumerate(unique_parts, 1):
            print(f"{i}. {part}")
    
    print("\n=== SAYFA DAĞILIMI ===")
    if 'Sayfa_No' in df.columns:
        page_counts = df['Sayfa_No'].value_counts().sort_index()
        for page, count in page_counts.head(10).items():
            print(f"Sayfa {page}: {count} öğe")
            
except Exception as e:
    print(f"Hata: {e}")
