#!/usr/bin/env python3
"""
Basitleştirilmiş İlişkisel Futbol Veritabanı - V3
- External ID'ler kaldırıldı, hamdata'daki orijinal ID'ler kullanılıyor
- Sütun isimleri birebir hamdata ile uyumlu
- Gereksiz sütunlar kaldırıldı
"""

import psycopg2
import pandas as pd
import requests
import json
from datetime import datetime
from psycopg2.extras import execute_values
import re
import warnings
warnings.filterwarnings('ignore')

def get_match_data():
    """API'den maç verilerini çek"""
    try:
        url = "https://www.mackolik.com/api/live/all"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            matches_data = []
            for match in data:
                matches_data.append({
                    'mac_id': match.get('id', ''),
                    'turnuva_adi': match.get('category', {}).get('tournament', {}).get('name', ''),
                    'turnuva_id': match.get('category', {}).get('tournament', {}).get('id', ''),
                    'ulke': match.get('category', {}).get('country', {}).get('name', ''),
                    'sezon': match.get('category', {}).get('tournament', {}).get('season', ''),
                    'sezon_id': match.get('category', {}).get('tournament', {}).get('seasonId', ''),
                    'ev_sahibi_takim': match.get('home', {}).get('name', ''),
                    'ev_id': match.get('home', {}).get('id', ''),
                    'deplasman_takim': match.get('away', {}).get('name', ''),
                    'dep_id': match.get('away', {}).get('id', ''),
                    'tarih': match.get('date', ''),
                    'saat': match.get('time', ''),
                    'mac_durumu': match.get('status', ''),
                    'ev_skor': match.get('score', {}).get('home', 0),
                    'dep_skor': match.get('score', {}).get('away', 0),
                    'iy_ev_skor': match.get('score', {}).get('ht', {}).get('home', 0),
                    'iy_dep_skor': match.get('score', {}).get('ht', {}).get('away', 0),
                })
            
            df = pd.DataFrame(matches_data)
            return df
            
    except Exception as e:
        print(f"❌ API hatası: {e}")
        return None

