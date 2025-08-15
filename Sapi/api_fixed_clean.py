import http.client
import pandas as pd
import json
import psycopg2
from psycopg2.extras import execute_values

# Tarih parametresi
datex = "09/08/2025"

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
df = None
if response.status == 200:  
    json_data = json.loads(data).get("m")
    if json_data:
        df = pd.DataFrame(json_data)
    else:
        print(f"{datex} tarihi için veri bulunamadı.")
else:
    print(f"Veri çekilemedi. HTTP Status: {response.status}")

if df is not None and not df.empty:
    print(f"{len(df)} adet maç verisi bulundu.")
    
    def insert_data_to_db_sync(dataframe):
        db_config = {
            "dbname": "soccerdb",
            "user": "ahmet21",
            "password": "diclem2121.",
            "host": "165.227.130.23",
            "port": "5432"
        }
        
        try:
            pg_conn = psycopg2.connect(
                host=db_config['host'],
                port=db_config['port'],
                database=db_config['dbname'],
                user=db_config['user'],
                password=db_config['password'],
                connect_timeout=10
            )
            cursor = pg_conn.cursor()
            print("✅ Veritabanı bağlantısı başarılı!")

            # Sadece gerekli sütunlarla tablo oluştur
            create_table_query = """
                CREATE TABLE IF NOT EXISTS hamdata (
                    mac_id TEXT PRIMARY KEY,
                    ev_id TEXT,
                    ev_sahibi_takim TEXT,
                    dep_id TEXT,
                    deplasman_takim TEXT,
                    kriter_id TEXT,
                    mac_durumu TEXT,
                    skor TEXT,
                    istatistik_7 TEXT,
                    saat TEXT,
                    oran_1 TEXT,
                    oran_x TEXT,
                    oran_2 TEXT,
                    oran_alt TEXT,
                    oran_ust TEXT,
                    ev_skor TEXT,
                    dep_skor TEXT,
                    iy_ev_skor TEXT,
                    iy_dep_skor TEXT,
                    kategori TEXT,
                    tarih TEXT,
                    turnuva_kategori_id TEXT,
                    ulke TEXT,
                    turnuva_id TEXT,
                    turnuva_adi TEXT,
                    sezon_id TEXT,
                    sezon TEXT,
                    turnuva_kodu TEXT
                );
            """
            cursor.execute(create_table_query)
            pg_conn.commit()
            print("✅ Tablo kontrol edildi/oluşturuldu.")

            # DataFrame'i sadece gerekli sütunlarla işle
            filtered_data = []
            for idx, row in dataframe.iterrows():
                # Turnuva bilgilerini ayrıştır
                try:
                    turnuva_raw = row[36] if len(row) > 36 else []
                    turnuva_info = turnuva_raw if isinstance(turnuva_raw, list) else []
                except:
                    turnuva_info = []
                
                turnuva_kategori_id = str(turnuva_info[0]) if len(turnuva_info) > 0 else ''
                turnuva_kategorisi = str(turnuva_info[1]) if len(turnuva_info) > 1 else ''
                turnuva_id = str(turnuva_info[2]) if len(turnuva_info) > 2 else ''
                turnuva_adi = str(turnuva_info[3]) if len(turnuva_info) > 3 else ''
                sezon_id = str(turnuva_info[4]) if len(turnuva_info) > 4 else ''
                sezon = str(turnuva_info[5]) if len(turnuva_info) > 5 else ''
                turnuva_kodu = str(turnuva_info[9]) if len(turnuva_info) > 9 else ''
                
                # Sadece gerekli sütunları tut
                filtered_row = [
                    str(row[0]),  # mac_id
                    str(row[1]),  # ev_id
                    str(row[2]),  # ev_sahibi_takim
                    str(row[3]),  # dep_id
                    str(row[4]),  # deplasman_takim
                    str(row[5]),  # kriter_id (deplasman_id olarak gelen)
                    str(row[6]),  # mac_durumu
                    str(row[7]),  # skor
                    str(row[14]),  # istatistik_7
                    str(row[16]),  # saat
                    str(row[18]),  # oran_1
                    str(row[19]),  # oran_x
                    str(row[20]),  # oran_2
                    str(row[21]),  # oran_alt
                    str(row[22]),  # oran_ust
                    str(row[29]),  # ev_skor
                    str(row[30]),  # dep_skor
                    str(row[31]),  # iy_ev_skor
                    str(row[32]),  # iy_dep_skor
                    str(row[34]),  # kategori
                    str(row[35]),  # tarih
                    turnuva_kategori_id,  # turnuva_kategori_id
                    turnuva_kategorisi,   # ulke
                    turnuva_id,           # turnuva_id
                    turnuva_adi,          # turnuva_adi
                    sezon_id,             # sezon_id
                    sezon,                # sezon
                    turnuva_kodu          # turnuva_kodu
                ]
                filtered_data.append(filtered_row)

            print(f"İşlenecek kayıt sayısı: {len(filtered_data)}")

            # Bulk UPSERT ile veritabanına ekle
            if filtered_data:
                execute_values(
                    cursor,
                    """
                    INSERT INTO hamdata (
                        mac_id, ev_id, ev_sahibi_takim, dep_id, deplasman_takim,
                        kriter_id, mac_durumu, skor, istatistik_7, saat,
                        oran_1, oran_x, oran_2, oran_alt, oran_ust,
                        ev_skor, dep_skor, iy_ev_skor, iy_dep_skor, kategori,
                        tarih, turnuva_kategori_id, ulke, turnuva_id, turnuva_adi,
                        sezon_id, sezon, turnuva_kodu
                    ) VALUES %s
                    ON CONFLICT (mac_id) DO UPDATE SET
                        ev_id = EXCLUDED.ev_id,
                        ev_sahibi_takim = EXCLUDED.ev_sahibi_takim,
                        dep_id = EXCLUDED.dep_id,
                        deplasman_takim = EXCLUDED.deplasman_takim,
                        kriter_id = EXCLUDED.kriter_id,
                        mac_durumu = EXCLUDED.mac_durumu,
                        skor = EXCLUDED.skor,
                        istatistik_7 = EXCLUDED.istatistik_7,
                        saat = EXCLUDED.saat,
                        oran_1 = EXCLUDED.oran_1,
                        oran_x = EXCLUDED.oran_x,
                        oran_2 = EXCLUDED.oran_2,
                        oran_alt = EXCLUDED.oran_alt,
                        oran_ust = EXCLUDED.oran_ust,
                        ev_skor = EXCLUDED.ev_skor,
                        dep_skor = EXCLUDED.dep_skor,
                        iy_ev_skor = EXCLUDED.iy_ev_skor,
                        iy_dep_skor = EXCLUDED.iy_dep_skor,
                        kategori = EXCLUDED.kategori,
                        tarih = EXCLUDED.tarih,
                        turnuva_kategori_id = EXCLUDED.turnuva_kategori_id,
                        ulke = EXCLUDED.ulke,
                        turnuva_id = EXCLUDED.turnuva_id,
                        turnuva_adi = EXCLUDED.turnuva_adi,
                        sezon_id = EXCLUDED.sezon_id,
                        sezon = EXCLUDED.sezon,
                        turnuva_kodu = EXCLUDED.turnuva_kodu
                    """,
                    filtered_data,
                    page_size=100
                )

                pg_conn.commit()
                print(f"✅ {len(filtered_data)} kayıt başarıyla işlendi! (Yeni eklendi veya güncellendi)")

                # İstatistik göster
                cursor.execute("SELECT COUNT(*) FROM hamdata")
                result = cursor.fetchone()
                total_count = result[0] if result is not None else 0
                print(f"📊 Toplam veritabanında {total_count} adet maç kaydı bulunuyor.")

        except Exception as e:
            print(f"❌ Veritabanı hatası: {e}")
        finally:
            if cursor:
                cursor.close()
            if pg_conn:
                pg_conn.close()
        
        print("İşlem tamamlandı!")

    # Fonksiyonu çağır
    insert_data_to_db_sync(df)
else:
    print("❌ Veri alınamadı veya boş.")
