import pandas as pd
import openpyxl
from pathlib import Path

file_path = 'Ağustos_TT.xlsx'
if Path(file_path).exists():
    workbook = openpyxl.load_workbook(file_path, data_only=True)
    sheet_names = workbook.sheetnames
    print('Sekme isimleri:')
    for i, name in enumerate(sheet_names, 1):
        print(f'{i}. {name}')
        
    # Her sekme için kısa analiz
    for sheet_name in sheet_names:
        print(f'\n--- {sheet_name} ---')
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f'Satır sayısı: {len(df)}')
            print(f'Sütun sayısı: {len(df.columns)}')
            print(f'Sütunlar: {list(df.columns)[:3]}...' if len(df.columns) > 3 else f'Sütunlar: {list(df.columns)}')
            
            if not df.empty:
                print('İlk 3 satır:')
                print(df.head(3).to_string())
        except Exception as e:
            print(f'Hata: {e}')
else:
    print('Dosya bulunamadı')
