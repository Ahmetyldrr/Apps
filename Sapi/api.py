#!/usr/bin/env python3
"""
Orijinal API Script - Mackolik Futbol Verileri
Ham API verilerini çeker ve PostgreSQL veritabanına kaydeder
"""

import http.client
import pandas as pd
import json
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

def get_football_data():
    """Mackolik API'den futbol maç verilerini çek"""
    
    # Bugünün tarihi
    datex = datetime.now().strftime("%d/%m/%Y")
    
    print(f"🌐 API'den {datex} tarihli veriler çekiliyor...")
    
    try:
        # API bağlantısı
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
        
        print(f"📡 HTTP Response: {response.status}")
        
        if response.status == 200:
            data = response.read()
            
            try:
                json_data = json.loads(data)
                matches = json_data.get("m", [])
                
                if matches:
                    print(f"✅ {len(matches)} adet maç verisi alındı")
                    df = pd.DataFrame(matches)
                    return df
                else:
                    print("⚠️ Maç verisi bulunamadı (boş)")
                    return None
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON parse hatası: {e}")
                return None
        else:
            print(f"❌ API hatası: HTTP {response.status}")
            error_data = response.read()
            print(f"Hata detayı: {error_data[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()

def save_to_database(dataframe):
    """DataFrame'i PostgreSQL veritabanına kaydet"""
    
    db_config = {
        "dbname": "soccerdb",
        "user": "ahmet21",
        "password": "diclem2121.",
        "host": "165.227.130.23",
        "port": "5432"
    }
    
    try:
        print("🔗 Veritabanına bağlanılıyor...")
        
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
        
        # Raw data tablosu oluştur (tüm sütunlarla)
        print("🏗️ Raw data tablosu kontrol ediliyor...")
        
        # Sütun sayısını belirle
        max_columns = dataframe.shape[1]
        print(f"📊 DataFrame'de {max_columns} sütun bulundu")
        
        # Dinamik sütun oluşturma
        column_definitions = []
        for i in range(max_columns):
            column_definitions.append(f"col_{i} TEXT")
        
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS raw_football_data (
                id SERIAL PRIMARY KEY,
                {', '.join(column_definitions)},
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        
        cursor.execute(create_table_query)
        pg_conn.commit()
        print(f"✅ Raw data tablosu hazır ({max_columns} sütun)")
        
        # Verileri hazırla
        print("🔄 Veriler hazırlanıyor...")
        data_to_insert = []
        
        for idx, row in dataframe.iterrows():
            # Her satırı string'e dönüştür
            row_data = []
            for i in range(max_columns):
                if i < len(row):
                    cell_value = str(row.iloc[i]) if row.iloc[i] is not None else ''
                else:
                    cell_value = ''
                row_data.append(cell_value)
            
            data_to_insert.append(row_data)
        
        # Bulk insert
        print(f"📥 {len(data_to_insert)} kayıt veritabanına ekleniyor...")
        
        # Insert query oluştur
        column_placeholders = ', '.join(['%s'] * max_columns)
        column_names = ', '.join([f'col_{i}' for i in range(max_columns)])
        
        insert_query = f"""
            INSERT INTO raw_football_data ({column_names})
            VALUES ({column_placeholders})
        """
        
        # Execute_values ile bulk insert
        execute_values(
            cursor,
            insert_query,
            data_to_insert,
            page_size=100
        )
        
        pg_conn.commit()
        
        # Sonuçları kontrol et
        cursor.execute("SELECT COUNT(*) FROM raw_football_data")
        count_result = cursor.fetchone()
        total_count = count_result[0] if count_result is not None else 0
        
        print(f"✅ {len(data_to_insert)} kayıt başarıyla eklendi!")
        print(f"📊 Toplam veritabanında {total_count} kayıt bulunuyor")
        
        # Örnek veri göster
        print("\n🔍 İlk birkaç kayıt:")
        cursor.execute(f"SELECT col_0, col_1, col_2, col_3, col_4 FROM raw_football_data ORDER BY id DESC LIMIT 3")
        sample_data = cursor.fetchall()
        
        for i, sample in enumerate(sample_data, 1):
            print(f"   {i}. {sample[0]} | {sample[1]} | {sample[2]} vs {sample[4]}")
        
    except Exception as e:
        print(f"❌ Veritabanı hatası: {e}")
        import traceback
        print(f"Detay: {traceback.format_exc()}")
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'pg_conn' in locals():
            pg_conn.close()
        print("🔐 Veritabanı bağlantısı kapatıldı")

def analyze_data_structure(dataframe):
    """DataFrame yapısını analiz et"""
    
    print("\n🔍 VERİ YAPISI ANALİZİ")
    print("="*40)
    
    # Temel bilgiler
    print(f"📊 Satır sayısı: {len(dataframe)}")
    print(f"📊 Sütun sayısı: {dataframe.shape[1]}")
    
    # İlk birkaç sütunun örnek değerleri
    print(f"\n📋 İLK 10 SÜTUN ÖRNEKLERİ:")
    for i in range(min(10, dataframe.shape[1])):
        sample_values = dataframe.iloc[:3, i].tolist()
        print(f"   Sütun {i}: {sample_values}")
    
    # Özel sütunları bul
    if dataframe.shape[1] > 36:
        print(f"\n🎯 36. SÜTUN (Turnuva Bilgisi) ANALİZİ:")
        turnuva_samples = dataframe.iloc[:3, 36].tolist()
        for i, sample in enumerate(turnuva_samples):
            print(f"   Örnek {i+1}: {sample}")
            if isinstance(sample, list) and len(sample) > 0:
                print(f"      Liste uzunluğu: {len(sample)}")
                print(f"      İlk 5 eleman: {sample[:5]}")
    
    # Veri tiplerini kontrol et
    print(f"\n📈 VERİ TİPLERİ:")
    type_counts = {}
    for col in dataframe.columns:
        dtype = str(dataframe[col].dtype)
        type_counts[dtype] = type_counts.get(dtype, 0) + 1
    
    for dtype, count in type_counts.items():
        print(f"   {dtype}: {count} sütun")

def main():
    """Ana fonksiyon"""
    
    print("🚀 MACKOLIK API VERİ ÇEKİCİ")
    print("="*50)
    print(f"🕒 Başlangıç: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. API'den veri çek
    df = get_football_data()
    
    if df is not None and not df.empty:
        print(f"\n📦 {len(df)} kayıt başarıyla alındı")
        
        # 2. Veri yapısını analiz et
        analyze_data_structure(df)
        
        # 3. Veritabanına kaydet
        print(f"\n💾 Veritabanına kaydetme işlemi başlıyor...")
        save_to_database(df)
        
        print(f"\n🎉 İşlem başarıyla tamamlandı!")
        print(f"🕒 Bitiş: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    else:
        print("❌ Veri alınamadı, işlem sonlandırılıyor")

if __name__ == "__main__":
    main()
