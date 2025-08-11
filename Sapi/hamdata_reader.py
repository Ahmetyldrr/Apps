#!/usr/bin/env python3
"""
Hamdata Reader - PostgreSQL'den veri çekme ve DataFrame oluşturma
Hamdata tablosundan verileri alıp pandas DataFrame'e dönüştürür
"""

import pandas as pd
import psycopg2
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def connect_database():
    """Veritabanı bağlantısı kur"""
    
    db_config = {
        "dbname": "soccerdb",
        "user": "ahmet21",
        "password": "diclem2121.",
        "host": "165.227.130.23",
        "port": "5432"
    }
    
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['dbname'],
            user=db_config['user'],
            password=db_config['password'],
            connect_timeout=10
        )
        print("[OK] Veritabanı bağlantısı başarılı!")
        return conn
    
    except Exception as e:
        print(f"[HATA] Veritabanı bağlantı hatası: {e}")
        return None

def get_all_data():
    """Hamdata tablosundaki tüm verileri al"""
    
    conn = connect_database()
    if not conn:
        return None
    
    try:
        print("[VERI] Tüm hamdata verileri çekiliyor...")
        
        query = """
            SELECT 
                mac_id,
                ev_id,
                ev_sahibi_takim,
                dep_id,
                deplasman_takim,
                kriter_id,
                mac_durumu,
                skor,
                istatistik_7,
                saat,
                oran_1,
                oran_x,
                oran_2,
                oran_alt,
                oran_ust,
                ev_skor,
                dep_skor,
                iy_ev_skor,
                iy_dep_skor,
                kategori,
                tarih,
                turnuva_kategori_id,
                ulke,
                turnuva_id,
                turnuva_adi,
                sezon_id,
                sezon,
                turnuva_kodu,
                created_at
            FROM hamdata 
            ORDER BY created_at DESC
        """
        
        df = pd.read_sql_query(query, conn)
        
        if not df.empty:
            print(f"[OK] {len(df):,} kayıt başarıyla çekildi")
            return df
        else:
            print("[UYARI] Hiç veri bulunamadı")
            return None
            
    except Exception as e:
        print(f"[HATA] Veri çekme hatası: {e}")
        return None
        
    finally:
        conn.close()

def get_data_by_date(target_date):
    """Belirli bir tarihteki verileri al"""
    
    conn = connect_database()
    if not conn:
        return None
    
    try:
        print(f"[VERI] {target_date} tarihli veriler çekiliyor...")
        
        query = """
            SELECT 
                mac_id,
                ev_id,
                ev_sahibi_takim,
                dep_id,
                deplasman_takim,
                kriter_id,
                mac_durumu,
                skor,
                istatistik_7,
                saat,
                oran_1,
                oran_x,
                oran_2,
                oran_alt,
                oran_ust,
                ev_skor,
                dep_skor,
                iy_ev_skor,
                iy_dep_skor,
                kategori,
                tarih,
                turnuva_kategori_id,
                ulke,
                turnuva_id,
                turnuva_adi,
                sezon_id,
                sezon,
                turnuva_kodu,
                created_at
            FROM hamdata 
            WHERE tarih = %s
            ORDER BY saat
        """
        
        df = pd.read_sql_query(query, conn, params=[target_date])
        
        if not df.empty:
            print(f"[OK] {len(df):,} kayıt çekildi ({target_date})")
            return df
        else:
            print(f"[UYARI] {target_date} tarihinde veri bulunamadı")
            return None
            
    except Exception as e:
        print(f"[HATA] Veri çekme hatası: {e}")
        return None
        
    finally:
        conn.close()

