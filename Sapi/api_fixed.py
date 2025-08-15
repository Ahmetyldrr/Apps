#!/usr/bin/env python3
"""
API Fixed - İyileştirilmiş Mackolik API Script
Optimize edilmiş veri çekimi ve PostgreSQL entegrasyonu
"""

import http.client
import pandas as pd
import json
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, timedelta
import time

def fetch_api_data(date_str):
    """Belirtilen tarih için API'den veri çek"""
    
    print(f"[TARIH] {date_str} tarihli veriler çekiliyor...")
    
    try:
        conn = http.client.HTTPSConnection('vd.mackolik.com', timeout=30)
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
        
        conn.request('GET', f'/livedata?date={date_str}', headers=headers)
        response = conn.getresponse()
        
        if response.status == 200:
            data = response.read()
            json_data = json.loads(data).get("m", [])
            
            if json_data:
                print(f"   [OK] {len(json_data)} maç bulundu")
                return json_data
            else:
                print(f"   [UYARI] Veri bulunamadı")
                return []
        else:
            print(f"   [HATA] HTTP {response.status}")
            return []
            
    except Exception as e:
        print(f"   [HATA] Hata: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def process_raw_data(raw_matches):
    """Ham veriyi işle ve DataFrame'e dönüştür"""
    
    if not raw_matches:
        return None
    
    print(f"[ISLEM] {len(raw_matches)} kayıt işleniyor...")
    
    processed_data = []
    
    for match in raw_matches:
        try:
            # Temel maç bilgileri
            mac_id = str(match[0]) if len(match) > 0 else ''
            ev_id = str(match[1]) if len(match) > 1 else ''
            ev_takim = str(match[2]) if len(match) > 2 else ''
            dep_id = str(match[3]) if len(match) > 3 else ''
            dep_takim = str(match[4]) if len(match) > 4 else ''
            
            # Maç detayları
            mac_durumu = str(match[6]) if len(match) > 6 else ''
            skor = str(match[7]) if len(match) > 7 else ''
            saat = str(match[16]) if len(match) > 16 else ''
            tarih = str(match[35]) if len(match) > 35 else ''
            
            # Skorlar
            ev_skor = str(match[29]) if len(match) > 29 else '0'
            dep_skor = str(match[30]) if len(match) > 30 else '0'
            iy_ev_skor = str(match[31]) if len(match) > 31 else '0'
            iy_dep_skor = str(match[32]) if len(match) > 32 else '0'
            
            # Bahis oranları
            oran_1 = str(match[18]) if len(match) > 18 else ''
            oran_x = str(match[19]) if len(match) > 19 else ''
            oran_2 = str(match[20]) if len(match) > 20 else ''
            oran_alt = str(match[21]) if len(match) > 21 else ''
            oran_ust = str(match[22]) if len(match) > 22 else ''
            
            # Turnuva bilgileri
            turnuva_info = match[36] if len(match) > 36 and isinstance(match[36], list) else []
            
            turnuva_kategori_id = str(turnuva_info[0]) if len(turnuva_info) > 0 else ''
            ulke = str(turnuva_info[1]) if len(turnuva_info) > 1 else ''
            turnuva_id = str(turnuva_info[2]) if len(turnuva_info) > 2 else ''
            turnuva_adi = str(turnuva_info[3]) if len(turnuva_info) > 3 else ''
            sezon_id = str(turnuva_info[4]) if len(turnuva_info) > 4 else ''
            sezon = str(turnuva_info[5]) if len(turnuva_info) > 5 else ''
            turnuva_kodu = str(turnuva_info[9]) if len(turnuva_info) > 9 else ''
            
            # Diğer bilgiler
            kategori = str(match[34]) if len(match) > 34 else ''
            kriter_id = str(match[5]) if len(match) > 5 else ''
            istatistik_7 = str(match[14]) if len(match) > 14 else ''
            
            # İşlenmiş veriyi listeye ekle
            processed_row = {
                'mac_id': mac_id,
                'ev_id': ev_id,
                'ev_sahibi_takim': ev_takim,
                'dep_id': dep_id,
                'deplasman_takim': dep_takim,
                'kriter_id': kriter_id,
                'mac_durumu': mac_durumu,
                'skor': skor,
                'istatistik_7': istatistik_7,
                'saat': saat,
                'oran_1': oran_1,
                'oran_x': oran_x,
                'oran_2': oran_2,
                'oran_alt': oran_alt,
                'oran_ust': oran_ust,
                'ev_skor': ev_skor,
                'dep_skor': dep_skor,
                'iy_ev_skor': iy_ev_skor,
                'iy_dep_skor': iy_dep_skor,
                'kategori': kategori,
                'tarih': tarih,
                'turnuva_kategori_id': turnuva_kategori_id,
                'ulke': ulke,
                'turnuva_id': turnuva_id,
                'turnuva_adi': turnuva_adi,
                'sezon_id': sezon_id,
                'sezon': sezon,
                'turnuva_kodu': turnuva_kodu
            }
            
            processed_data.append(processed_row)
            
        except Exception as e:
            print(f"   [UYARI] Satır işleme hatası: {e}")
            continue
    
    if processed_data:
        df = pd.DataFrame(processed_data)
        print(f"[OK] {len(processed_data)} kayıt işlendi")
        return df
    else:
        print("[HATA] İşlenecek veri bulunamadı")
        return None

def save_to_hamdata(dataframe):
    """DataFrame'i hamdata tablosuna kaydet"""
    
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
        
        print("[OK] Veritabanı bağlantısı başarılı!")
        
        # Hamdata tablosunu oluştur (yoksa)
        create_table_query = """
            CREATE TABLE IF NOT EXISTS hamdata (
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
                turnuva_kodu TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        cursor.execute(create_table_query)
        pg_conn.commit()
        print("[OK] Hamdata tablosu hazır")
        
        # Mevcut kayıt sayısını kontrol et
        cursor.execute("SELECT COUNT(*) FROM hamdata")
        existing_count_result = cursor.fetchone()
        existing_count = existing_count_result[0] if existing_count_result else 0
        print(f"[ISTATISTIK] Mevcut kayıt sayısı: {existing_count:,}")
        
        # Duplicate mac_id'leri kaldır (son gelen veriyi tut)
        print(f"[KONTROL] Duplicate kayıtlar kontrol ediliyor...")
        original_count = len(dataframe)
        dataframe = dataframe.drop_duplicates(subset=['mac_id'], keep='last')
        final_count = len(dataframe)
        
        if original_count != final_count:
            duplicate_count = original_count - final_count
            print(f"   [TEMIZLIK] {duplicate_count} duplicate kayıt kaldırıldı")
        else:
            print(f"   [OK] Duplicate kayıt bulunamadı")
        
        # DataFrame'i listeye dönüştür
        data_to_insert = []
        for _, row in dataframe.iterrows():
            data_to_insert.append([
                row['mac_id'],
                row['ev_id'],
                row['ev_sahibi_takim'],
                row['dep_id'],
                row['deplasman_takim'],
                row['kriter_id'],
                row['mac_durumu'],
                row['skor'],
                row['istatistik_7'],
                row['saat'],
                row['oran_1'],
                row['oran_x'],
                row['oran_2'],
                row['oran_alt'],
                row['oran_ust'],
                row['ev_skor'],
                row['dep_skor'],
                row['iy_ev_skor'],
                row['iy_dep_skor'],
                row['kategori'],
                row['tarih'],
                row['turnuva_kategori_id'],
                row['ulke'],
                row['turnuva_id'],
                row['turnuva_adi'],
                row['sezon_id'],
                row['sezon'],
                row['turnuva_kodu']
            ])
        
        # UPSERT ile verileri ekle (güvenli batch işlemi)
        print(f"[KAYDET] {len(data_to_insert)} kayıt ekleniyor/güncelleniyor...")
        
        # Batch boyutunu küçült ve güvenli işlem yap
        batch_size = 50
        successful_inserts = 0
        failed_inserts = 0
        
        for i in range(0, len(data_to_insert), batch_size):
            batch = data_to_insert[i:i + batch_size]
            
            try:
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
                    batch,
                    page_size=batch_size
                )
                
                successful_inserts += len(batch)
                
                # Her batch'ten sonra commit yap
                pg_conn.commit()
                
                print(f"   [OK] Batch {i//batch_size + 1}: {len(batch)} kayıt işlendi")
                
            except Exception as batch_error:
                print(f"   [HATA] Batch {i//batch_size + 1} hatası: {batch_error}")
                failed_inserts += len(batch)
                
                # Hata durumunda rollback yap
                pg_conn.rollback()
                
                # Tek tek denemeyi deneyebiliriz
                print(f"   [DENEME] Batch'teki kayıtlar tek tek denenecek...")
                for j, single_record in enumerate(batch):
                    try:
                        cursor.execute(
                            """
                            INSERT INTO hamdata (
                                mac_id, ev_id, ev_sahibi_takim, dep_id, deplasman_takim,
                                kriter_id, mac_durumu, skor, istatistik_7, saat,
                                oran_1, oran_x, oran_2, oran_alt, oran_ust,
                                ev_skor, dep_skor, iy_ev_skor, iy_dep_skor, kategori,
                                tarih, turnuva_kategori_id, ulke, turnuva_id, turnuva_adi,
                                sezon_id, sezon, turnuva_kodu
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                            single_record
                        )
                        pg_conn.commit()
                        successful_inserts += 1
                        failed_inserts -= 1
                        
                    except Exception as single_error:
                        print(f"      [HATA] Kayıt {j+1} (mac_id: {single_record[0]}): {single_error}")
                        pg_conn.rollback()
        
        print(f"[OZET] Başarılı: {successful_inserts}, Başarısız: {failed_inserts}")
        
        # Son durum kontrolü
        cursor.execute("SELECT COUNT(*) FROM hamdata")
        final_count_result = cursor.fetchone()
        final_count = final_count_result[0] if final_count_result else 0
        
        print(f"[OK] İşlem tamamlandı!")
        print(f"[ISTATISTIK] Önceki toplam: {existing_count:,}")
        print(f"[ISTATISTIK] Sonraki toplam: {final_count:,}")
        print(f"[ISTATISTIK] İşlenen kayıt: {successful_inserts:,}")
        print(f"[ISTATISTIK] Başarısız kayıt: {failed_inserts:,}")
        
        if final_count > existing_count:
            new_records = final_count - existing_count
            print(f"[ISTATISTIK] Net yeni kayıt: {new_records:,}")
        else:
            print(f"[ISTATISTIK] Güncellenen kayıt var (yeni kayıt sayısı hesaplanamadı)")
        
    except Exception as e:
        print(f"[HATA] Veritabanı hatası: {e}")
        import traceback
        print(f"Detay: {traceback.format_exc()}")
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'pg_conn' in locals():
            pg_conn.close()

def fetch_multiple_dates(days_back=7):
    """Birden fazla tarih için veri çek"""
    
    print(f"[TARIH] Son {days_back} günün verileri çekiliyor...")
    
    all_matches = []
    
    for i in range(days_back):
        date_to_fetch = datetime.now() - timedelta(days=i)
        date_str = date_to_fetch.strftime("%d/%m/%Y")
        
        matches = fetch_api_data(date_str)
        if matches:
            all_matches.extend(matches)
        
        # API'ye fazla yük binmesin diye 3 saniye bekleme
        if i < days_back - 1:
            print(f"   [BEKLE] 3 saniye bekleniyor...")
            time.sleep(3)
    
    if all_matches:
        print(f"[HEDEF] Toplam {len(all_matches)} maç verisi toplandı")
        return all_matches
    else:
        print("[HATA] Hiç veri toplanamadı")
        return []

def fetch_date_range(start_date, end_date):
    """Belirtilen tarih aralığındaki tüm günler için veri çek"""
    
    current_date = start_date
    all_matches = []
    total_days = (end_date - start_date).days + 1
    
    print(f"[TARIH] {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')} arası {total_days} günlük veri çekiliyor...")
    
    day_counter = 0
    
    while current_date <= end_date:
        day_counter += 1
        date_str = current_date.strftime("%d/%m/%Y")
        
        print(f"   [TARIH] Gün {day_counter}/{total_days}: {date_str}")
        
        matches = fetch_api_data(date_str)
        if matches:
            all_matches.extend(matches)
            print(f"      [OK] {len(matches)} maç eklendi")
        else:
            print(f"      [UYARI] Bu tarihte veri bulunamadı")
        
        # Bir sonraki güne geç
        current_date += timedelta(days=1)
        
        # API'ye fazla yük binmesin diye 5 saniye bekleme (son gün değilse)
        if current_date <= end_date:
            print(f"      [BEKLE] 5 saniye bekleniyor...")
            time.sleep(5)
    
    print(f"\n[HEDEF] Tarih aralığı tarama tamamlandı!")
    print(f"[ISTATISTIK] Toplam {len(all_matches)} maç verisi toplandı")
    
    if all_matches:
        return all_matches
    else:
        print("[HATA] Hiç veri toplanamadı")
        return []

def main():
    """Ana fonksiyon"""
    
    print("[SISTEM] İYİLEŞTİRİLMİŞ API SCRIPT")
    print("="*60)
    print(f"[ZAMAN] Başlangıç: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Kullanıcı seçimi
    print(f"\n[HEDEF] VERİ ÇEKME SEÇENEKLERİ:")
    print("1. Sadece bugün")
    print("2. Son 3 gün")
    print("3. Son 7 gün")
    print("4. Özel tarih")
    print("5. Tarih aralığı (başlangıç - bitiş)")
    
    choice = input("\nSeçiminizi yapın (1-5): ").strip()
    
    raw_matches = []
    
    if choice == "1":
        # Sadece bugün
        today = datetime.now().strftime("%d/%m/%Y")
        raw_matches = fetch_api_data(today)
        
    elif choice == "2":
        # Son 3 gün
        raw_matches = fetch_multiple_dates(3)
        
    elif choice == "3":
        # Son 7 gün
        raw_matches = fetch_multiple_dates(7)
        
    elif choice == "4":
        # Özel tarih
        date_input = input("Tarihi girin (DD/MM/YYYY): ").strip()
        try:
            # Tarih formatını doğrula
            datetime.strptime(date_input, "%d/%m/%Y")
            raw_matches = fetch_api_data(date_input)
        except ValueError:
            print("[HATA] Geçersiz tarih formatı! DD/MM/YYYY formatında girin.")
            return
            
    elif choice == "5":
        # Tarih aralığı
        start_date_input = input("Başlangıç tarihi (DD/MM/YYYY): ").strip()
        end_date_input = input("Bitiş tarihi (DD/MM/YYYY): ").strip()
        
        try:
            # Tarih formatlarını doğrula
            start_date = datetime.strptime(start_date_input, "%d/%m/%Y")
            end_date = datetime.strptime(end_date_input, "%d/%m/%Y")
            
            # Başlangıç tarihi bitiş tarihinden sonra olamaz
            if start_date > end_date:
                print("[HATA] Başlangıç tarihi bitiş tarihinden sonra olamaz!")
                return
            
            # Tarih aralığı bilgisi
            date_diff = (end_date - start_date).days + 1
            print(f"[TARIH] {date_diff} günlük tarih aralığından veri çekiliyor...")
            raw_matches = fetch_date_range(start_date, end_date)
            
        except ValueError:
            print("[HATA] Geçersiz tarih formatı! DD/MM/YYYY formatında girin.")
            return
    else:
        print("[HATA] Geçersiz seçim! Lütfen 1-5 arasında bir sayı girin.")
        return
    
    # Veriyi işle
    if raw_matches:
        df = process_raw_data(raw_matches)
        
        if df is not None and not df.empty:
            # Özet bilgi
            print(f"\n[ISTATISTIK] VERİ ÖZETİ:")
            print(f"   [ISTATISTIK] Toplam Maç: {len(df)}")
            print(f"   [ISTATISTIK] Farklı Ülke: {df['ulke'].nunique()}")
            print(f"   [ISTATISTIK] Farklı Turnuva: {df['turnuva_adi'].nunique()}")
            print(f"   [ISTATISTIK] Farklı Tarih: {df['tarih'].nunique()}")
            
            # Veritabanına kaydet
            save_to_hamdata(df)
            
            print(f"\n[BASARI] İşlem başarıyla tamamlandı!")
            print(f"[ZAMAN] Bitiş: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("[HATA] İşlenecek veri bulunamadı")
    else:
        print("[HATA] Ham veri alınamadı")

if __name__ == "__main__":
    main()
