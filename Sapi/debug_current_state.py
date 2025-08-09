#!/usr/bin/env python3
"""
Mevcut Veritabanı Durumu Debug Scripti
"""

import psycopg2
import traceback

def debug_current_state():
    """Mevcut veritabanı durumunu detaylı debug et"""
    
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
        
        print("🔍 VERİTABANI DURUMU DEBUG RAPORU")
        print("="*60)
        
        # 1. Bağlantı bilgileri
        cursor.execute("SELECT current_database(), current_user, inet_server_addr(), inet_server_port()")
        conn_info = cursor.fetchone()
        if conn_info:
            print(f"🗄️ Database: {conn_info[0]}")
            print(f"👤 User: {conn_info[1]}")
            print(f"🌐 Host: {conn_info[2]}:{conn_info[3]}")
        
        # 2. PostgreSQL versiyon bilgisi
        cursor.execute("SELECT version()")
        version = cursor.fetchone()
        if version:
            print(f"📊 PostgreSQL: {version[0][:80]}...")
        
        # 3. Tüm tabloları listele
        cursor.execute("""
            SELECT 
                t.table_name,
                t.table_type,
                pg_size_pretty(pg_total_relation_size(c.oid)) as size
            FROM information_schema.tables t
            LEFT JOIN pg_class c ON c.relname = t.table_name
            WHERE t.table_schema = 'public'
            ORDER BY t.table_name
        """)
        tables = cursor.fetchall()
        
        print(f"\n📋 TOPLAM {len(tables)} TABLO BULUNDU:")
        print("-" * 60)
        
        for table_info in tables:
            table_name = table_info[0]
            table_type = table_info[1]
            table_size = table_info[2] if table_info[2] else "Bilinmiyor"
            
            # Kayıt sayısını al
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count_result = cursor.fetchone()
                count = count_result[0] if count_result else 0
            except:
                count = "Hata"
            
            print(f"📊 {table_name}")
            print(f"   Tür: {table_type}")
            print(f"   Boyut: {table_size}")
            print(f"   Kayıt: {count:,}" if isinstance(count, int) else f"   Kayıt: {count}")
            print()
        
        # 4. Hamdata detaylı analiz
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'hamdata'
            )
        """)
        hamdata_exists = cursor.fetchone()
        
        if hamdata_exists and hamdata_exists[0]:
            print("🎯 HAMDATA DETAYLI ANALİZ:")
            print("-" * 40)
            
            # Hamdata yapısı
            cursor.execute("""
                SELECT column_name, data_type, character_maximum_length, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'hamdata' 
                ORDER BY ordinal_position
            """)
            columns = cursor.fetchall()
            
            print(f"📋 Sütun Yapısı ({len(columns)} sütun):")
            for col in columns:
                col_name = col[0]
                data_type = col[1]
                max_length = f"({col[2]})" if col[2] else ""
                nullable = "NULL" if col[3] == "YES" else "NOT NULL"
                print(f"   • {col_name}: {data_type}{max_length} - {nullable}")
            
            # Hamdata istatistikleri
            cursor.execute("SELECT COUNT(*) FROM hamdata")
            total_hamdata = cursor.fetchone()
            if total_hamdata:
                print(f"\n📈 Toplam Hamdata Kayıt: {total_hamdata[0]:,}")
            
            # Null/boş değer analizi
            print(f"\n🔍 NULL/BOŞ DEĞER ANALİZİ:")
            key_columns = ['mac_id', 'turnuva_adi', 'ev_sahibi_takim', 'deplasman_takim', 'tarih']
            
            for col in key_columns:
                cursor.execute(f"""
                    SELECT 
                        COUNT(*) as toplam,
                        COUNT(CASE WHEN {col} IS NULL OR {col} = '' THEN 1 END) as bos_null,
                        COUNT(CASE WHEN {col} IS NOT NULL AND {col} != '' THEN 1 END) as dolu
                    FROM hamdata
                """)
                stats = cursor.fetchone()
                if stats:
                    bos_oran = (stats[1] / stats[0] * 100) if stats[0] > 0 else 0
                    print(f"   • {col}: {stats[2]:,} dolu, {stats[1]:,} boş (%{bos_oran:.1f} boş)")
        
        # 5. İlişkisel tablo kontrolü
        relational_tables = ['countries', 'leagues', 'seasons', 'teams', 'team_seasons', 'matches', 'betting_odds']
        existing_relational = []
        
        for table in relational_tables:
            cursor.execute(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = '{table}'
                )
            """)
            exists = cursor.fetchone()
            if exists and exists[0]:
                existing_relational.append(table)
        
        if existing_relational:
            print(f"\n🔗 İLİŞKİSEL TABLOLAR ({len(existing_relational)}/{len(relational_tables)}):")
            print("-" * 40)
            
            for table in existing_relational:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count_result = cursor.fetchone()
                count = count_result[0] if count_result else 0
                
                # Foreign key'leri kontrol et
                cursor.execute(f"""
                    SELECT 
                        kcu.column_name,
                        ccu.table_name AS foreign_table_name,
                        ccu.column_name AS foreign_column_name
                    FROM information_schema.table_constraints AS tc 
                    JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage AS ccu
                        ON ccu.constraint_name = tc.constraint_name
                    WHERE tc.constraint_type = 'FOREIGN KEY' 
                    AND tc.table_name = '{table}'
                """)
                foreign_keys = cursor.fetchall()
                
                print(f"📊 {table}: {count:,} kayıt")
                if foreign_keys:
                    print(f"   🔗 Foreign Keys:")
                    for fk in foreign_keys:
                        print(f"      {fk[0]} -> {fk[1]}.{fk[2]}")
                print()
        
        # 6. Son güncelleme tarihleri
        print("📅 SON GÜNCELLEMELERİ:")
        print("-" * 30)
        
        for table in tables:
            table_name = table[0]
            
            # created_at veya updated_at sütunu var mı kontrol et
            cursor.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}' 
                AND column_name IN ('created_at', 'updated_at')
            """)
            time_columns = cursor.fetchall()
            
            if time_columns:
                time_col = time_columns[0][0]
                cursor.execute(f"SELECT MAX({time_col}) FROM {table_name}")
                last_update = cursor.fetchone()
                if last_update and last_update[0]:
                    print(f"   • {table_name}: {last_update[0]}")
        
        cursor.close()
        pg_conn.close()
        
        print("\n" + "="*60)
        print("✅ Debug raporu tamamlandı!")
        
    except Exception as e:
        print(f"❌ Debug hatası: {e}")
        print("\n🔍 DETAYLI HATA BİLGİSİ:")
        print("-" * 40)
        print(traceback.format_exc())

if __name__ == "__main__":
    debug_current_state()