def get_data_by_date_range(start_date, end_date):
    """Belirli tarih aralığındaki verileri al"""
    
    conn = connect_database()
    if not conn:
        return None
    
    try:
        print(f"[VERI] {start_date} - {end_date} arası veriler çekiliyor...")
        
        query = """
            SELECT 
                mac_id,
                ev_id,
                ev_sahibi_takim,
                dep_id,
                deplasman_takim,
                kriter_id,
                mac_durumu,
                skor,
                istatistik_7,
                saat,
                oran_1,
                oran_x,
                oran_2,
                oran_alt,
                oran_ust,
                ev_skor,
                dep_skor,
                iy_ev_skor,
                iy_dep_skor,
                kategori,
                tarih,
                turnuva_kategori_id,
                ulke,
                turnuva_id,
                turnuva_adi,
                sezon_id,
                sezon,
                turnuva_kodu,
                created_at
            FROM hamdata 
            WHERE tarih >= %s AND tarih <= %s
            ORDER BY tarih, saat
        """
        
        df = pd.read_sql_query(query, conn, params=[start_date, end_date])
        
        if not df.empty:
            print(f"[OK] {len(df):,} kayıt çekildi ({start_date} - {end_date})")
            return df
        else:
            print(f"[UYARI] {start_date} - {end_date} arasında veri bulunamadı")
            return None
            
    except Exception as e:
        print(f"[HATA] Veri çekme hatası: {e}")
        return None
        
    finally:
        conn.close()

def get_data_by_country(country_name):
    """Belirli ülkedeki verileri al"""
    
    conn = connect_database()
    if not conn:
        return None
    
    try:
        print(f"[VERI] {country_name} ülkesindeki veriler çekiliyor...")
        
        query = """
            SELECT 
                mac_id,
                ev_id,
                ev_sahibi_takim,
                dep_id,
                deplasman_takim,
                kriter_id,
                mac_durumu,
                skor,
                istatistik_7,
                saat,
                oran_1,
                oran_x,
                oran_2,
                oran_alt,
                oran_ust,
                ev_skor,
                dep_skor,
                iy_ev_skor,
                iy_dep_skor,
                kategori,
                tarih,
                turnuva_kategori_id,
                ulke,
                turnuva_id,
                turnuva_adi,
                sezon_id,
                sezon,
                turnuva_kodu,
                created_at
            FROM hamdata 
            WHERE ulke ILIKE %s
            ORDER BY tarih DESC, saat
        """
        
        df = pd.read_sql_query(query, conn, params=[f'%{country_name}%'])
        
        if not df.empty:
            print(f"[OK] {len(df):,} kayıt çekildi ({country_name})")
            return df
        else:
            print(f"[UYARI] {country_name} ülkesinde veri bulunamadı")
            return None
            
    except Exception as e:
        print(f"[HATA] Veri çekme hatası: {e}")
        return None
        
    finally:
        conn.close()

def get_data_by_league(league_name):
    """Belirli ligdeki verileri al"""
    
    conn = connect_database()
    if not conn:
        return None
    
    try:
        print(f"[VERI] {league_name} ligindeki veriler çekiliyor...")
        
        query = """
            SELECT 
                mac_id,
                ev_id,
                ev_sahibi_takim,
                dep_id,
                deplasman_takim,
                kriter_id,
                mac_durumu,
                skor,
                istatistik_7,
                saat,
                oran_1,
                oran_x,
                oran_2,
                oran_alt,
                oran_ust,
                ev_skor,
                dep_skor,
                iy_ev_skor,
                iy_dep_skor,
                kategori,
                tarih,
                turnuva_kategori_id,
                ulke,
                turnuva_id,
                turnuva_adi,
                sezon_id,
                sezon,
                turnuva_kodu,
                created_at
            FROM hamdata 
            WHERE turnuva_adi ILIKE %s
            ORDER BY tarih DESC, saat
        """
        
        df = pd.read_sql_query(query, conn, params=[f'%{league_name}%'])
        
        if not df.empty:
            print(f"[OK] {len(df):,} kayıt çekildi ({league_name})")
            return df
        else:
            print(f"[UYARI] {league_name} liginde veri bulunamadı")
            return None
            
    except Exception as e:
        print(f"[HATA] Veri çekme hatası: {e}")
        return None
        
    finally:
        conn.close()

