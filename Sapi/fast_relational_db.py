#!/usr/bin/env python3
"""
Hızlı İlişkisel Veritabanı Oluşturma - V1
Mevcut hamdata'dan hızlıca ilişkisel tablolar oluşturur
"""

import psycopg2
from psycopg2.extras import execute_values

def fast_create_relational():
    """Hamdata'dan hızlıca ilişkisel veritabanı oluştur"""
    
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
        
        print("⚡ HIZLI İLİŞKİSEL VERİTABANI OLUŞTURMA")
        print("="*50)
        
        # Hamdata kontrolü
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'hamdata'
            )
        """)
        hamdata_exists = cursor.fetchone()
        
        if not hamdata_exists or not hamdata_exists[0]:
            print("❌ Hamdata tablosu bulunamadı!")
            return
        
        cursor.execute("SELECT COUNT(*) FROM hamdata")
        hamdata_count = cursor.fetchone()
        total = hamdata_count[0] if hamdata_count else 0
        print(f"📊 Hamdata kayıt sayısı: {total:,}")
        
        if total == 0:
            print("⚠️ Hamdata boş!")
            return
        
        # Mevcut ilişkisel tabloları sil
        print("\n🗑️ Mevcut ilişkisel tablolar siliniyor...")
        tables_to_drop = ['betting_odds', 'team_seasons', 'matches', 'teams', 'seasons', 'leagues', 'countries']
        
        for table in tables_to_drop:
            cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
        
        print("✅ Eski tablolar silindi")
        
        # Yeni tabloları oluştur
        print("\n🏗️ Yeni tablolar oluşturuluyor...")
        
        # 1. Countries
        cursor.execute("""
            CREATE TABLE countries (
                ulke VARCHAR(100) PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 2. Leagues
        cursor.execute("""
            CREATE TABLE leagues (
                turnuva_id VARCHAR(50) PRIMARY KEY,
                turnuva_adi VARCHAR(150) NOT NULL,
                ulke VARCHAR(100) REFERENCES countries(ulke),
                turnuva_kodu VARCHAR(10),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 3. Seasons
        cursor.execute("""
            CREATE TABLE seasons (
                sezon_id VARCHAR(50) PRIMARY KEY,
                sezon VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 4. Teams
        cursor.execute("""
            CREATE TABLE teams (
                team_id VARCHAR(50) PRIMARY KEY,
                team_name VARCHAR(150) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 5. Matches
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 6. Team_Seasons
        cursor.execute("""
            CREATE TABLE team_seasons (
                team_season_id SERIAL PRIMARY KEY,
                team_id VARCHAR(50) REFERENCES teams(team_id),
                turnuva_id VARCHAR(50) REFERENCES leagues(turnuva_id),
                sezon_id VARCHAR(50) REFERENCES seasons(sezon_id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(team_id, turnuva_id, sezon_id)
            )
        """)
        
        # 7. Betting_Odds
        cursor.execute("""
            CREATE TABLE betting_odds (
                mac_id VARCHAR(50) PRIMARY KEY REFERENCES matches(mac_id),
                oran_1 DECIMAL(6,3),
                oran_x DECIMAL(6,3),
                oran_2 DECIMAL(6,3),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("✅ Tablolar oluşturuldu")
        
        # Hızlı veri transferi
        print("\n⚡ Hızlı veri transferi başlıyor...")
        
        # Countries
        print("   🌍 Countries...")
        cursor.execute("""
            INSERT INTO countries (ulke)
            SELECT DISTINCT ulke 
            FROM hamdata 
            WHERE ulke IS NOT NULL AND ulke != '' AND ulke != 'nan'
        """)
        countries_count = cursor.rowcount
        
        # Seasons
        print("   📅 Seasons...")
        cursor.execute("""
            INSERT INTO seasons (sezon_id, sezon)
            SELECT DISTINCT sezon_id, sezon 
            FROM hamdata 
            WHERE sezon_id IS NOT NULL AND sezon_id != '' AND sezon_id != 'nan'
            AND sezon IS NOT NULL AND sezon != '' AND sezon != 'nan'
        """)
        seasons_count = cursor.rowcount
        
        # Leagues
        print("   🏆 Leagues...")
        cursor.execute("""
            INSERT INTO leagues (turnuva_id, turnuva_adi, ulke, turnuva_kodu)
            SELECT DISTINCT 
                turnuva_id, 
                turnuva_adi, 
                CASE WHEN ulke = '' OR ulke = 'nan' THEN NULL ELSE ulke END,
                CASE WHEN turnuva_kodu = '' OR turnuva_kodu = 'nan' THEN NULL ELSE turnuva_kodu END
            FROM hamdata 
            WHERE turnuva_id IS NOT NULL AND turnuva_id != '' AND turnuva_id != 'nan'
            AND turnuva_adi IS NOT NULL AND turnuva_adi != '' AND turnuva_adi != 'nan'
        """)
        leagues_count = cursor.rowcount
        
        # Teams
        print("   ⚽ Teams...")
        cursor.execute("""
            WITH all_teams AS (
                SELECT DISTINCT ev_id as team_id, ev_sahibi_takim as team_name 
                FROM hamdata 
                WHERE ev_id IS NOT NULL AND ev_id != '' AND ev_id != 'nan'
                AND ev_sahibi_takim IS NOT NULL AND ev_sahibi_takim != '' AND ev_sahibi_takim != 'nan'
                UNION
                SELECT DISTINCT dep_id as team_id, deplasman_takim as team_name 
                FROM hamdata 
                WHERE dep_id IS NOT NULL AND dep_id != '' AND dep_id != 'nan'
                AND deplasman_takim IS NOT NULL AND deplasman_takim != '' AND deplasman_takim != 'nan'
            )
            INSERT INTO teams (team_id, team_name)
            SELECT team_id, team_name FROM all_teams
        """)
        teams_count = cursor.rowcount
        
        # Matches
        print("   🏈 Matches...")
        cursor.execute("""
            INSERT INTO matches (
                mac_id, turnuva_id, sezon_id, ev_id, dep_id,
                ev_sahibi_takim, deplasman_takim, tarih, saat, mac_durumu, skor,
                ev_skor, dep_skor
            )
            SELECT 
                mac_id,
                CASE WHEN turnuva_id = '' OR turnuva_id = 'nan' THEN NULL ELSE turnuva_id END,
                CASE WHEN sezon_id = '' OR sezon_id = 'nan' THEN NULL ELSE sezon_id END,
                CASE WHEN ev_id = '' OR ev_id = 'nan' THEN NULL ELSE ev_id END,
                CASE WHEN dep_id = '' OR dep_id = 'nan' THEN NULL ELSE dep_id END,
                ev_sahibi_takim,
                deplasman_takim,
                CASE WHEN tarih = '' OR tarih = 'nan' THEN NULL ELSE tarih END,
                CASE WHEN saat = '' OR saat = 'nan' THEN NULL ELSE saat END,
                CASE WHEN mac_durumu = '' OR mac_durumu = 'nan' THEN NULL ELSE mac_durumu END,
                CASE WHEN skor = '' OR skor = 'nan' THEN NULL ELSE skor END,
                CASE WHEN ev_skor = '' OR ev_skor = 'None' OR ev_skor = 'nan' THEN 0 
                     WHEN ev_skor ~ '^[0-9]+$' THEN CAST(ev_skor AS INTEGER) 
                     ELSE 0 END,
                CASE WHEN dep_skor = '' OR dep_skor = 'None' OR dep_skor = 'nan' THEN 0 
                     WHEN dep_skor ~ '^[0-9]+$' THEN CAST(dep_skor AS INTEGER) 
                     ELSE 0 END
            FROM hamdata
            WHERE mac_id IS NOT NULL AND mac_id != '' AND mac_id != 'nan'
        """)
        matches_count = cursor.rowcount
        
        # Team_Seasons
        print("   🔗 Team_Seasons...")
        cursor.execute("""
            WITH all_team_seasons AS (
                SELECT DISTINCT ev_id as team_id, turnuva_id, sezon_id 
                FROM hamdata 
                WHERE ev_id IS NOT NULL AND ev_id != '' AND ev_id != 'nan'
                AND turnuva_id IS NOT NULL AND turnuva_id != '' AND turnuva_id != 'nan'
                AND sezon_id IS NOT NULL AND sezon_id != '' AND sezon_id != 'nan'
                UNION
                SELECT DISTINCT dep_id as team_id, turnuva_id, sezon_id 
                FROM hamdata 
                WHERE dep_id IS NOT NULL AND dep_id != '' AND dep_id != 'nan'
                AND turnuva_id IS NOT NULL AND turnuva_id != '' AND turnuva_id != 'nan'
                AND sezon_id IS NOT NULL AND sezon_id != '' AND sezon_id != 'nan'
            )
            INSERT INTO team_seasons (team_id, turnuva_id, sezon_id)
            SELECT team_id, turnuva_id, sezon_id FROM all_team_seasons
        """)
        team_seasons_count = cursor.rowcount
        
        # Betting_Odds
        print("   💰 Betting_Odds...")
        cursor.execute("""
            INSERT INTO betting_odds (mac_id, oran_1, oran_x, oran_2)
            SELECT 
                mac_id,
                CASE WHEN oran_1 = '' OR oran_1 = 'None' OR oran_1 = 'nan' THEN NULL 
                     WHEN oran_1 ~ '^[0-9]+\.?[0-9]*$' THEN CAST(oran_1 AS DECIMAL) 
                     ELSE NULL END,
                CASE WHEN oran_x = '' OR oran_x = 'None' OR oran_x = 'nan' THEN NULL 
                     WHEN oran_x ~ r'^[0-9]+\.?[0-9]*$' THEN CAST(oran_x AS DECIMAL) 
                     ELSE NULL END,
                CASE WHEN oran_2 = '' OR oran_2 = 'None' OR oran_2 = 'nan' THEN NULL 
                     WHEN oran_2 ~ '^[0-9]+\.?[0-9]*$' THEN CAST(oran_2 AS DECIMAL) 
                     ELSE NULL END
            FROM hamdata
            WHERE mac_id IS NOT NULL AND mac_id != '' AND mac_id != 'nan'
            AND (
                (oran_1 IS NOT NULL AND oran_1 != '' AND oran_1 != 'None' AND oran_1 != 'nan')
                OR (oran_x IS NOT NULL AND oran_x != '' AND oran_x != 'None' AND oran_x != 'nan')
                OR (oran_2 IS NOT NULL AND oran_2 != '' AND oran_2 != 'None' AND oran_2 != 'nan')
            )
        """)
        betting_count = cursor.rowcount
        
        pg_conn.commit()
        
        # Sonuçları göster
        print(f"\n📊 HIZLI TRANSFER SONUÇLARI:")
        print("="*40)
        print(f"🌍 Countries: {countries_count:,}")
        print(f"🏆 Leagues: {leagues_count:,}")
        print(f"📅 Seasons: {seasons_count:,}")
        print(f"⚽ Teams: {teams_count:,}")
        print(f"🏈 Matches: {matches_count:,}")
        print(f"🔗 Team_Seasons: {team_seasons_count:,}")
        print(f"💰 Betting_Odds: {betting_count:,}")
        print("="*40)
        
        cursor.close()
        pg_conn.close()
        
        print("⚡ Hızlı ilişkisel veritabanı oluşturma tamamlandı!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        print(f"Detay: {traceback.format_exc()}")

if __name__ == "__main__":
    fast_create_relational()