def create_simple_schema(cursor):
    """Basitleştirilmiş veritabanı şeması oluştur - hamdata sütun isimleriyle"""
    
    print("🗑️ Mevcut ilişkisel tablolar siliniyor...")
    
    # Önce tüm tabloları sil
    cursor.execute("DROP TABLE IF EXISTS betting_odds CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS matches CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS team_seasons CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS teams CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS seasons CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS leagues CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS countries CASCADE;")
    
    print("✅ Eski tablolar silindi")
    print("🏗️ Basitleştirilmiş tablolar oluşturuluyor...")
    
    # 1. Countries (hamdata'daki ulke sütunu)
    cursor.execute("""
        CREATE TABLE countries (
            ulke VARCHAR(100) PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # 2. Leagues (hamdata'daki turnuva_id, turnuva_adi, ulke)
    cursor.execute("""
        CREATE TABLE leagues (
            turnuva_id VARCHAR(50) PRIMARY KEY,
            turnuva_adi VARCHAR(150) NOT NULL,
            ulke VARCHAR(100) REFERENCES countries(ulke) ON DELETE SET NULL,
            turnuva_kodu VARCHAR(10),
            turnuva_kategori_id VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # 3. Seasons (hamdata'daki sezon_id, sezon)
    cursor.execute("""
        CREATE TABLE seasons (
            sezon_id VARCHAR(50) PRIMARY KEY,
            sezon VARCHAR(20) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # 4. Teams (hamdata'daki ev_id/dep_id, ev_sahibi_takim/deplasman_takim)
    cursor.execute("""
        CREATE TABLE teams (
            team_id VARCHAR(50) PRIMARY KEY,
            team_name VARCHAR(150) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # 5. Team_Seasons (takım-sezon-lig ilişkisi)
    cursor.execute("""
        CREATE TABLE team_seasons (
            team_season_id SERIAL PRIMARY KEY,
            team_id VARCHAR(50) REFERENCES teams(team_id) ON DELETE CASCADE,
            turnuva_id VARCHAR(50) REFERENCES leagues(turnuva_id) ON DELETE CASCADE,
            sezon_id VARCHAR(50) REFERENCES seasons(sezon_id) ON DELETE CASCADE,
            is_active BOOLEAN DEFAULT true,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(team_id, turnuva_id, sezon_id)
        );
    """)
    
    # 6. Matches (hamdata sütunlarıyla)
    cursor.execute("""
        CREATE TABLE matches (
            mac_id VARCHAR(50) PRIMARY KEY,
            turnuva_id VARCHAR(50) REFERENCES leagues(turnuva_id) ON DELETE CASCADE,
            sezon_id VARCHAR(50) REFERENCES seasons(sezon_id) ON DELETE CASCADE,
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # 7. Betting Odds (hamdata'daki oran sütunları)
    cursor.execute("""
        CREATE TABLE betting_odds (
            odds_id SERIAL PRIMARY KEY,
            mac_id VARCHAR(50) REFERENCES matches(mac_id) ON DELETE CASCADE,
            oran_1 DECIMAL(6,3),
            oran_x DECIMAL(6,3),
            oran_2 DECIMAL(6,3),
            oran_alt DECIMAL(6,3),
            oran_ust DECIMAL(6,3),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(mac_id)
        );
    """)
    
    print("✅ Basitleştirilmiş tablo yapısı oluşturuldu!")
    
    # İndeksler oluştur
    cursor.execute("CREATE INDEX idx_teams_id ON teams(team_id);")
    cursor.execute("CREATE INDEX idx_leagues_id ON leagues(turnuva_id);")
    cursor.execute("CREATE INDEX idx_seasons_id ON seasons(sezon_id);")
    cursor.execute("CREATE INDEX idx_matches_id ON matches(mac_id);")
    cursor.execute("CREATE INDEX idx_team_seasons_lookup ON team_seasons(team_id, turnuva_id, sezon_id);")
    cursor.execute("CREATE INDEX idx_matches_date ON matches(tarih);")
    
    print("✅ İndeksler oluşturuldu!")

def safe_int(value):
    """Güvenli integer dönüşümü"""
    try:
        if value is None or value == '' or str(value).lower() == 'nan':
            return None
        return int(float(str(value)))
    except:
        return None

def safe_decimal(value):
    """Güvenli decimal dönüşümü"""
    try:
        if value is None or value == '' or str(value).lower() == 'nan':
            return None
        return float(str(value))
    except:
        return None

def upsert_countries(cursor, conn, df):
    """Ülkeleri UPSERT ile ekle - hamdata ulke sütunu"""
    countries = df['ulke'].dropna().unique()
    countries = [c for c in countries if c and str(c) != 'nan' and str(c).strip()]
    
    if countries:
        for country in countries:
            cursor.execute("""
                INSERT INTO countries (ulke) 
                VALUES (%s) 
                ON CONFLICT (ulke) DO NOTHING
            """, (str(country).strip(),))
        conn.commit()
        print(f"✅ {len(countries)} ülke işlendi")

def upsert_leagues(cursor, conn, df):
    """Ligleri UPSERT ile ekle - hamdata turnuva sütunları"""
    leagues_data = df[['turnuva_id', 'turnuva_adi', 'ulke', 'turnuva_kodu', 'turnuva_kategori_id']].drop_duplicates()
    
    for _, row in leagues_data.iterrows():
        if row['turnuva_id'] and str(row['turnuva_id']) != 'nan' and str(row['turnuva_id']).strip():
            cursor.execute("""
                INSERT INTO leagues (turnuva_id, turnuva_adi, ulke, turnuva_kodu, turnuva_kategori_id) 
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (turnuva_id) DO UPDATE SET
                    turnuva_adi = EXCLUDED.turnuva_adi,
                    ulke = EXCLUDED.ulke,
                    turnuva_kodu = EXCLUDED.turnuva_kodu,
                    turnuva_kategori_id = EXCLUDED.turnuva_kategori_id
            """, (
                str(row['turnuva_id']).strip(), 
                str(row['turnuva_adi']).strip() if row['turnuva_adi'] else '',
                str(row['ulke']).strip() if row['ulke'] else None,
                str(row['turnuva_kodu']).strip() if row['turnuva_kodu'] else None,
                str(row['turnuva_kategori_id']).strip() if row['turnuva_kategori_id'] else None
            ))
    
    conn.commit()
    print(f"✅ {len(leagues_data)} lig işlendi")

def upsert_seasons(cursor, conn, df):
    """Sezonları UPSERT ile ekle - hamdata sezon sütunları"""
    seasons_data = df[['sezon_id', 'sezon']].drop_duplicates()
    
    print(f"🔍 {len(seasons_data)} unique sezon bulundu")
    
    successful_seasons = 0
    
    for _, row in seasons_data.iterrows():
        if row['sezon_id'] and str(row['sezon_id']) != 'nan' and str(row['sezon_id']).strip():
            try:
                cursor.execute("""
                    INSERT INTO seasons (sezon_id, sezon) 
                    VALUES (%s, %s)
                    ON CONFLICT (sezon_id) DO UPDATE SET
                        sezon = EXCLUDED.sezon
                """, (str(row['sezon_id']).strip(), str(row['sezon']).strip() if row['sezon'] else ''))
                successful_seasons += 1
            except Exception as e:
                print(f"⚠️ Sezon ekleme hatası: {row['sezon']} | {e}")
        else:
            print(f"⚠️ Geçersiz sezon_id: '{row['sezon_id']}'")
    
    conn.commit()
    print(f"✅ {successful_seasons} sezon başarıyla işlendi")

def upsert_teams(cursor, conn, df):
    """Takımları UPSERT ile ekle - hamdata takım sütunları"""
    # Ev sahibi takımlar
    home_teams = df[['ev_id', 'ev_sahibi_takim']].rename(columns={
        'ev_id': 'team_id', 'ev_sahibi_takim': 'team_name'
    })
    # Deplasman takımları  
    away_teams = df[['dep_id', 'deplasman_takim']].rename(columns={
        'dep_id': 'team_id', 'deplasman_takim': 'team_name'
    })
    
    all_teams = pd.concat([home_teams, away_teams]).drop_duplicates(subset=['team_id'])
    
    for _, row in all_teams.iterrows():
        if row['team_id'] and str(row['team_id']) != 'nan' and str(row['team_id']).strip():
            cursor.execute("""
                INSERT INTO teams (team_id, team_name) 
                VALUES (%s, %s)
                ON CONFLICT (team_id) DO UPDATE SET
                    team_name = EXCLUDED.team_name
            """, (str(row['team_id']).strip(), str(row['team_name']).strip() if row['team_name'] else ''))
    
    conn.commit()
    print(f"✅ {len(all_teams)} takım işlendi")

def upsert_team_seasons(cursor, conn, df):
    """Takım-Sezon-Lig ilişkilerini UPSERT ile ekle"""
    
    # Ev sahibi takımlar için
    home_data = df[['ev_id', 'turnuva_id', 'sezon_id']].rename(columns={'ev_id': 'team_id'})
    # Deplasman takımları için
    away_data = df[['dep_id', 'turnuva_id', 'sezon_id']].rename(columns={'dep_id': 'team_id'})
    
    all_team_seasons = pd.concat([home_data, away_data]).drop_duplicates()
    
    print(f"🔍 {len(all_team_seasons)} unique takım-sezon kombinasyonu bulundu")
    
    successful_ts = 0
    
    for idx, row in all_team_seasons.iterrows():
        if (row['team_id'] and str(row['team_id']) != 'nan' and 
            row['turnuva_id'] and str(row['turnuva_id']) != 'nan' and 
            row['sezon_id'] and str(row['sezon_id']) != 'nan'):
            
            cursor.execute("""
                INSERT INTO team_seasons (team_id, turnuva_id, sezon_id) 
                VALUES (%s, %s, %s)
                ON CONFLICT (team_id, turnuva_id, sezon_id) DO UPDATE SET
                    is_active = true
            """, (str(row['team_id']).strip(), str(row['turnuva_id']).strip(), str(row['sezon_id']).strip()))
            successful_ts += 1
    
    conn.commit()
    print(f"✅ {successful_ts} takım-sezon ilişkisi başarıyla işlendi")

def upsert_matches(cursor, conn, df):
    """Maçları UPSERT ile ekle - hamdata sütunlarıyla"""
    
    successful_matches = 0
    
    for idx, row in df.iterrows():
        if row['mac_id'] and str(row['mac_id']) != 'nan':
            cursor.execute("""
                INSERT INTO matches (
                    mac_id, turnuva_id, sezon_id, ev_id, dep_id,
                    ev_sahibi_takim, deplasman_takim, tarih, saat, mac_durumu,
                    skor, ev_skor, dep_skor, iy_ev_skor, iy_dep_skor,
                    kategori, istatistik_7, kriter_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (mac_id) DO UPDATE SET
                    turnuva_id = EXCLUDED.turnuva_id,
                    sezon_id = EXCLUDED.sezon_id,
                    ev_id = EXCLUDED.ev_id,
                    dep_id = EXCLUDED.dep_id,
                    ev_sahibi_takim = EXCLUDED.ev_sahibi_takim,
                    deplasman_takim = EXCLUDED.deplasman_takim,
                    tarih = EXCLUDED.tarih,
                    saat = EXCLUDED.saat,
                    mac_durumu = EXCLUDED.mac_durumu,
                    skor = EXCLUDED.skor,
                    ev_skor = EXCLUDED.ev_skor,
                    dep_skor = EXCLUDED.dep_skor,
                    iy_ev_skor = EXCLUDED.iy_ev_skor,
                    iy_dep_skor = EXCLUDED.iy_dep_skor,
                    kategori = EXCLUDED.kategori,
                    istatistik_7 = EXCLUDED.istatistik_7,
                    kriter_id = EXCLUDED.kriter_id,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                str(row['mac_id']).strip(),
                str(row['turnuva_id']).strip() if row['turnuva_id'] else None,
                str(row['sezon_id']).strip() if row['sezon_id'] else None,
                str(row['ev_id']).strip() if row['ev_id'] else None,
                str(row['dep_id']).strip() if row['dep_id'] else None,
                str(row['ev_sahibi_takim']).strip() if row['ev_sahibi_takim'] else '',
                str(row['deplasman_takim']).strip() if row['deplasman_takim'] else '',
                str(row['tarih']).strip() if row['tarih'] else None,
                str(row['saat']).strip() if row['saat'] else None,
                str(row['mac_durumu']).strip() if row['mac_durumu'] else None,
                str(row['skor']).strip() if row['skor'] else None,
                safe_int(row['ev_skor']),
                safe_int(row['dep_skor']),
                safe_int(row['iy_ev_skor']),
                safe_int(row['iy_dep_skor']),
                str(row['kategori']).strip() if row['kategori'] else None,
                str(row['istatistik_7']).strip() if row['istatistik_7'] else None,
                str(row['kriter_id']).strip() if row['kriter_id'] else None
            ))
            successful_matches += 1
    
    conn.commit()
    print(f"✅ {successful_matches} maç başarıyla işlendi")

def upsert_betting_odds(cursor, conn, df):
    """Bahis oranlarını UPSERT ile ekle - hamdata oran sütunları"""
    
    successful_odds = 0
    
    for idx, row in df.iterrows():
        if row['mac_id'] and str(row['mac_id']) != 'nan':
            # Hamdata'dan bahis oranlarını al
            oran_1 = safe_decimal(row['oran_1'])
            oran_x = safe_decimal(row['oran_x'])
            oran_2 = safe_decimal(row['oran_2'])
            oran_alt = safe_decimal(row['oran_alt'])
            oran_ust = safe_decimal(row['oran_ust'])
            
            # En az bir oran varsa ekle
            if any([oran_1, oran_x, oran_2, oran_alt, oran_ust]):
                cursor.execute("""
                    INSERT INTO betting_odds (mac_id, oran_1, oran_x, oran_2, oran_alt, oran_ust) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (mac_id) DO UPDATE SET
                        oran_1 = EXCLUDED.oran_1,
                        oran_x = EXCLUDED.oran_x,
                        oran_2 = EXCLUDED.oran_2,
                        oran_alt = EXCLUDED.oran_alt,
                        oran_ust = EXCLUDED.oran_ust
                """, (str(row['mac_id']).strip(), oran_1, oran_x, oran_2, oran_alt, oran_ust))
                successful_odds += 1
    
    conn.commit()
    print(f"✅ {successful_odds} bahis oranı işlendi")

def show_final_statistics(cursor):
    """Final istatistikleri göster"""
    print("\n" + "="*60)
    print("📊 VERİTABANI İSTATİSTİKLERİ - HAMDATAİLE UYUMLU")
    print("="*60)
    
    tables = [
        ('countries', 'Ülkeler'),
        ('leagues', 'Ligler'),
        ('seasons', 'Sezonlar'),
        ('teams', 'Takımlar'),
        ('team_seasons', 'Takım-Sezon İlişkileri'),
        ('matches', 'Maçlar'),
        ('betting_odds', 'Bahis Oranları')
    ]
    
    for table_name, description in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        result = cursor.fetchone()
        count = result[0] if result else 0
        print(f"📈 {description}: {count:,} kayıt")
    
    print("="*60)

def create_simple_relational_db():
    """Basitleştirilmiş ilişkisel veritabanı oluştur - hamdata ile uyumlu"""
    
    db_config = {
        "dbname": "soccerdb",
        "user": "ahmet21",
        "password": "diclem2121.",
        "host": "165.227.130.23",
        "port": "5432"
    }
    
    pg_conn = None
    cursor = None
    
    try:
        print("🚀 Basitleştirilmiş İlişkisel Futbol Veritabanı V3")
        print("="*60)
        
        # Veritabanına bağlan
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
        
        # 1. Basitleştirilmiş şemayı oluştur
        create_simple_schema(cursor)
        
        # 2. Mevcut hamdata'yı kontrol et
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'hamdata'
            );
        """)
        result = cursor.fetchone()
        hamdata_exists = result[0] if result else False
        
        df = None
        
        if hamdata_exists:
            print("📊 Mevcut hamdata tablosu bulundu, veriler okunuyor...")
            cursor.execute("SELECT COUNT(*) FROM hamdata")
            count_result = cursor.fetchone()
            existing_count = count_result[0] if count_result else 0
            
            if existing_count > 0:
                print(f"💾 {existing_count} adet mevcut veri bulundu")
                cursor.execute("SELECT * FROM hamdata")
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                raw_data = cursor.fetchall()
                
                if columns and raw_data:
                    df_existing = pd.DataFrame(raw_data, columns=columns)
                    print(f"✅ Mevcut veriler DataFrame'e dönüştürüldü: {len(df_existing)} kayıt")
                    df = df_existing
        
        # 3. API'den yeni veri çek (opsiyonel)
        if df is None:
            print("🌐 API'den yeni veri çekiliyor...")
            df_new = get_match_data()
            
            if df_new is not None and not df_new.empty:
                print(f"📡 {len(df_new)} adet yeni API verisi alındı")
                df = df_new
        
        if df is None:
            print("❌ Ne mevcut veri ne de yeni API verisi bulunamadı!")
            return
        
        # 4. Veriyi sırasıyla UPSERT et
        print(f"🚀 {len(df)} kayıt basitleştirilmiş ilişkisel yapıya aktarılıyor...")
        
        upsert_countries(cursor, pg_conn, df)
        upsert_seasons(cursor, pg_conn, df)
        upsert_leagues(cursor, pg_conn, df)
        upsert_teams(cursor, pg_conn, df)
        upsert_team_seasons(cursor, pg_conn, df)
        upsert_matches(cursor, pg_conn, df)
        upsert_betting_odds(cursor, pg_conn, df)
        
        # 5. Final istatistikleri göster
        show_final_statistics(cursor)
        
        print("🎉 Basitleştirilmiş ilişkisel veritabanı başarıyla oluşturuldu!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        print(f"Detay: {traceback.format_exc()}")
        
    finally:
        # Veritabanı bağlantısını düzgün kapat
        if cursor:
            cursor.close()
            print("✅ Cursor kapatıldı")
        if pg_conn:
            pg_conn.close()
            print("✅ Veritabanı bağlantısı kapatıldı")

if __name__ == "__main__":
    create_simple_relational_db()
