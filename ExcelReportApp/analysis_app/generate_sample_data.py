import pandas as pd
import numpy as np
import os

# Betiğin bulunduğu dizini temel al
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
    print(f"'{DATA_DIR}' klasörü oluşturuldu.")

# 10 adet örnek Excel dosyası oluştur
for i in range(1, 11):
    data = {
        'Tarih': pd.to_datetime(pd.date_range(start='2023-01-01', periods=50, freq='D')),
        'Talep_Miktari': np.random.randint(100, 500, size=50),
        'Stok_Seviyesi': np.random.randint(50, 200, size=50),
        'Satis_Fiyati': np.random.uniform(10.5, 50.0, size=50).round(2)
    }
    df = pd.DataFrame(data)
    
    file_path = os.path.join(DATA_DIR, f'analiz_raporu_{i}.xlsx')
    df.to_excel(file_path, index=False, engine='xlsxwriter')

print(f"{len(os.listdir(DATA_DIR))} adet örnek Excel dosyası '{DATA_DIR}' klasörüne oluşturuldu.")
