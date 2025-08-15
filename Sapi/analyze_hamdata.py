#!/usr/bin/env python3
"""
Hamdata Tablosu Analiz Scripti
"""

import psycopg2
import pandas as pd

def analyze_hamdata():
    """Hamdata tablosunu detaylı analiz et"""
    
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
        
        print("🔍 HAMDATA TABLO ANALİZİ")
        print("="*50)
        
        # Tablo varlığını kontrol et
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'hamdata'
            );
        """)
        result = cursor.fetchone()
        exists = result[0] if result is not None else False
        
        if not exists:
            print("❌ Hamdata tablosu bulunamadı!")
            return
        
        # Temel istatistikler
        cursor.execute("SELECT COUNT(*) FROM hamdata")
        result = cursor.fetchone()
        total_count = result[0] if result is not None else 0
        print(f"📊 Toplam Kayıt: {total_count:,}")
        
        # Tablo yapısını göster
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'hamdata' 
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        
        print(f"\n📋 Tablo Yapısı ({len(columns)} sütun):")
        for col in columns:
            nullable = "NULL" if col[2] == "YES" else "NOT NULL"
            print(f"   • {col[0]} ({col[1]}) - {nullable}")
        
        # Örneklem veriler
        cursor.execute("SELECT * FROM hamdata LIMIT 5")
        sample_data = cursor.fetchall()
        
        if sample_data:
            print(f"\n🔍 Örnek Veriler:")
            for i, row in enumerate(sample_data, 1):
                print(f"   Kayıt {i}:")
                print(f"      Mac ID: {row[0]}")
                print(f"      Ev Takım: {row[2]} ({row[1]})")
                print(f"      Dep Takım: {row[4]} ({row[3]})")
                print(f"      Turnuva: {row[24]} - {row[26]}")
                print(f"      Skor: {row[7]}")
                print(f"      Tarih: {row[20]}")
                print()
        
        # Turnuva dağılımı
        cursor.execute("""
            SELECT turnuva_adi, COUNT(*) as mac_sayisi
            FROM hamdata 
            WHERE turnuva_adi IS NOT NULL AND turnuva_adi != ''
            GROUP BY turnuva_adi 
            ORDER BY mac_sayisi DESC 
            LIMIT 10
        """)
        tournaments = cursor.fetchall()
        
        if tournaments:
            print("🏆 En Fazla Maç Olan Turnuvalar:")
            for tournament in tournaments:
                print(f"   • {tournament[0]}: {tournament[1]:,} maç")
        
        # Ülke dağılımı
        cursor.execute("""
            SELECT ulke, COUNT(*) as mac_sayisi
            FROM hamdata 
            WHERE ulke IS NOT NULL AND ulke != ''
            GROUP BY ulke 
            ORDER BY mac_sayisi DESC 
            LIMIT 10
        """)
        countries = cursor.fetchall()
        
        if countries:
            print(f"\n🌍 En Fazla Maç Olan Ülkeler:")
            for country in countries:
                print(f"   • {country[0]}: {country[1]:,} maç")
        
        # Sezon dağılımı
        cursor.execute("""
            SELECT sezon, COUNT(*) as mac_sayisi
            FROM hamdata 
            WHERE sezon IS NOT NULL AND sezon != ''
            GROUP BY sezon 
            ORDER BY mac_sayisi DESC 
            LIMIT 5
        """)
        seasons = cursor.fetchall()
        
        if seasons:
            print(f"\n📅 En Fazla Maç Olan Sezonlar:")
            for season in seasons:
                print(f"   • {season[0]}: {season[1]:,} maç")
        
        # Tarih aralığı
        cursor.execute("""
            SELECT MIN(tarih) as en_eski, MAX(tarih) as en_yeni
            FROM hamdata 
            WHERE tarih IS NOT NULL AND tarih != ''
        """)
        date_range = cursor.fetchone()
        
        if date_range is not None and date_range[0] and date_range[1]:
            print(f"\n📆 Tarih Aralığı: {date_range[0]} - {date_range[1]}")
        
        # Bahis oranları kontrolü
        cursor.execute("""
            SELECT 
                COUNT(*) as toplam,
                COUNT(CASE WHEN oran_1 IS NOT NULL AND oran_1 != '' THEN 1 END) as oran_1_count,
                COUNT(CASE WHEN oran_x IS NOT NULL AND oran_x != '' THEN 1 END) as oran_x_count,
                COUNT(CASE WHEN oran_2 IS NOT NULL AND oran_2 != '' THEN 1 END) as oran_2_count
            FROM hamdata
        """)
        odds_stats = cursor.fetchone()
        
        if odds_stats:
            print(f"\n💰 Bahis Oranları Dağılımı:")
            print(f"   • Toplam Maç: {odds_stats[0]:,}")
            print(f"   • Oran 1 Olan: {odds_stats[1]:,} (%{odds_stats[1]/odds_stats[0]*100:.1f})")
            print(f"   • Oran X Olan: {odds_stats[2]:,} (%{odds_stats[2]/odds_stats[0]*100:.1f})")
            print(f"   • Oran 2 Olan: {odds_stats[3]:,} (%{odds_stats[3]/odds_stats[0]*100:.1f})")
        
        cursor.close()
        pg_conn.close()
        
        print("\n✅ Analiz tamamlandı!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        print(f"Detay: {traceback.format_exc()}")

if __name__ == "__main__":
    analyze_hamdata()
