#!/usr/bin/env python3
"""
API Update - Mevcut veritabanına yeni veri ekleme/güncelleme
- Mevcut tabloları silmez
- Sadece UPSERT işlemi yapar
- İlişkisel tabloları da günceller
"""

import http.client
import pandas as pd
import json
import psycopg2
from psycopg2.extras import execute_values

# Tarih parametresi
datex = "16/08/2025"

print(f"📅 {datex} tarihli veriler çekiliyor...")

conn = http.client.HTTPSConnection('vd.mackolik.com')
headers = {
    'accept': '*/*',
    'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    'if-modified-since': 'Tue, 05 Aug 2025 22:34:53 GMT',
    'origin': 'https://arsiv.mackolik.com',
    'priority': 'u=1, i',
    'referer': 'https://arsiv.mackolik.com/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
}
conn.request('GET', f'/livedata?date={datex}', headers=headers)
response = conn.getresponse()

data = response.read()
df = None
if response.status == 200:  
    json_data = json.loads(data).get("m")
    if json_data:
        df = pd.DataFrame(json_data)
    else:
        print(f"❌ {datex} tarihi için veri bulunamadı.")
else:
    print(f"❌ Veri çekilemedi. HTTP Status: {response.status}")

if df is not None and not df.empty:
    print(f"✅ {len(df)} adet maç verisi bulundu.")
    
    def update_database_sync(dataframe):
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

            # Mevcut tablo sayılarını kontrol et
            cursor.execute("SELECT COUNT(*) FROM hamdata")
            result = cursor.fetchone()
            hamdata_before = result[0] if result else 0
            print(f"📊 Mevcut hamdata kayıt sayısı: {hamdata_before}")

            # DataFrame'i işle
            filtered_data = []
            new_countries = set()
            new_leagues = set()
            new_seasons = set()
            new_teams = set()
            
            for idx, row in dataframe.iterrows():
                # Turnuva bilgilerini ayrıştır
                try:
                    turnuva_raw = row[36] if len(row) > 36 else []
                    turnuva_info = turnuva_raw if isinstance(turnuva_raw, list) else []
                except:
                    turnuva_info = []
                
                turnuva_kategori_id = str(turnuva_info[0]) if len(turnuva_info) > 0 else ''
                turnuva_kategorisi = str(turnuva_info[1]) if len(turnuva_info) > 1 else ''
                turnuva_id = str(turnuva_info[2]) if len(turnuva_info) > 2 else ''
                turnuva_adi = str(turnuva_info[3]) if len(turnuva_info) > 3 else ''
                sezon_id = str(turnuva_info[4]) if len(turnuva_info) > 4 else ''
                sezon = str(turnuva_info[5]) if len(turnuva_info) > 5 else ''
                turnuva_kodu = str(turnuva_info[9]) if len(turnuva_info) > 9 else ''
                
                # Yeni veriler için setleri güncelle
                if turnuva_kategorisi and turnuva_kategorisi != 'nan':
                    new_countries.add((turnuva_kategori_id, turnuva_kategorisi))
                if turnuva_id and turnuva_adi and turnuva_adi != 'nan':
                    new_leagues.add((turnuva_id, turnuva_adi, turnuva_kategori_id, turnuva_kodu))
                if sezon_id and sezon and sezon != 'nan':
                    new_seasons.add((sezon_id, sezon, turnuva_id))
                
                ev_takim = str(row[2]) if len(row) > 2 else ''
                dep_takim = str(row[4]) if len(row) > 4 else ''
                ev_id = str(row[1]) if len(row) > 1 else ''
                dep_id = str(row[3]) if len(row) > 3 else ''
                
                if ev_takim and ev_takim != 'nan':
                    new_teams.add((ev_id, ev_takim))
                if dep_takim and dep_takim != 'nan':
                    new_teams.add((dep_id, dep_takim))
                
                # Hamdata için filtrelenmiş satır
                filtered_row = [
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
                filtered_data.append(filtered_row)

            print(f"🔄 İşlenecek kayıt sayısı: {len(filtered_data)}")

            # 1. Countries tablosunu güncelle
            if new_countries:
                # Unique country names sadece
                unique_countries = list(set([cname for cid, cname in new_countries if cid and cname and cname != 'nan']))
                country_data = [[cname] for cname in unique_countries]
                if country_data:
                    execute_values(
                        cursor,
                        """
                        INSERT INTO countries (ulke)
                        VALUES %s
                        ON CONFLICT (ulke) DO NOTHING
                        """,
                        country_data,
                        page_size=100
                    )
                    print(f"🌍 {len(country_data)} ülke güncellendi")

            # 2. Leagues tablosunu güncelle
            if new_leagues:
                # Unique turnuva_id'ye göre de-duplicate et
                league_dict = {}
                for lid, lname, cid, lcode in new_leagues:
                    if lid and lname and lname != 'nan':
                        league_dict[lid] = [lid, lname, lcode, cid]
                
                league_data = list(league_dict.values())
                if league_data:
                    execute_values(
                        cursor,
                        """
                        INSERT INTO leagues (turnuva_id, turnuva_adi, turnuva_kodu, turnuva_kategori_id)
                        VALUES %s
                        ON CONFLICT (turnuva_id) DO UPDATE SET
                            turnuva_adi = EXCLUDED.turnuva_adi,
                            turnuva_kodu = EXCLUDED.turnuva_kodu,
                            turnuva_kategori_id = EXCLUDED.turnuva_kategori_id
                        """,
                        league_data,
                        page_size=100
                    )
                    print(f"🏆 {len(league_data)} turnuva güncellendi")

            # 3. Seasons tablosunu güncelle
            if new_seasons:
                # Unique sezon_id'ye göre de-duplicate et
                season_dict = {}
                for sid, sname, lid in new_seasons:
                    if sid and sname and sname != 'nan':
                        season_dict[sid] = [sid, sname]
                
                season_data = list(season_dict.values())
                if season_data:
                    execute_values(
                        cursor,
                        """
                        INSERT INTO seasons (sezon_id, sezon)
                        VALUES %s
                        ON CONFLICT (sezon_id) DO UPDATE SET
                            sezon = EXCLUDED.sezon
                        """,
                        season_data,
                        page_size=100
                    )
                    print(f"📅 {len(season_data)} sezon güncellendi")

            # 4. Teams tablosunu güncelle
            if new_teams:
                # Unique team_id'ye göre de-duplicate et
                team_dict = {}
                for tid, tname in new_teams:
                    if tid and tname and tname != 'nan':
                        team_dict[tid] = [tid, tname]
                
                team_data = list(team_dict.values())
                if team_data:
                    execute_values(
                        cursor,
                        """
                        INSERT INTO teams (team_id, team_name)
                        VALUES %s
                        ON CONFLICT (team_id) DO UPDATE SET
                            team_name = EXCLUDED.team_name
                        """,
                        team_data,
                        page_size=100
                    )
                    print(f"⚽ {len(team_data)} takım güncellendi")

            # 5. Hamdata tablosunu güncelle
            if filtered_data:
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
                    ON CONFLICT (mac_id) DO UPDATE SET
                        ev_id = EXCLUDED.ev_id,
                        ev_sahibi_takim = EXCLUDED.ev_sahibi_takim,
                        dep_id = EXCLUDED.dep_id,
                        deplasman_takim = EXCLUDED.deplasman_takim,
                        kriter_id = EXCLUDED.kriter_id,
                        mac_durumu = EXCLUDED.mac_durumu,
                        skor = EXCLUDED.skor,
                        istatistik_7 = EXCLUDED.istatistik_7,
                        saat = EXCLUDED.saat,
                        oran_1 = EXCLUDED.oran_1,
                        oran_x = EXCLUDED.oran_x,
                        oran_2 = EXCLUDED.oran_2,
                        oran_alt = EXCLUDED.oran_alt,
                        oran_ust = EXCLUDED.oran_ust,
                        ev_skor = EXCLUDED.ev_skor,
                        dep_skor = EXCLUDED.dep_skor,
                        iy_ev_skor = EXCLUDED.iy_ev_skor,
                        iy_dep_skor = EXCLUDED.iy_dep_skor,
                        kategori = EXCLUDED.kategori,
                        tarih = EXCLUDED.tarih,
                        turnuva_kategori_id = EXCLUDED.turnuva_kategori_id,
                        ulke = EXCLUDED.ulke,
                        turnuva_id = EXCLUDED.turnuva_id,
                        turnuva_adi = EXCLUDED.turnuva_adi,
                        sezon_id = EXCLUDED.sezon_id,
                        sezon = EXCLUDED.sezon,
                        turnuva_kodu = EXCLUDED.turnuva_kodu
                    """,
                    filtered_data,
                    page_size=100
                )

                pg_conn.commit()

                # İstatistikleri kontrol et
                cursor.execute("SELECT COUNT(*) FROM hamdata")
                result = cursor.fetchone()
                hamdata_after = result[0] if result else 0
                
                added_count = hamdata_after - hamdata_before
                print(f"✅ {len(filtered_data)} kayıt işlendi!")
                print(f"📊 Önceki toplam: {hamdata_before}")
                print(f"📊 Sonraki toplam: {hamdata_after}")
                print(f"📈 Yeni eklenen: {added_count}")

            # 6. Matches tablosunu güncelle
            matches_data = []
            for row_data in filtered_data:
                mac_id = row_data[0]
                ev_id = row_data[1]
                ev_sahibi_takim = row_data[2]
                dep_id = row_data[3]
                deplasman_takim = row_data[4]
                kriter_id = row_data[5]
                mac_durumu = row_data[6]
                skor = row_data[7]
                istatistik_7 = row_data[8]
                saat = row_data[9]
                ev_skor = row_data[15] if row_data[15] and row_data[15] != 'None' else 0
                dep_skor = row_data[16] if row_data[16] and row_data[16] != 'None' else 0
                iy_ev_skor = row_data[17] if row_data[17] and row_data[17] != 'None' else 0
                iy_dep_skor = row_data[18] if row_data[18] and row_data[18] != 'None' else 0
                kategori = row_data[19]
                tarih = row_data[20]
                turnuva_id = row_data[23]
                sezon_id = row_data[25]
                
                matches_data.append([
                    mac_id, turnuva_id, sezon_id, ev_id, dep_id,
                    ev_sahibi_takim, deplasman_takim, tarih, saat, mac_durumu,
                    skor, ev_skor, dep_skor, iy_ev_skor, iy_dep_skor,
                    kategori, istatistik_7, kriter_id
                ])

            if matches_data:
                execute_values(
                    cursor,
                    """
                    INSERT INTO matches (
                        mac_id, turnuva_id, sezon_id, ev_id, dep_id,
                        ev_sahibi_takim, deplasman_takim, tarih, saat, mac_durumu,
                        skor, ev_skor, dep_skor, iy_ev_skor, iy_dep_skor,
                        kategori, istatistik_7, kriter_id
                    ) VALUES %s
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
                    """,
                    matches_data,
                    page_size=100
                )
                print(f"🏈 {len(matches_data)} maç kaydı güncellendi")

            # 7. Team_Seasons tablosunu güncelle
            team_seasons_data = set()
            for row_data in filtered_data:
                ev_id = row_data[1]
                dep_id = row_data[3]
                turnuva_id = row_data[23]
                sezon_id = row_data[25]
                
                if ev_id and turnuva_id and sezon_id:
                    team_seasons_data.add((ev_id, turnuva_id, sezon_id))
                if dep_id and turnuva_id and sezon_id:
                    team_seasons_data.add((dep_id, turnuva_id, sezon_id))

            if team_seasons_data:
                team_seasons_list = [[team_id, turnuva_id, sezon_id] for team_id, turnuva_id, sezon_id in team_seasons_data]
                execute_values(
                    cursor,
                    """
                    INSERT INTO team_seasons (team_id, turnuva_id, sezon_id)
                    VALUES %s
                    ON CONFLICT (team_id, turnuva_id, sezon_id) DO UPDATE SET
                        is_active = true,
                        created_at = EXCLUDED.created_at
                    """,
                    team_seasons_list,
                    page_size=100
                )
                print(f"🔗 {len(team_seasons_list)} takım-sezon ilişkisi güncellendi")

            # 8. Betting_Odds tablosunu güncelle
            betting_data = []
            for row_data in filtered_data:
                mac_id = row_data[0]
                oran_1 = row_data[10] if row_data[10] and row_data[10] != 'None' else None
                oran_x = row_data[11] if row_data[11] and row_data[11] != 'None' else None
                oran_2 = row_data[12] if row_data[12] and row_data[12] != 'None' else None
                oran_alt = row_data[13] if row_data[13] and row_data[13] != 'None' else None
                oran_ust = row_data[14] if row_data[14] and row_data[14] != 'None' else None
                
                # En az bir oran varsa ekle
                if any([oran_1, oran_x, oran_2, oran_alt, oran_ust]):
                    betting_data.append([mac_id, oran_1, oran_x, oran_2, oran_alt, oran_ust])

            if betting_data:
                execute_values(
                    cursor,
                    """
                    INSERT INTO betting_odds (mac_id, oran_1, oran_x, oran_2, oran_alt, oran_ust)
                    VALUES %s
                    ON CONFLICT (mac_id) DO UPDATE SET
                        oran_1 = EXCLUDED.oran_1,
                        oran_x = EXCLUDED.oran_x,
                        oran_2 = EXCLUDED.oran_2,
                        oran_alt = EXCLUDED.oran_alt,
                        oran_ust = EXCLUDED.oran_ust,
                        created_at = CURRENT_TIMESTAMP
                    """,
                    betting_data,
                    page_size=100
                )
                print(f"💰 {len(betting_data)} bahis oranı güncellendi")

            pg_conn.commit()
            print("✅ Tüm tablolar başarıyla güncellendi!")

        except Exception as e:
            print(f"❌ Veritabanı hatası: {e}")
        finally:
            if cursor:
                cursor.close()
            if pg_conn:
                pg_conn.close()
        
        print("🎉 Güncelleme işlemi tamamlandı!")

    # Fonksiyonu çağır
    update_database_sync(df)
else:
    print("❌ Veri alınamadı veya boş.")
