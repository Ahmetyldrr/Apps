import psycopg2

def clean_database():
    """Mevcut veritabanındaki tüm tabloları sil"""
    
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
        
        # Mevcut tabloları listele
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"📊 {len(tables)} tablo bulundu:")
            for table in tables:
                print(f"   - {table[0]}")
            
            print("\n🗑️ Tüm tablolar siliniyor...")
            
            # Foreign key constraint'lerini kaldırmak için CASCADE kullan
            for table in tables:
                table_name = table[0]
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
                    print(f"✅ {table_name} tablosu silindi")
                except Exception as e:
                    print(f"⚠️ {table_name} silinirken hata: {e}")
            
            pg_conn.commit()
            print("\n🎉 Tüm tablolar başarıyla silindi!")
            
        else:
            print("ℹ️ Silinecek tablo bulunamadı.")
        
        # Son kontrol
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE';
        """)
        remaining_tables = cursor.fetchall()
        
        if remaining_tables:
            print(f"⚠️ {len(remaining_tables)} tablo hala mevcut:")
            for table in remaining_tables:
                print(f"   - {table[0]}")
        else:
            print("✅ Veritabanı tamamen temizlendi!")
        
        cursor.close()
        pg_conn.close()
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        print(f"Detay: {traceback.format_exc()}")

if __name__ == "__main__":
    print("🗑️ Veritabanı Temizleme İşlemi")
    print("=" * 40)
    
    # Otomatik onay
    print("⚠️ TÜM TABLOLAR SİLİNİYOR...")
    clean_database()
    
    print("=" * 40)
    print("✅ Temizleme işlemi tamamlandı!")
