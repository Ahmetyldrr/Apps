#!/usr/bin/env python3
"""
Hamdata'yı İlişkisel Yapıya Dönüştürme Scripti
Bu script mevcut hamdata tablosunu alır ve ilişkisel tablolara böler
"""

import psycopg2
from psycopg2.extras import execute_values

def convert_hamdata_to_relational():
    """Mevcut hamdata tablosunu ilişkisel yapıya dönüştür"""
    
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
        
        print("🔄 HAMDATA -> İLİŞKİSEL DÖNÜŞÜM")
        print("="*50)
        
        # Hamdata varlığını kontrol et
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'hamdata'
            )
        """)
        hamdata_exists = cursor.fetchone()
        
        if not hamdata_exists or not hamdata_exists[0]:
            print("❌ Hamdata tablosu bulunamadı!")
            print("   Önce api_fixed_clean.py çalıştırın.")
            return
        
        # Hamdata kayıt sayısı
        cursor.execute("SELECT COUNT(*) FROM hamdata")
        hamdata_count = cursor.fetchone()
        total_hamdata = hamdata_count[0] if hamdata_count else 0
        print(f"📊 Hamdata kayıt sayısı: {total_hamdata:,}")
        
        if total_hamdata == 0:
            print("⚠️ Hamdata tablosu boş!")
            return
        
        # İlişkisel tabloları oluştur
        print("\n🏗️ İlişkisel tablolar oluşturuluyor...")
        
        # 1. Countries tablosu
        cursor.execute("DROP TABLE IF EXISTS countries CASCADE")
        cursor.execute("""
            CREATE TABLE countries (
                ulke VARCHAR(100) PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 2. Leagues tablosu
        cursor.execute("DROP TABLE IF EXISTS leagues CASCADE")
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
        
        # 3. Seasons tablosu
        cursor.execute("DROP TABLE IF EXISTS seasons CASCADE")
        cursor.execute("""
            CREATE TABLE seasons (
                sezon_id VARCHAR(50) PRIMARY KEY,
                sezon VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 4. Teams tablosu
        cursor.execute("DROP TABLE IF EXISTS teams CASCADE")
        cursor.execute("""
            CREATE TABLE teams (
                team_id VARCHAR(50) PRIMARY KEY,
                team_name VARCHAR(150) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 5. Matches tablosu
        cursor.execute("DROP TABLE IF EXISTS matches CASCADE")
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
        
        # 6. Betting Odds tablosu
        cursor.execute("DROP TABLE IF EXISTS betting_odds CASCADE")
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
        
        print("✅ Tablolar oluşturuldu!")
        
        # Hamdata'dan veri çek
        print("\n📊 Hamdata verisi okunuyor...")
        cursor.execute("SELECT * FROM hamdata")
        hamdata_rows = cursor.fetchall()
        
        # Sütun isimlerini al
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'hamdata' 
            ORDER BY ordinal_position
        """)
        column_names = [row[0] for row in cursor.fetchall()]
        
        print(f"✅ {len(hamdata_rows)} kayıt okundu")
        
        # Veriyi işle
        countries_set = set()
        leagues_dict = {}
        seasons_dict = {}
        teams_dict = {}
        matches_list = []
        betting_odds_list = []
        
        print("\n🔄 Veriler işleniyor...")
        
        for row in hamdata_rows:
            # Row'u dictionary'ye dönüştür
            data = dict(zip(column_names, row))
            
            # Countries
            if data.get('ulke') and data['ulke'].strip():
                countries_set.add(data['ulke'].strip())
            
            # Leagues
            if data.get('turnuva_id') and data['turnuva_id'].strip():
                leagues_dict[data['turnuva_id']] = {
                    'turnuva_id': data['turnuva_id'],
                    'turnuva_adi': data.get('turnuva_adi', ''),
                    'ulke': data.get('ulke', ''),
                    'turnuva_kodu': data.get('turnuva_kodu', ''),
                    'turnuva_kategori_id': data.get('turnuva_kategori_id', '')
                }
            
            # Seasons
            if data.get('sezon_id') and data['sezon_id'].strip():
                seasons_dict[data['sezon_id']] = {
                    'sezon_id': data['sezon_id'],
                    'sezon': data.get('sezon', '')
                }
            
            # Teams
            if data.get('ev_id') and data['ev_id'].strip():
                teams_dict[data['ev_id']] = {
                    'team_id': data['ev_id'],
                    'team_name': data.get('ev_sahibi_takim', '')
                }
            
            if data.get('dep_id') and data['dep_id'].strip():
                teams_dict[data['dep_id']] = {
                    'team_id': data['dep_id'],
                    'team_name': data.get('deplasman_takim', '')
                }
            
            # Matches
            if data.get('mac_id') and data['mac_id'].strip():
                try:
                    ev_skor = int(data.get('ev_skor', 0)) if data.get('ev_skor') and str(data['ev_skor']).isdigit() else 0
                    dep_skor = int(data.get('dep_skor', 0)) if data.get('dep_skor') and str(data['dep_skor']).isdigit() else 0
                    iy_ev_skor = int(data.get('iy_ev_skor', 0)) if data.get('iy_ev_skor') and str(data['iy_ev_skor']).isdigit() else 0
                    iy_dep_skor = int(data.get('iy_dep_skor', 0)) if data.get('iy_dep_skor') and str(data['iy_dep_skor']).isdigit() else 0
                except:
                    ev_skor = dep_skor = iy_ev_skor = iy_dep_skor = 0
                
                matches_list.append([
                    data['mac_id'],
                    data.get('turnuva_id'),
                    data.get('sezon_id'),
                    data.get('ev_id'),
                    data.get('dep_id'),
                    data.get('ev_sahibi_takim', ''),
                    data.get('deplasman_takim', ''),
                    data.get('tarih'),
                    data.get('saat'),
                    data.get('mac_durumu'),
                    data.get('skor'),
                    ev_skor,
                    dep_skor,
                    iy_ev_skor,
                    iy_dep_skor,
                    data.get('kategori'),
                    data.get('istatistik_7'),
                    data.get('kriter_id')
                ])
            
            # Betting odds
            if data.get('mac_id') and data['mac_id'].strip():
                try:
                    oran_1 = float(data['oran_1']) if data.get('oran_1') and data['oran_1'] not in ['', 'None'] else None
                    oran_x = float(data['oran_x']) if data.get('oran_x') and data['oran_x'] not in ['', 'None'] else None
                    oran_2 = float(data['oran_2']) if data.get('oran_2') and data['oran_2'] not in ['', 'None'] else None
                    oran_alt = float(data['oran_alt']) if data.get('oran_alt') and data['oran_alt'] not in ['', 'None'] else None
                    oran_ust = float(data['oran_ust']) if data.get('oran_ust') and data['oran_ust'] not in ['', 'None'] else None
                except:
                    oran_1 = oran_x = oran_2 = oran_alt = oran_ust = None
                
                # En az bir oran varsa ekle
                if any([oran_1, oran_x, oran_2, oran_alt, oran_ust]):
                    betting_odds_list.append([
                        data['mac_id'],
                        oran_1,
                        oran_x,
                        oran_2,
                        oran_alt,
                        oran_ust
                    ])
        
        # Verileri tablolara ekle
        print("\n📥 Veriler tablolara ekleniyor...")
        
        # 1. Countries
        if countries_set:
            countries_list = [[country] for country in countries_set]
            execute_values(cursor, "INSERT INTO countries (ulke) VALUES %s", countries_list)
            print(f"✅ {len(countries_list)} ülke eklendi")
        
        # 2. Seasons
        if seasons_dict:
            seasons_list = [[v['sezon_id'], v['sezon']] for v in seasons_dict.values()]
            execute_values(cursor, "INSERT INTO seasons (sezon_id, sezon) VALUES %s", seasons_list)
            print(f"✅ {len(seasons_list)} sezon eklendi")
        
        # 3. Leagues
        if leagues_dict:
            leagues_list = [[
                v['turnuva_id'], 
                v['turnuva_adi'], 
                v['ulke'] if v['ulke'] else None,
                v['turnuva_kodu'] if v['turnuva_kodu'] else None,
                v['turnuva_kategori_id'] if v['turnuva_kategori_id'] else None
            ] for v in leagues_dict.values()]
            execute_values(cursor, """
                INSERT INTO leagues (turnuva_id, turnuva_adi, ulke, turnuva_kodu, turnuva_kategori_id) 
                VALUES %s
            """, leagues_list)
            print(f"✅ {len(leagues_list)} lig eklendi")
        
        # 4. Teams
        if teams_dict:
            teams_list = [[v['team_id'], v['team_name']] for v in teams_dict.values()]
            execute_values(cursor, "INSERT INTO teams (team_id, team_name) VALUES %s", teams_list)
            print(f"✅ {len(teams_list)} takım eklendi")
        
        # 5. Matches
        if matches_list:
            execute_values(cursor, """
                INSERT INTO matches (
                    mac_id, turnuva_id, sezon_id, ev_id, dep_id,
                    ev_sahibi_takim, deplasman_takim, tarih, saat, mac_durumu,
                    skor, ev_skor, dep_skor, iy_ev_skor, iy_dep_skor,
                    kategori, istatistik_7, kriter_id
                ) VALUES %s
            """, matches_list)
            print(f"✅ {len(matches_list)} maç eklendi")
        
        # 6. Betting Odds
        if betting_odds_list:
            execute_values(cursor, """
                INSERT INTO betting_odds (mac_id, oran_1, oran_x, oran_2, oran_alt, oran_ust) 
                VALUES %s
            """, betting_odds_list)
            print(f"✅ {len(betting_odds_list)} bahis oranı eklendi")
        
        pg_conn.commit()
        
        # Final istatistikler
        print(f"\n📊 DÖNÜŞÜM İSTATİSTİKLERİ:")
        print(f"   🗃️ Hamdata Kaynak: {total_hamdata:,} kayıt")
        print(f"   🌍 Countries: {len(countries_set):,} ülke")
        print(f"   🏆 Leagues: {len(leagues_dict):,} lig")
        print(f"   📅 Seasons: {len(seasons_dict):,} sezon")
        print(f"   ⚽ Teams: {len(teams_dict):,} takım")
        print(f"   🏈 Matches: {len(matches_list):,} maç")
        print(f"   💰 Betting Odds: {len(betting_odds_list):,} oran")
        
        cursor.close()
        pg_conn.close()
        
        print(f"\n✅ Dönüşüm başarıyla tamamlandı!")
        print("🔗 İlişkisel tablolar hazır!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        print(f"Detay: {traceback.format_exc()}")

if __name__ == "__main__":
    convert_hamdata_to_relational()
