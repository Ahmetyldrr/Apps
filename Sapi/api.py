import http.client
import pandas as pd
import json
from sqlalchemy import create_engine, text

# Tarih parametresi
datex = "01/08/2025"  # Bu tarihi istediğiniz gibi değiştirebilirsiniz.

conn = http.client.HTTPSConnection('vd.mackolik.com')
headers = {
    'accept': '*/*',
    'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    'if-modified-since': 'Tue, 05 Aug 2025 22:34:53 GMT',
    'origin': 'https://arsiv.mackolik.com',
    'priority': 'u=1, i',
    'referer': 'https://arsiv.mackolik.com/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
}
conn.request('GET', f'/livedata?date={datex}', headers=headers)
response = conn.getresponse()

data = response.read()
df = None # df'i başlangıçta None olarak tanımla
if response.status == 200:  
    json_data = json.loads(data).get("m") # .get() ile daha güvenli erişim
    if json_data:
        df = pd.DataFrame(json_data)
    else:
        print(f"{datex} tarihi için veri bulunamadı.")
else:
    print(f"Veri çekilemedi. HTTP Status: {response.status}")

# df'in veri içerip içermediğini kontrol et
if df is not None and not df.empty:
    print(f"{len(df)} adet maç verisi bulundu.")
    # --- Verileri doğrudan veritabanına gönder (SQLAlchemy ile) ---
    def insert_data_to_db_sync(dataframe):
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
                # Sütun adlarını 'col_0', 'col_1', ... olarak ayarla
                dataframe.columns = [f"col_{i}" for i in range(len(dataframe.columns))]
                # Tüm verileri string'e çevir
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
                conn.commit() # Değişiklikleri onayla
                print(f"Ana tabloya {result.rowcount} kayıt eklendi/güncellendi.")

        except Exception as e:
            print(f"\nVeritabanı işlemi sırasında bir hata oluştu: {e}")
        finally:
            engine.dispose()
            print("Veritabanı bağlantısı kapatıldı.")

    # Senkron fonksiyonu çalıştır
    insert_data_to_db_sync(df)
    # --- Veri gönderme sonu ---

    print("\nİlk 5 veri:")
    print(df.head())
else:
    print("Veritabanına yazılacak veri bulunamadığı için işlem sonlandırıldı.")