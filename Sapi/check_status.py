#!/usr/bin/env python3
"""
Basitleştirilmiş Veritabanı Durumu Kontrol
"""

import psycopg2

def check_database_status():
    """Veritabanı durumunu kontrol et"""
    
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
        
        print("🔍 VERİTABANI DURUM KONTROLÜ")
        print("="*50)
        
        # Tablo listesi
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        print(f"📊 Toplam {len(tables)} tablo bulundu:")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            result = cursor.fetchone()
            count = result[0] if result is not None else 0
            print(f"   • {table_name}: {count:,} kayıt")
        
        print("\n" + "="*50)
        
        # Hamdata detayı varsa göster
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'hamdata'
            );
        """)
        hamdata_row = cursor.fetchone()
        hamdata_exists = hamdata_row[0] if hamdata_row is not None else False
        
        if hamdata_exists:
            print("📋 HAMDATA DETAYI:")
            cursor.execute("SELECT COUNT(*) FROM hamdata")
            total_row = cursor.fetchone()
            total = total_row[0] if total_row is not None else 0
            print(f"   📈 Toplam Kayıt: {total}")
            
            # Örnek kayıtlar
            cursor.execute("SELECT mac_id, turnuva_adi, ev_sahibi_takim, deplasman_takim FROM hamdata LIMIT 5")
            samples = cursor.fetchall()
            if samples:
                print("   🔍 Örnek Kayıtlar:")
                for sample in samples:
                    print(f"      {sample[0]}: {sample[1]} | {sample[2]} vs {sample[3]}")
        
        # İlişkisel tablolar varsa kontrol et
        relational_tables = ['countries', 'leagues', 'seasons', 'teams', 'team_seasons', 'matches', 'betting_odds']
        relational_exists = []
        
        for table in relational_tables:
            cursor.execute(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = '{table}'
                );
            """)
            row = cursor.fetchone()
            exists = row[0] if row is not None else False
            if exists:
                relational_exists.append(table)
        
        if relational_exists:
            print(f"\n🔗 İLİŞKİSEL TABLOLAR ({len(relational_exists)}/{len(relational_tables)}):")
            for table in relational_exists:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                result = cursor.fetchone()
                count = result[0] if result is not None else 0
                print(f"   • {table}: {count:,} kayıt")
        
        cursor.close()
        pg_conn.close()
        
        print("\n✅ Kontrol tamamlandı!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    check_database_status()
