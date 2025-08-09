#!/usr/bin/env python3
"""
Komple Futbol Veritabanı Oluşturma Scripti
Sıfırdan API çekip ilişkisel veritabanı oluşturur
"""

import http.client
import pandas as pd
import json
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, timedelta

def create_complete_football_db():
    """Komple futbol veritabanını sıfırdan oluştur"""
    
    print("🚀 KOMPLE FUTBOL VERİTABANI OLUŞTURMA")
    print("="*60)
    print(f"🕒 Başlangıç: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    db_config = {
        "dbname": "soccerdb",
        "user": "ahmet21",
        "password": "diclem2121.",
        "host": "165.227.130.23",
        "port": "5432"
    }
    
    try:
        # Veritabanı bağlantısı
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
        
        # 1. Mevcut tabloları temizle
        print("\n🗑️ Mevcut tablolar temizleniyor...")
        tables_to_drop = [
            'betting_odds', 'team_seasons', 'matches', 
            'teams', 'seasons', 'leagues', 'countries', 'hamdata'
        ]
        
        for table in tables_to_drop:
            cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
        
        pg_conn.commit()
        print("✅ Mevcut tablolar silindi")
        
        # 2. API'den veri çek (son 5 gün)
        print("\n🌐 API'den veriler çekiliyor...")
        all_matches = []
        
        # Son 5 günün verilerini çek
        for i in range(5):
            date_to_fetch = datetime.now() - timedelta(days=i)
            date_str = date_to_fetch.strftime("%d/%m/%Y")
            
            try:
                print(f"   📅 {date_str} tarihi çekiliyor...")
                
                conn = http.client.HTTPSConnection('vd.mackolik.com')
                headers = {
                    'accept': '*/*',
                    'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
                    'origin': 'https://arsiv.mackolik.com',
                    'referer': 'https://arsiv.mackolik.com/',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                }
                
                conn.request('GET', f'/livedata?date={date_str}', headers=headers)
                response = conn.getresponse()
                
                if response.status == 200:
                    data = response.read()
                    json_data = json.loads(data).get("m", [])
                    
                    if json_data:
                        all_matches.extend(json_data)
                        print(f"      ✅ {len(json_data)} maç bulundu")
                    else:
                        print(f"      ⚠️ Veri bulunamadı")
                else:
                    print(f"      ❌ HTTP {response.status}")
                
                conn.close()
                
            except Exception as e:
                print(f"      ❌ Hata: {e}")
        
        if not all_matches:
            print("❌ Hiç veri çekilemedi!")
            return
        
        print(f"✅ Toplam {len(all_matches)} maç verisi çekildi")
        
        # 3. Hamdata tablosunu oluştur
        print("\n🏗️ Hamdata tablosu oluşturuluyor...")
        
        create_hamdata_query = """
            CREATE TABLE hamdata (
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
        cursor.execute(create_hamdata_query)
        print("✅ Hamdata tablosu oluşturuldu")
        
        # 4. API verilerini hamdata formatına dönüştür
        print("\n🔄 API verileri işleniyor...")
        
        processed_data = []
        for row in all_matches:
            try:
                # Turnuva bilgilerini ayrıştır
                turnuva_raw = row[36] if len(row) > 36 else []
                turnuva_info = turnuva_raw if isinstance(turnuva_raw, list) else []
                
                turnuva_kategori_id = str(turnuva_info[0]) if len(turnuva_info) > 0 else ''
                turnuva_kategorisi = str(turnuva_info[1]) if len(turnuva_info) > 1 else ''
                turnuva_id = str(turnuva_info[2]) if len(turnuva_info) > 2 else ''
                turnuva_adi = str(turnuva_info[3]) if len(turnuva_info) > 3 else ''
                sezon_id = str(turnuva_info[4]) if len(turnuva_info) > 4 else ''
                sezon = str(turnuva_info[5]) if len(turnuva_info) > 5 else ''
                turnuva_kodu = str(turnuva_info[9]) if len(turnuva_info) > 9 else ''
                
                # Hamdata formatında satır oluştur
                processed_row = [
                    str(row[0]),  # mac_id
                    str(row[1]),  # ev_id
                    str(row[2]),  # ev_sahibi_takim
                    str(row[3]),  # dep_id
                    str(row[4]),  # deplasman_takim
                    str(row[5]),  # kriter_id
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
                processed_data.append(processed_row)
                
            except Exception as e:
                print(f"      ⚠️ Satır işleme hatası: {e}")
        
        # 5. Hamdata'ya veri ekle
        if processed_data:
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
                """,
                processed_data,
                page_size=100
            )
            
            pg_conn.commit()
            print(f"✅ {len(processed_data)} kayıt hamdata'ya eklendi")
        
        # 6. İlişkisel tabloları oluştur
        print("\n🔗 İlişkisel tablolar oluşturuluyor...")
        
        # Countries
        cursor.execute("""
            CREATE TABLE countries (
                ulke VARCHAR(100) PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Leagues
        cursor.execute("""
            CREATE TABLE leagues (
                turnuva_id VARCHAR(50) PRIMARY KEY,
                turnuva_adi VARCHAR(150) NOT NULL,
                ulke VARCHAR(100) REFERENCES countries(ulke),
                turnuva_kodu VARCHAR(10),
                turnuva_kategori_id VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Seasons
        cursor.execute("""
            CREATE TABLE seasons (
                sezon_id VARCHAR(50) PRIMARY KEY,
                sezon VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Teams
        cursor.execute("""
            CREATE TABLE teams (
                team_id VARCHAR(50) PRIMARY KEY,
                team_name VARCHAR(150) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Team_Seasons
        cursor.execute("""
            CREATE TABLE team_seasons (
                team_season_id SERIAL PRIMARY KEY,
                team_id VARCHAR(50) REFERENCES teams(team_id),
                turnuva_id VARCHAR(50) REFERENCES leagues(turnuva_id),
                sezon_id VARCHAR(50) REFERENCES seasons(sezon_id),
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(team_id, turnuva_id, sezon_id)
            )
        """)
        
        # Matches
        cursor.execute("""
            CREATE TABLE matches (
                mac_id VARCHAR(50) PRIMARY KEY,
                turnuva_id VARCHAR(50) REFERENCES leagues(turnuva_id),
                sezon_id VARCHAR(50) REFERENCES seasons(sezon_id),
                ev_id VARCHAR(50),
                dep_id VARCHAR(50),
                ev_sahibi_takim VARCHAR(150),
                deplasman_takim VARCHAR(150),
                tarih VARCHAR(20),
                saat VARCHAR(10),
                mac_durumu VARCHAR(20),
                skor VARCHAR(20),
                ev_skor INTEGER DEFAULT 0,
                dep_skor INTEGER DEFAULT 0,
                iy_ev_skor INTEGER DEFAULT 0,
                iy_dep_skor INTEGER DEFAULT 0,
                kategori VARCHAR(10),
                istatistik_7 VARCHAR(50),
                kriter_id VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Betting_Odds
        cursor.execute("""
            CREATE TABLE betting_odds (
                mac_id VARCHAR(50) PRIMARY KEY REFERENCES matches(mac_id),
                oran_1 DECIMAL(6,3),
                oran_x DECIMAL(6,3),
                oran_2 DECIMAL(6,3),
                oran_alt DECIMAL(6,3),
                oran_ust DECIMAL(6,3),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("✅ İlişkisel tablolar oluşturuldu")
        
        # 7. Hamdata'dan ilişkisel tablolara veri aktar
        print("\n🔄 İlişkisel tablolara veri aktarılıyor...")
        
        # Countries
        cursor.execute("""
            INSERT INTO countries (ulke)
            SELECT DISTINCT ulke 
            FROM hamdata 
            WHERE ulke IS NOT NULL AND ulke != ''
        """)
        countries_count = cursor.rowcount
        print(f"   ✅ {countries_count} ülke eklendi")
        
        # Seasons
        cursor.execute("""
            INSERT INTO seasons (sezon_id, sezon)
            SELECT DISTINCT sezon_id, sezon 
            FROM hamdata 
            WHERE sezon_id IS NOT NULL AND sezon_id != ''
        """)
        seasons_count = cursor.rowcount
        print(f"   ✅ {seasons_count} sezon eklendi")
        
        # Leagues
        cursor.execute("""
            INSERT INTO leagues (turnuva_id, turnuva_adi, ulke, turnuva_kodu, turnuva_kategori_id)
            SELECT DISTINCT 
                turnuva_id, 
                turnuva_adi, 
                CASE WHEN ulke = '' THEN NULL ELSE ulke END,
                CASE WHEN turnuva_kodu = '' THEN NULL ELSE turnuva_kodu END,
                CASE WHEN turnuva_kategori_id = '' THEN NULL ELSE turnuva_kategori_id END
            FROM hamdata 
            WHERE turnuva_id IS NOT NULL AND turnuva_id != ''
        """)
        leagues_count = cursor.rowcount
        print(f"   ✅ {leagues_count} lig eklendi")
        
        # Teams (Ev sahibi + Deplasman)
        cursor.execute("""
            INSERT INTO teams (team_id, team_name)
            SELECT DISTINCT ev_id, ev_sahibi_takim 
            FROM hamdata 
            WHERE ev_id IS NOT NULL AND ev_id != ''
            UNION
            SELECT DISTINCT dep_id, deplasman_takim 
            FROM hamdata 
            WHERE dep_id IS NOT NULL AND dep_id != ''
        """)
        teams_count = cursor.rowcount
        print(f"   ✅ {teams_count} takım eklendi")
        
        # Matches
        cursor.execute("""
            INSERT INTO matches (
                mac_id, turnuva_id, sezon_id, ev_id, dep_id,
                ev_sahibi_takim, deplasman_takim, tarih, saat, mac_durumu,
                skor, ev_skor, dep_skor, iy_ev_skor, iy_dep_skor,
                kategori, istatistik_7, kriter_id
            )
            SELECT 
                mac_id,
                CASE WHEN turnuva_id = '' THEN NULL ELSE turnuva_id END,
                CASE WHEN sezon_id = '' THEN NULL ELSE sezon_id END,
                CASE WHEN ev_id = '' THEN NULL ELSE ev_id END,
                CASE WHEN dep_id = '' THEN NULL ELSE dep_id END,
                ev_sahibi_takim,
                deplasman_takim,
                CASE WHEN tarih = '' THEN NULL ELSE tarih END,
                CASE WHEN saat = '' THEN NULL ELSE saat END,
                CASE WHEN mac_durumu = '' THEN NULL ELSE mac_durumu END,
                CASE WHEN skor = '' THEN NULL ELSE skor END,
                CASE WHEN ev_skor = '' OR ev_skor = 'None' THEN 0 ELSE CAST(ev_skor AS INTEGER) END,
                CASE WHEN dep_skor = '' OR dep_skor = 'None' THEN 0 ELSE CAST(dep_skor AS INTEGER) END,
                CASE WHEN iy_ev_skor = '' OR iy_ev_skor = 'None' THEN 0 ELSE CAST(iy_ev_skor AS INTEGER) END,
                CASE WHEN iy_dep_skor = '' OR iy_dep_skor = 'None' THEN 0 ELSE CAST(iy_dep_skor AS INTEGER) END,
                CASE WHEN kategori = '' THEN NULL ELSE kategori END,
                CASE WHEN istatistik_7 = '' THEN NULL ELSE istatistik_7 END,
                CASE WHEN kriter_id = '' THEN NULL ELSE kriter_id END
            FROM hamdata
        """)
        matches_count = cursor.rowcount
        print(f"   ✅ {matches_count} maç eklendi")
        
        # Team_Seasons
        cursor.execute("""
            INSERT INTO team_seasons (team_id, turnuva_id, sezon_id)
            SELECT DISTINCT ev_id, turnuva_id, sezon_id 
            FROM hamdata 
            WHERE ev_id IS NOT NULL AND ev_id != '' 
            AND turnuva_id IS NOT NULL AND turnuva_id != ''
            AND sezon_id IS NOT NULL AND sezon_id != ''
            UNION
            SELECT DISTINCT dep_id, turnuva_id, sezon_id 
            FROM hamdata 
            WHERE dep_id IS NOT NULL AND dep_id != ''
            AND turnuva_id IS NOT NULL AND turnuva_id != ''
            AND sezon_id IS NOT NULL AND sezon_id != ''
        """)
        team_seasons_count = cursor.rowcount
        print(f"   ✅ {team_seasons_count} takım-sezon ilişkisi eklendi")
        
        # Betting_Odds
        cursor.execute("""
            INSERT INTO betting_odds (mac_id, oran_1, oran_x, oran_2, oran_alt, oran_ust)
            SELECT 
                mac_id,
                CASE WHEN oran_1 = '' OR oran_1 = 'None' THEN NULL ELSE CAST(oran_1 AS DECIMAL) END,
                CASE WHEN oran_x = '' OR oran_x = 'None' THEN NULL ELSE CAST(oran_x AS DECIMAL) END,
                CASE WHEN oran_2 = '' OR oran_2 = 'None' THEN NULL ELSE CAST(oran_2 AS DECIMAL) END,
                CASE WHEN oran_alt = '' OR oran_alt = 'None' THEN NULL ELSE CAST(oran_alt AS DECIMAL) END,
                CASE WHEN oran_ust = '' OR oran_ust = 'None' THEN NULL ELSE CAST(oran_ust AS DECIMAL) END
            FROM hamdata
            WHERE (oran_1 IS NOT NULL AND oran_1 != '' AND oran_1 != 'None')
            OR (oran_x IS NOT NULL AND oran_x != '' AND oran_x != 'None')
            OR (oran_2 IS NOT NULL AND oran_2 != '' AND oran_2 != 'None')
            OR (oran_alt IS NOT NULL AND oran_alt != '' AND oran_alt != 'None')
            OR (oran_ust IS NOT NULL AND oran_ust != '' AND oran_ust != 'None')
        """)
        betting_count = cursor.rowcount
        print(f"   ✅ {betting_count} bahis oranı eklendi")
        
        pg_conn.commit()
        
        # 8. Final istatistikler
        print(f"\n📊 KOMPLE VERİTABANI İSTATİSTİKLERİ:")
        print("="*50)
        print(f"🗃️ Hamdata: {len(processed_data):,} kayıt")
        print(f"🌍 Countries: {countries_count:,} ülke")
        print(f"🏆 Leagues: {leagues_count:,} lig")
        print(f"📅 Seasons: {seasons_count:,} sezon")
        print(f"⚽ Teams: {teams_count:,} takım")
        print(f"🔗 Team_Seasons: {team_seasons_count:,} ilişki")
        print(f"🏈 Matches: {matches_count:,} maç")
        print(f"💰 Betting_Odds: {betting_count:,} oran")
        print("="*50)
        
        cursor.close()
        pg_conn.close()
        
        print(f"🕒 Bitiş: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎉 KOMPLE FUTBOL VERİTABANI BAŞARIYLA OLUŞTURULDU!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        print(f"Detay: {traceback.format_exc()}")

if __name__ == "__main__":
    create_complete_football_db()
