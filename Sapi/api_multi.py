import http.client
import pandas as pd
import json
from sqlalchemy import create_engine, text
from datetime import date, timedelta
import time

# --- Ayarlar ---
# Veri çekilecek tarih aralığını belirleyin
start_date = date(2025,8, 1)
end_date = date(2025,8,3) # Aralık ayının tamamı

def insert_data_to_db_sync(dataframe):
    """Verileri DataFrame'den veritabanına toplu olarak ekler/günceller."""
    db_config = {
        "dbname": "soccerdb",
        "user": "ahmet21",
        "password": "diclem2121.",
        "host": "165.227.130.23",
        "port": "5432"
    }
    engine = create_engine(
        f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    )
    
    try:
        with engine.connect() as conn:
            print("\nVeritabanı bağlantısı başarılı.")
            
            # 1. Ana tablonun var olduğundan emin ol
            columns_for_create = ", ".join([f"col_{i} TEXT" for i in range(1, 38)])
            create_table_query = text(f"""
                CREATE TABLE IF NOT EXISTS hamdata (
                    col_0 TEXT PRIMARY KEY,
                    {columns_for_create}
                );
            """)
            conn.execute(create_table_query)
            print("Tablo 'hamdata' kontrol edildi/oluşturuldu.")

            # 2. DataFrame'i veritabanına uygun hale getir
            dataframe.columns = [f"col_{i}" for i in range(len(dataframe.columns))]
            dataframe = dataframe.astype(str)

            # 3. Verileri geçici bir tabloya toplu olarak yaz
            temp_table_name = "hamdata_temp"
            dataframe.to_sql(temp_table_name, conn, if_exists='replace', index=False)
            print(f"{len(dataframe)} kayıt geçici tabloya yazıldı.")

            # 4. Geçici tablodan ana tabloya UPSERT yap
            columns_list = [f"col_{i}" for i in range(38)]
            columns_str = ", ".join(columns_list)
            update_set_str = ", ".join([f"{col} = EXCLUDED.{col}" for col in columns_list[1:]])
            
            upsert_query = text(f"""
                INSERT INTO hamdata ({columns_str})
                SELECT {columns_str} FROM {temp_table_name}
                ON CONFLICT (col_0) DO UPDATE SET {update_set_str};
            """)
            
            result = conn.execute(upsert_query)
            conn.commit()
            print(f"Ana tabloya {result.rowcount} kayıt eklendi/güncellendi.")

    except Exception as e:
        print(f"\nVeritabanı işlemi sırasında bir hata oluştu: {e}")
    finally:
        engine.dispose()
        print("Veritabanı bağlantısı kapatıldı.")

# --- Ana Betik ---
def daterange(start, end):
    """Tarih aralığında her gün için bir tarih nesnesi döndürür."""
    for n in range(int((end - start).days) + 1):
        yield start + timedelta(n)

all_dfs = []
conn = http.client.HTTPSConnection('vd.mackolik.com')
headers = {
    'accept': '*/*',
    'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://arsiv.mackolik.com',
    'referer': 'https://arsiv.mackolik.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
}

print(f"Veri çekme işlemi başlatılıyor: {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}")

for single_date in daterange(start_date, end_date):
    date_str_req = single_date.strftime("%d/%m/%Y") # API için format: AA/GG/YYYY
    print(f"Taranan tarih: {single_date.strftime('%d.%m.%Y')}")
    
    try:
        conn.request('GET', f'/livedata?date={date_str_req}', headers=headers)
        response = conn.getresponse()
        
        if response.status == 200:
            data = response.read()
            json_data = json.loads(data).get("m")
            if json_data:
                df = pd.DataFrame(json_data)
                all_dfs.append(df)
                print(f"  -> {len(df)} kayıt bulundu.")
            else:
                print(f"  -> Bu tarih için veri yok.")
        else:
            print(f"  -> Hata! HTTP Status: {response.status}")
            conn.close()
            conn = http.client.HTTPSConnection('vd.mackolik.com') # Bağlantıyı yenile

    except Exception as e:
        print(f"  -> İstek sırasında hata: {e}")
        conn.close()
        conn = http.client.HTTPSConnection('vd.mackolik.com') # Bağlantıyı yenile

    time.sleep(4) # Sunucuyu yormamak için 1 saniye bekle

conn.close()

if all_dfs:
    final_df = pd.concat(all_dfs, ignore_index=True)
    
    # --- Tekrar Eden Kayıtları Temizleme ---
    # Veritabanına göndermeden önce, aynı ID'ye sahip (sütun 0) tekrar eden kayıtları temizle.
    # 'keep="last"' parametresi sayesinde, tekrar eden ID'lerden en sonuncusu tutulur.
    initial_rows = len(final_df)
    # Sütun 0'a göre tekrar edenleri bul ve sonuncuyu tut
    final_df.drop_duplicates(subset=[0], keep='last', inplace=True)
    final_rows = len(final_df)
    
    if initial_rows > final_rows:
        print(f"\n{initial_rows - final_rows} adet tekrar eden kayıt bulundu ve kaldırıldı. Yalnızca en güncel olanlar tutuldu.")
    # --- Temizleme Sonu ---

    print(f"\nToplam {len(final_df)} benzersiz kayıt bulundu. Veritabanına yazılıyor...")
    
    insert_data_to_db_sync(final_df)
    
    print("\nİşlem tamamlandı. Toplam veriden ilk 5 satır:")
    print(final_df.head())
else:
    print("\nBelirtilen tarih aralığında hiç veri bulunamadı.")
