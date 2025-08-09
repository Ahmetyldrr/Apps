#!/usr/bin/env python3
"""
Veritabanı Test Scripti
"""

import psycopg2
from datetime import datetime

def test_database_connection():
    """Veritabanı bağlantısını test et"""
    
    db_config = {
        "dbname": "soccerdb",
        "user": "ahmet21",
        "password": "diclem2121.",
        "host": "165.227.130.23",
        "port": "5432"
    }
    
    try:
        print("🔗 Veritabanı bağlantısı test ediliyor...")
        
        pg_conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['dbname'],
            user=db_config['user'],
            password=db_config['password'],
            connect_timeout=10
        )
        cursor = pg_conn.cursor()
        
        print("✅ Bağlantı başarılı!")
        
        # PostgreSQL versiyonu
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        if version:
            print(f"📊 PostgreSQL: {version[0][:50]}...")
        
        # Veritabanı adı
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()
        if db_name:
            print(f"🗄️ Aktif Veritabanı: {db_name[0]}")
        
        # Tablo sayısı
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        table_count = cursor.fetchone()
        if table_count:
            print(f"📋 Toplam Tablo: {table_count[0]}")
        
        # Tabloları listele
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"📊 Tablolar:")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count_result = cursor.fetchone()
                count = count_result[0] if count_result else 0
                print(f"   • {table[0]}: {count:,} kayıt")
        
        # Bağlantı süresini test et
        start_time = datetime.now()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        end_time = datetime.now()
        
        response_time = (end_time - start_time).total_seconds() * 1000
        print(f"⚡ Bağlantı Hızı: {response_time:.2f}ms")
        
        cursor.close()
        pg_conn.close()
        
        print("✅ Test başarıyla tamamlandı!")
        return True
        
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return False

def test_sample_queries():
    """Örnek sorgular ile test et"""
    
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
        
        print("\n🧪 ÖRNEK SORGULAR TEST EDİLİYOR")
        print("="*40)
        
        # Test 1: Hamdata var mı?
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'hamdata'
            )
        """)
        hamdata_exists = cursor.fetchone()
        if hamdata_exists and hamdata_exists[0]:
            print("✅ Hamdata tablosu mevcut")
            
            # Hamdata kayıt sayısı
            cursor.execute("SELECT COUNT(*) FROM hamdata")
            hamdata_count = cursor.fetchone()
            if hamdata_count:
                print(f"📊 Hamdata kayıt sayısı: {hamdata_count[0]:,}")
        else:
            print("❌ Hamdata tablosu bulunamadı")
        
        # Test 2: İlişkisel tablolar var mı?
        relational_tables = ['countries', 'leagues', 'seasons', 'teams', 'matches']
        
        for table in relational_tables:
            cursor.execute(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = '{table}'
                )
            """)
            table_exists = cursor.fetchone()
            if table_exists and table_exists[0]:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count_result = cursor.fetchone()
                count = count_result[0] if count_result else 0
                print(f"✅ {table}: {count:,} kayıt")
            else:
                print(f"❌ {table} tablosu yok")
        
        # Test 3: Örnek join sorgusu
        try:
            cursor.execute("""
                SELECT m.mac_id, l.turnuva_adi, m.ev_sahibi_takim, m.deplasman_takim
                FROM matches m
                JOIN leagues l ON m.turnuva_id = l.turnuva_id
                LIMIT 3
            """)
            join_results = cursor.fetchall()
            
            if join_results:
                print("✅ Join sorgusu başarılı:")
                for result in join_results:
                    print(f"   {result[1]}: {result[2]} vs {result[3]}")
            else:
                print("⚠️ Join sorgusu sonuç vermedi")
                
        except Exception as e:
            print(f"❌ Join sorgusu hatası: {e}")
        
        cursor.close()
        pg_conn.close()
        
        print("✅ Tüm testler tamamlandı!")
        
    except Exception as e:
        print(f"❌ Test hatası: {e}")

if __name__ == "__main__":
    print("🧪 VERİTABANI TEST SÜİTİ")
    print("="*40)
    
    # Temel bağlantı testi
    if test_database_connection():
        # Detaylı testler
        test_sample_queries()
    else:
        print("❌ Temel bağlantı başarısız, testler durduruluyor")
    
    print("="*40)
    print("🎉 Test süreci tamamlandı!")
