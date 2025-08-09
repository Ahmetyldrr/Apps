#!/usr/bin/env python3
"""
Sezon Verileri Kontrol Scripti
"""

import psycopg2
from collections import Counter

def check_seasons():
    """Sezon verilerini detaylı kontrol et"""
    
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
        
        print("📅 SEZON VERİLERİ KONTROL RAPORU")
        print("="*60)
        
        # Hamdata tablosunda sezon kontrolü
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'hamdata'
            )
        """)
        hamdata_exists = cursor.fetchone()
        
        if hamdata_exists and hamdata_exists[0]:
            print("✅ Hamdata tablosu bulundu")
            
            # Toplam kayıt sayısı
            cursor.execute("SELECT COUNT(*) FROM hamdata")
            total_count = cursor.fetchone()
            total = total_count[0] if total_count else 0
            print(f"📊 Toplam Hamdata Kayıt: {total:,}")
            
            # Unique sezonlar
            cursor.execute("""
                SELECT 
                    sezon,
                    sezon_id,
                    COUNT(*) as mac_sayisi
                FROM hamdata 
                WHERE sezon IS NOT NULL AND sezon != ''
                GROUP BY sezon, sezon_id
                ORDER BY mac_sayisi DESC
            """)
            seasons = cursor.fetchall()
            
            print(f"\n📋 HAMDATA'DA BULUNAN SEZONLAR ({len(seasons)} unique):")
            print("-" * 60)
            
            for i, season in enumerate(seasons, 1):
                sezon_adi = season[0] if season[0] else "Bilinmiyor"
                sezon_id = season[1] if season[1] else "Bilinmiyor"
                mac_sayisi = season[2]
                oran = (mac_sayisi / total) * 100
                
                print(f"{i:2d}. {sezon_adi} (ID: {sezon_id})")
                print(f"     Maç Sayısı: {mac_sayisi:,} (%{oran:.1f})")
                
                if i <= 10:  # İlk 10 sezonu detaylı göster
                    # Bu sezondaki turnuvalar
                    cursor.execute("""
                        SELECT turnuva_adi, COUNT(*) as mac_sayisi
                        FROM hamdata 
                        WHERE sezon_id = %s AND turnuva_adi IS NOT NULL
                        GROUP BY turnuva_adi
                        ORDER BY mac_sayisi DESC
                        LIMIT 3
                    """, (sezon_id,))
                    tournaments = cursor.fetchall()
                    
                    if tournaments:
                        print(f"     Top Turnuvalar:")
                        for tournament in tournaments:
                            print(f"       • {tournament[0]}: {tournament[1]} maç")
                print()
        else:
            print("❌ Hamdata tablosu bulunamadı!")
        
        # İlişkisel seasons tablosu kontrolü
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'seasons'
            )
        """)
        seasons_table_exists = cursor.fetchone()
        
        if seasons_table_exists and seasons_table_exists[0]:
            print("🔗 İLİŞKİSEL SEASONS TABLOSU:")
            print("-" * 40)
            
            cursor.execute("SELECT COUNT(*) FROM seasons")
            seasons_count = cursor.fetchone()
            seasons_total = seasons_count[0] if seasons_count else 0
            print(f"📊 Toplam Seasons Kayıt: {seasons_total:,}")
            
            # Seasons tablosundaki veriler
            cursor.execute("""
                SELECT sezon_id, sezon, created_at
                FROM seasons 
                ORDER BY sezon
            """)
            seasons_data = cursor.fetchall()
            
            if seasons_data:
                print(f"\n📋 SEASONS TABLOSU İÇERİĞİ:")
                for season in seasons_data:
                    sezon_id = season[0]
                    sezon_adi = season[1]
                    created_at = season[2]
                    
                    # Bu sezonda kaç maç var (matches tablosundan)
                    cursor.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_name = 'matches'
                        )
                    """)
                    matches_exists = cursor.fetchone()
                    
                    if matches_exists and matches_exists[0]:
                        cursor.execute("""
                            SELECT COUNT(*) 
                            FROM matches 
                            WHERE sezon_id = %s
                        """, (sezon_id,))
                        match_count = cursor.fetchone()
                        match_total = match_count[0] if match_count else 0
                        print(f"   • {sezon_adi} (ID: {sezon_id})")
                        print(f"     Matches'de: {match_total:,} maç")
                        print(f"     Oluşturulma: {created_at}")
                    else:
                        print(f"   • {sezon_adi} (ID: {sezon_id}) - Matches tablosu yok")
                    print()
        else:
            print("❌ İlişkisel seasons tablosu bulunamadı!")
        
        # Sezon format analizi
        if hamdata_exists and hamdata_exists[0]:
            print("🔍 SEZON FORMAT ANALİZİ:")
            print("-" * 30)
            
            cursor.execute("""
                SELECT DISTINCT sezon
                FROM hamdata 
                WHERE sezon IS NOT NULL AND sezon != ''
                ORDER BY sezon
            """)
            season_formats = cursor.fetchall()
            
            # Sezon formatlarını kategorize et
            formats = {
                'YYYY/YY': [],      # 2023/24
                'YYYY-YY': [],      # 2023-24
                'YYYY/YYYY': [],    # 2023/2024
                'YYYY-YYYY': [],    # 2023-2024
                'OTHER': []         # Diğer formatlar
            }
            
            for season_tuple in season_formats:
                season = season_tuple[0]
                
                if '/' in season and len(season) == 7:  # 2023/24
                    formats['YYYY/YY'].append(season)
                elif '-' in season and len(season) == 7:  # 2023-24
                    formats['YYYY-YY'].append(season)
                elif '/' in season and len(season) == 9:  # 2023/2024
                    formats['YYYY/YYYY'].append(season)
                elif '-' in season and len(season) == 9:  # 2023-2024
                    formats['YYYY-YYYY'].append(season)
                else:
                    formats['OTHER'].append(season)
            
            for format_name, seasons_list in formats.items():
                if seasons_list:
                    print(f"📊 {format_name} Formatı: {len(seasons_list)} sezon")
                    # İlk birkaç örnek göster
                    examples = seasons_list[:5]
                    print(f"   Örnekler: {', '.join(examples)}")
                    if len(seasons_list) > 5:
                        print(f"   ... ve {len(seasons_list) - 5} sezon daha")
                    print()
        
        cursor.close()
        pg_conn.close()
        
        print("="*60)
        print("✅ Sezon kontrolü tamamlandı!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        print(f"Detay: {traceback.format_exc()}")

if __name__ == "__main__":
    check_seasons()
