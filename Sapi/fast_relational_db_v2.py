#!/usr/bin/env python3
"""
Hızlı İlişkisel Veritabanı Oluşturma - V2
Optimized version with better error handling
"""

import psycopg2
from psycopg2.extras import execute_values

def fast_create_relational_v2():
    """Hamdata'dan hızlıca ilişkisel veritabanı oluştur - V2"""
    
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
        
        print("⚡ HIZLI İLİŞKİSEL VERİTABANI V2")
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
        
        # Optimized table creation
        print("\n🏗️ Optimize edilmiş tablolar oluşturuluyor...")
        
        # 1. Countries
        cursor.execute("""
            CREATE TABLE countries (
                ulke VARCHAR(100) PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX idx_countries_ulke ON countries(ulke);
        """)
        
        # 2. Seasons  
        cursor.execute("""
            CREATE TABLE seasons (
                sezon_id VARCHAR(50) PRIMARY KEY,
                sezon VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX idx_seasons_sezon ON seasons(sezon);
        """)
        
        # 3. Leagues
        cursor.execute("""
            CREATE TABLE leagues (
                turnuva_id VARCHAR(50) PRIMARY KEY,
                turnuva_adi VARCHAR(150) NOT NULL,
                ulke VARCHAR(100) REFERENCES countries(ulke),
                turnuva_kodu VARCHAR(10),
                turnuva_kategori_id VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX idx_leagues_adi ON leagues(turnuva_adi);
            CREATE INDEX idx_leagues_ulke ON leagues(ulke);
        """)
        
        # 4. Teams
        cursor.execute("""
            CREATE TABLE teams (
                team_id VARCHAR(50) PRIMARY KEY,
                team_name VARCHAR(150) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX idx_teams_name ON teams(team_name);
        """)
        
        # 5. Matches (Simplified)
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX idx_matches_tarih ON matches(tarih);
            CREATE INDEX idx_matches_turnuva ON matches(turnuva_id);
            CREATE INDEX idx_matches_sezon ON matches(sezon_id);
        """)
        
        # 6. Team_Seasons
        cursor.execute("""
            CREATE TABLE team_seasons (
                team_season_id SERIAL PRIMARY KEY,
                team_id VARCHAR(50) REFERENCES teams(team_id),
                turnuva_id VARCHAR(50) REFERENCES leagues(turnuva_id),
                sezon_id VARCHAR(50) REFERENCES seasons(sezon_id),
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(team_id, turnuva_id, sezon_id)
            );
            CREATE INDEX idx_team_seasons_lookup ON team_seasons(team_id, turnuva_id, sezon_id);
        """)
        
        # 7. Betting_Odds (Simplified)
        cursor.execute("""
            CREATE TABLE betting_odds (
                mac_id VARCHAR(50) PRIMARY KEY REFERENCES matches(mac_id),
                oran_1 DECIMAL(6,3),
                oran_x DECIMAL(6,3),
                oran_2 DECIMAL(6,3),
                oran_alt DECIMAL(6,3),
                oran_ust DECIMAL(6,3),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        print("✅ Optimize edilmiş tablolar oluşturuldu")
        
        # Ultra-fast bulk data transfer
        print("\n⚡ Ultra hızlı bulk veri transferi...")
        
        # 1. Countries - Direct insert
        print("   🌍 Countries...")
        cursor.execute("""
            INSERT INTO countries (ulke)
            SELECT DISTINCT ulke 
            FROM hamdata 
            WHERE ulke IS NOT NULL 
            AND ulke != '' 
            AND ulke != 'nan' 
            AND ulke != 'None'
        """)
        countries_count = cursor.rowcount
        
        # 2. Seasons - Direct insert
        print("   📅 Seasons...")
        cursor.execute("""
            INSERT INTO seasons (sezon_id, sezon)
            SELECT DISTINCT sezon_id, sezon 
            FROM hamdata 
            WHERE sezon_id IS NOT NULL 
            AND sezon_id != '' 
            AND sezon_id != 'nan' 
            AND sezon_id != 'None'
            AND sezon IS NOT NULL 
            AND sezon != '' 
            AND sezon != 'nan' 
            AND sezon != 'None'
        """)
        seasons_count = cursor.rowcount
        
        # 3. Leagues - Direct insert
        print("   🏆 Leagues...")
        cursor.execute("""
            INSERT INTO leagues (turnuva_id, turnuva_adi, ulke, turnuva_kodu, turnuva_kategori_id)
            SELECT DISTINCT 
                turnuva_id, 
                turnuva_adi, 
                NULLIF(NULLIF(NULLIF(ulke, ''), 'nan'), 'None'),
                NULLIF(NULLIF(NULLIF(turnuva_kodu, ''), 'nan'), 'None'),
                NULLIF(NULLIF(NULLIF(turnuva_kategori_id, ''), 'nan'), 'None')
            FROM hamdata 
            WHERE turnuva_id IS NOT NULL 
            AND turnuva_id != '' 
            AND turnuva_id != 'nan' 
            AND turnuva_id != 'None'
            AND turnuva_adi IS NOT NULL 
            AND turnuva_adi != '' 
            AND turnuva_adi != 'nan' 
            AND turnuva_adi != 'None'
        """)
        leagues_count = cursor.rowcount
        
        # 4. Teams - Union approach for performance
        print("   ⚽ Teams...")
        cursor.execute("""
            WITH all_teams AS (
                SELECT ev_id as team_id, ev_sahibi_takim as team_name 
                FROM hamdata 
                WHERE ev_id IS NOT NULL 
                AND ev_id != '' 
                AND ev_id != 'nan' 
                AND ev_id != 'None'
                AND ev_sahibi_takim IS NOT NULL 
                AND ev_sahibi_takim != '' 
                AND ev_sahibi_takim != 'nan' 
                AND ev_sahibi_takim != 'None'
                UNION
                SELECT dep_id as team_id, deplasman_takim as team_name 
                FROM hamdata 
                WHERE dep_id IS NOT NULL 
                AND dep_id != '' 
                AND dep_id != 'nan' 
                AND dep_id != 'None'
                AND deplasman_takim IS NOT NULL 
                AND deplasman_takim != '' 
                AND deplasman_takim != 'nan' 
                AND deplasman_takim != 'None'
            )
            INSERT INTO teams (team_id, team_name)
            SELECT DISTINCT team_id, team_name FROM all_teams
        """)
        teams_count = cursor.rowcount
        
        # 5. Matches - Optimized with safe casting
        print("   🏈 Matches...")
        cursor.execute("""
            INSERT INTO matches (
                mac_id, turnuva_id, sezon_id, ev_id, dep_id,
                ev_sahibi_takim, deplasman_takim, tarih, saat, 
                mac_durumu, skor, ev_skor, dep_skor, iy_ev_skor, iy_dep_skor, kategori
            )
            SELECT 
                mac_id,
                NULLIF(NULLIF(NULLIF(turnuva_id, ''), 'nan'), 'None'),
                NULLIF(NULLIF(NULLIF(sezon_id, ''), 'nan'), 'None'),
                NULLIF(NULLIF(NULLIF(ev_id, ''), 'nan'), 'None'),
                NULLIF(NULLIF(NULLIF(dep_id, ''), 'nan'), 'None'),
                NULLIF(NULLIF(NULLIF(ev_sahibi_takim, ''), 'nan'), 'None'),
                NULLIF(NULLIF(NULLIF(deplasman_takim, ''), 'nan'), 'None'),
                NULLIF(NULLIF(NULLIF(tarih, ''), 'nan'), 'None'),
                NULLIF(NULLIF(NULLIF(saat, ''), 'nan'), 'None'),
                NULLIF(NULLIF(NULLIF(mac_durumu, ''), 'nan'), 'None'),
                NULLIF(NULLIF(NULLIF(skor, ''), 'nan'), 'None'),
                CASE 
                    WHEN ev_skor ~ '^[0-9]+$' THEN CAST(ev_skor AS INTEGER) 
                    ELSE 0 
                END,
                CASE 
                    WHEN dep_skor ~ '^[0-9]+$' THEN CAST(dep_skor AS INTEGER) 
                    ELSE 0 
                END,
                CASE 
                    WHEN iy_ev_skor ~ '^[0-9]+$' THEN CAST(iy_ev_skor AS INTEGER) 
                    ELSE 0 
                END,
                CASE 
                    WHEN iy_dep_skor ~ '^[0-9]+$' THEN CAST(iy_dep_skor AS INTEGER) 
                    ELSE 0 
                END,
                NULLIF(NULLIF(NULLIF(kategori, ''), 'nan'), 'None')
            FROM hamdata
            WHERE mac_id IS NOT NULL 
            AND mac_id != '' 
            AND mac_id != 'nan' 
            AND mac_id != 'None'
        """)
        matches_count = cursor.rowcount
        
        # 6. Team_Seasons - Optimized relationship mapping
        print("   🔗 Team_Seasons...")
        cursor.execute("""
            WITH all_team_seasons AS (
                SELECT ev_id as team_id, turnuva_id, sezon_id 
                FROM hamdata 
                WHERE ev_id IS NOT NULL AND ev_id != '' AND ev_id != 'nan' AND ev_id != 'None'
                AND turnuva_id IS NOT NULL AND turnuva_id != '' AND turnuva_id != 'nan' AND turnuva_id != 'None'
                AND sezon_id IS NOT NULL AND sezon_id != '' AND sezon_id != 'nan' AND sezon_id != 'None'
                UNION
                SELECT dep_id as team_id, turnuva_id, sezon_id 
                FROM hamdata 
                WHERE dep_id IS NOT NULL AND dep_id != '' AND dep_id != 'nan' AND dep_id != 'None'
                AND turnuva_id IS NOT NULL AND turnuva_id != '' AND turnuva_id != 'nan' AND turnuva_id != 'None'
                AND sezon_id IS NOT NULL AND sezon_id != '' AND sezon_id != 'nan' AND sezon_id != 'None'
            )
            INSERT INTO team_seasons (team_id, turnuva_id, sezon_id)
            SELECT DISTINCT team_id, turnuva_id, sezon_id FROM all_team_seasons
        """)
        team_seasons_count = cursor.rowcount
        
        # 7. Betting_Odds - Safe decimal conversion
        print("   💰 Betting_Odds...")
        cursor.execute("""
            INSERT INTO betting_odds (mac_id, oran_1, oran_x, oran_2, oran_alt, oran_ust)
            SELECT 
                mac_id,
                CASE 
                    WHEN oran_1 ~ '^[0-9]+\\.?[0-9]*$' THEN CAST(oran_1 AS DECIMAL) 
                    ELSE NULL 
                END,
                CASE 
                    WHEN oran_x ~ '^[0-9]+\\.?[0-9]*$' THEN CAST(oran_x AS DECIMAL) 
                    ELSE NULL 
                END,
                CASE 
                    WHEN oran_2 ~ '^[0-9]+\\.?[0-9]*$' THEN CAST(oran_2 AS DECIMAL) 
                    ELSE NULL 
                END,
                CASE 
                    WHEN oran_alt ~ '^[0-9]+\\.?[0-9]*$' THEN CAST(oran_alt AS DECIMAL) 
                    ELSE NULL 
                END,
                CASE 
                    WHEN oran_ust ~ '^[0-9]+\\.?[0-9]*$' THEN CAST(oran_ust AS DECIMAL) 
                    ELSE NULL 
                END
            FROM hamdata
            WHERE mac_id IS NOT NULL AND mac_id != '' AND mac_id != 'nan' AND mac_id != 'None'
            AND (
                (oran_1 IS NOT NULL AND oran_1 ~ '^[0-9]+\\.?[0-9]*$')
                OR (oran_x IS NOT NULL AND oran_x ~ '^[0-9]+\\.?[0-9]*$')
                OR (oran_2 IS NOT NULL AND oran_2 ~ '^[0-9]+\\.?[0-9]*$')
                OR (oran_alt IS NOT NULL AND oran_alt ~ '^[0-9]+\\.?[0-9]*$')
                OR (oran_ust IS NOT NULL AND oran_ust ~ '^[0-9]+\\.?[0-9]*$')
            )
        """)
        betting_count = cursor.rowcount
        
        pg_conn.commit()
        
        # Performance statistics
        print(f"\n📊 ULTRA HIZLI TRANSFER SONUÇLARI:")
        print("="*50)
        print(f"🗃️ Kaynak Hamdata: {total:,} kayıt")
        print(f"🌍 Countries: {countries_count:,}")
        print(f"🏆 Leagues: {leagues_count:,}")
        print(f"📅 Seasons: {seasons_count:,}")
        print(f"⚽ Teams: {teams_count:,}")
        print(f"🏈 Matches: {matches_count:,}")
        print(f"🔗 Team_Seasons: {team_seasons_count:,}")
        print(f"💰 Betting_Odds: {betting_count:,}")
        print("="*50)
        
        # Data integrity check
        print(f"\n🔍 VERİ BÜTÜNLÜK KONTROLÜ:")
        
        # Check foreign keys
        cursor.execute("""
            SELECT COUNT(*) as total,
                   COUNT(CASE WHEN turnuva_id IS NOT NULL THEN 1 END) as with_league,
                   COUNT(CASE WHEN sezon_id IS NOT NULL THEN 1 END) as with_season
            FROM matches
        """)
        integrity_stats = cursor.fetchone()
        if integrity_stats:
            print(f"   📊 Maçlar: {integrity_stats[0]:,} toplam")
            print(f"   🏆 Lig bağlantılı: {integrity_stats[1]:,} (%{integrity_stats[1]/integrity_stats[0]*100:.1f})")
            print(f"   📅 Sezon bağlantılı: {integrity_stats[2]:,} (%{integrity_stats[2]/integrity_stats[0]*100:.1f})")
        
        cursor.close()
        pg_conn.close()
        
        print("\n⚡ Ultra hızlı V2 veritabanı oluşturma tamamlandı!")
        print("🚀 Optimize edilmiş indeksler ve foreign key'ler hazır!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        print(f"Detay: {traceback.format_exc()}")

if __name__ == "__main__":
    fast_create_relational_v2()