def get_latest_data(limit=1000):
    """En son eklenen verileri al"""
    
    conn = connect_database()
    if not conn:
        return None
    
    try:
        print(f"[VERI] En son {limit} kayıt çekiliyor...")
        
        query = """
            SELECT 
                mac_id,
                ev_id,
                ev_sahibi_takim,
                dep_id,
                deplasman_takim,
                kriter_id,
                mac_durumu,
                skor,
                istatistik_7,
                saat,
                oran_1,
                oran_x,
                oran_2,
                oran_alt,
                oran_ust,
                ev_skor,
                dep_skor,
                iy_ev_skor,
                iy_dep_skor,
                kategori,
                tarih,
                turnuva_kategori_id,
                ulke,
                turnuva_id,
                turnuva_adi,
                sezon_id,
                sezon,
                turnuva_kodu,
                created_at
            FROM hamdata 
            ORDER BY created_at DESC
            LIMIT %s
        """
        
        df = pd.read_sql_query(query, conn, params=[limit])
        
        if not df.empty:
            print(f"[OK] {len(df):,} kayıt çekildi (en son)")
            return df
        else:
            print("[UYARI] Hiç veri bulunamadı")
            return None
            
    except Exception as e:
        print(f"[HATA] Veri çekme hatası: {e}")
        return None
        
    finally:
        conn.close()

def get_database_stats():
    """Veritabanı istatistiklerini göster"""
    
    conn = connect_database()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        
        print("[ISTATISTIK] Hamdata tablosu özeti:")
        print("-" * 50)
        
        # Toplam kayıt sayısı
        cursor.execute("SELECT COUNT(*) FROM hamdata")
        total_count = cursor.fetchone()[0]
        print(f"Toplam kayıt: {total_count:,}")
        
        # Farklı ülke sayısı
        cursor.execute("SELECT COUNT(DISTINCT ulke) FROM hamdata WHERE ulke != ''")
        country_count = cursor.fetchone()[0]
        print(f"Farklı ülke: {country_count}")
        
        # Farklı turnuva sayısı
        cursor.execute("SELECT COUNT(DISTINCT turnuva_adi) FROM hamdata WHERE turnuva_adi != ''")
        league_count = cursor.fetchone()[0]
        print(f"Farklı turnuva: {league_count}")
        
        # Farklı tarih sayısı
        cursor.execute("SELECT COUNT(DISTINCT tarih) FROM hamdata WHERE tarih != ''")
        date_count = cursor.fetchone()[0]
        print(f"Farklı tarih: {date_count}")
        
        # En eski ve en yeni tarih
        cursor.execute("SELECT MIN(tarih), MAX(tarih) FROM hamdata WHERE tarih != ''")
        min_date, max_date = cursor.fetchone()
        print(f"Tarih aralığı: {min_date} - {max_date}")
        
        # En popüler ülkeler (top 5)
        cursor.execute("""
            SELECT ulke, COUNT(*) as sayi 
            FROM hamdata 
            WHERE ulke != '' 
            GROUP BY ulke 
            ORDER BY sayi DESC 
            LIMIT 5
        """)
        
        print("\nEn popüler ülkeler:")
        for country, count in cursor.fetchall():
            print(f"  {country}: {count:,} maç")
        
        # En popüler turnuvalar (top 5)
        cursor.execute("""
            SELECT turnuva_adi, COUNT(*) as sayi 
            FROM hamdata 
            WHERE turnuva_adi != '' 
            GROUP BY turnuva_adi 
            ORDER BY sayi DESC 
            LIMIT 5
        """)
        
        print("\nEn popüler turnuvalar:")
        for league, count in cursor.fetchall():
            print(f"  {league}: {count:,} maç")
            
    except Exception as e:
        print(f"[HATA] İstatistik hatası: {e}")
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()

def export_to_csv(dataframe, filename=None):
    """DataFrame'i CSV dosyasına kaydet"""
    
    if dataframe is None or dataframe.empty:
        print("[HATA] Kaydedilecek veri yok")
        return False
    
    if filename is None:
        filename = f"hamdata_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    try:
        dataframe.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"[OK] Veriler {filename} dosyasına kaydedildi ({len(dataframe):,} kayıt)")
        return True
        
    except Exception as e:
        print(f"[HATA] CSV kayıt hatası: {e}")
        return False

