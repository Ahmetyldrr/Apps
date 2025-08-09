#!/usr/bin/env python3
"""
Hızlı Test Scripti
"""

import psycopg2
import http.client
import json

def quick_connection_test():
    """Hızlı bağlantı testi"""
    print("🚀 HIZLI BAĞLANTI TESTİ")
    print("="*30)
    
    db_config = {
        "dbname": "soccerdb",
        "user": "ahmet21",
        "password": "diclem2121.",
        "host": "165.227.130.23",
        "port": "5432"
    }
    
    try:
        # Veritabanı bağlantısı
        print("🔗 Veritabanı test ediliyor...")
        pg_conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['dbname'],
            user=db_config['user'],
            password=db_config['password'],
            connect_timeout=5
        )
        cursor = pg_conn.cursor()
        
        cursor.execute("SELECT 1")
        cursor.fetchone()
        print("✅ Veritabanı bağlantısı OK")
        
        # Hamdata kontrolü
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'hamdata'
            )
        """)
        result = cursor.fetchone()
        hamdata_exists = result[0] if result is not None else False
        
        if hamdata_exists:
            cursor.execute("SELECT COUNT(*) FROM hamdata")
            count_result = cursor.fetchone()
            count = count_result[0] if count_result is not None else 0
            print(f"✅ Hamdata: {count:,} kayıt")
        else:
            print("❌ Hamdata tablosu yok")
        
        cursor.close()
        pg_conn.close()
        
    except Exception as e:
        print(f"❌ Veritabanı hatası: {e}")
    
    # API bağlantısı
    try:
        print("\n🌐 API test ediliyor...")
        conn = http.client.HTTPSConnection('vd.mackolik.com', timeout=10)
        headers = {
            'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        conn.request('GET', '/livedata?date=10/08/2025', headers=headers)
        response = conn.getresponse()
        
        if response.status == 200:
            data = response.read()
            json_data = json.loads(data).get("m")
            if json_data:
                print(f"✅ API: {len(json_data)} maç verisi alındı")
            else:
                print("⚠️ API: Veri boş")
        else:
            print(f"❌ API: HTTP {response.status}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ API hatası: {e}")
    
    print("\n🎉 Hızlı test tamamlandı!")

if __name__ == "__main__":
    quick_connection_test()
