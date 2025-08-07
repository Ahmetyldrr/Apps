import pandas as pd
from pathlib import Path
import json

file_path = 'Ağustos_TT.xlsx'

if Path(file_path).exists():
    print(f"Excel dosyası bulundu: {file_path}")
    
    # Pandas ile sekmelerimizi okumaya çalış
    try:
        # Tüm sekmeleri oku
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
        
        print(f"Toplam {len(sheet_names)} sekme bulundu:")
        for i, name in enumerate(sheet_names, 1):
            print(f"{i}. {name}")
        
        analysis_data = {}
        
        for sheet_name in sheet_names:
            print(f"\n--- {sheet_name} sekmesi analiz ediliyor ---")
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Sekme bilgileri
                sheet_info = {
                    'name': sheet_name,
                    'rows': len(df),
                    'columns': len(df.columns),
                    'column_names': list(df.columns),
                    'has_data': not df.empty
                }
                
                if not df.empty:
                    # İlk birkaç satırı al
                    sample_data = df.head(10).fillna('').to_dict('records')
                    sheet_info['sample_data'] = sample_data
                    
                    # Veri türleri
                    sheet_info['data_types'] = {col: str(dtype) for col, dtype in df.dtypes.items()}
                    
                    # Boş olmayan değer sayıları
                    sheet_info['non_null_counts'] = df.count().to_dict()
                
                analysis_data[sheet_name] = sheet_info
                
                print(f"  - Satır sayısı: {len(df)}")
                print(f"  - Sütun sayısı: {len(df.columns)}")
                print(f"  - Sütunlar: {list(df.columns)}")
                
                if not df.empty:
                    print("  - İlk 3 satır:")
                    print(df.head(3).to_string(index=False))
                    
            except Exception as e:
                print(f"  - Hata oluştu: {e}")
                analysis_data[sheet_name] = {'name': sheet_name, 'error': str(e)}
        
        # Analiz sonuçlarını JSON'a kaydet
        with open('excel_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"\nAnaliz tamamlandı! Sonuçlar 'excel_analysis.json' dosyasına kaydedildi.")
        
    except Exception as e:
        print(f"Excel dosyası okunurken hata oluştu: {e}")
        
else:
    print("Excel dosyası bulunamadı!")