def export_to_excel(dataframe, filename=None):
    """DataFrame'i Excel dosyasına kaydet"""
    
    if dataframe is None or dataframe.empty:
        print("[HATA] Kaydedilecek veri yok")
        return False
    
    if filename is None:
        filename = f"hamdata_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    try:
        dataframe.to_excel(filename, index=False, engine='openpyxl')
        print(f"[OK] Veriler {filename} dosyasına kaydedildi ({len(dataframe):,} kayıt)")
        return True
        
    except Exception as e:
        print(f"[HATA] Excel kayıt hatası: {e}")
        return False

def main():
    """Ana fonksiyon"""
    
    print("[SISTEM] HAMDATA READER")
    print("=" * 60)
    print(f"[ZAMAN] Başlangıç: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Kullanıcı seçimi
    print(f"\n[HEDEF] VERİ ÇEKME SEÇENEKLERİ:")
    print("1. Tüm verileri çek")
    print("2. Belirli tarih")
    print("3. Tarih aralığı")
    print("4. Belirli ülke")
    print("5. Belirli turnuva/lig")
    print("6. En son eklenen veriler")
    print("7. Veritabanı istatistikleri")
    
    choice = input("\nSeçiminizi yapın (1-7): ").strip()
    
    df = None
    
    if choice == "1":
        # Tüm veriler
        df = get_all_data()
        
    elif choice == "2":
        # Belirli tarih
        date_input = input("Tarihi girin (DD/MM/YYYY): ").strip()
        df = get_data_by_date(date_input)
        
    elif choice == "3":
        # Tarih aralığı
        start_date = input("Başlangıç tarihi (DD/MM/YYYY): ").strip()
        end_date = input("Bitiş tarihi (DD/MM/YYYY): ").strip()
        df = get_data_by_date_range(start_date, end_date)
        
    elif choice == "4":
        # Belirli ülke
        country = input("Ülke adını girin: ").strip()
        df = get_data_by_country(country)
        
    elif choice == "5":
        # Belirli turnuva
        league = input("Turnuva/lig adını girin: ").strip()
        df = get_data_by_league(league)
        
    elif choice == "6":
        # En son veriler
        limit_input = input("Kaç kayıt çekilsin? (varsayılan: 1000): ").strip()
        limit = int(limit_input) if limit_input.isdigit() else 1000
        df = get_latest_data(limit)
        
    elif choice == "7":
        # İstatistikler
        get_database_stats()
        return
        
    else:
        print("[HATA] Geçersiz seçim!")
        return
    
    # DataFrame işlemleri
    if df is not None and not df.empty:
        print(f"\n[BASARI] {len(df):,} kayıt başarıyla alındı!")
        
        # Temel bilgiler
        print(f"\n[BILGI] DATAFRAME ÖZET:")
        print(f"   Boyut: {df.shape}")
        print(f"   Sütun sayısı: {len(df.columns)}")
        print(f"   Bellek kullanımı: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
        
        # İlk 5 satırı göster
        print(f"\n[ÖNIZLEME] İlk 5 kayıt:")
        print(df.head().to_string())
        
        # Dışa aktarma seçeneği
        export_choice = input(f"\nVeriyi dosyaya kaydetmek istiyor musunuz? (1=CSV, 2=Excel, 3=Hayır): ").strip()
        
        if export_choice == "1":
            export_to_csv(df)
        elif export_choice == "2":
            export_to_excel(df)
        else:
            print("[BILGI] Veri dosyaya kaydedilmedi")
        
        print(f"\n[BASARI] İşlem tamamlandı!")
        print(f"[BILGI] DataFrame 'df' değişkeninde kullanıma hazır")
        
        # DataFrame'i return et (interaktif kullanım için)
        return df
        
    else:
        print("[HATA] Veri alınamadı")
        return None

if __name__ == "__main__":
    df = main()
