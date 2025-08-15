#!/usr/bin/env python3
"""
Hamdata Tablosu Kontrol Scripti
"""

import psycopg2
from datetime import datetime

def check_hamdata_table():
    """Hamdata tablosunu hızlı kontrol et"""
    
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
        
        print("🔍 HAMDATA KONTROL RAPORU")
        print("="*50)
        print(f"📅 Kontrol Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Tablo varlığını kontrol et
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'hamdata'
            );
        """)
        table_exists = cursor.fetchone()
        
        if not table_exists or not table_exists[0]:
            print("❌ HAMDATA TABLOSU BULUNAMADI!")
            print("   Önce api_fixed_clean.py çalıştırarak tablo oluşturun.")
            return
        
        print("✅ Hamdata tablosu mevcut")
        
        # Toplam kayıt sayısı
        cursor.execute("SELECT COUNT(*) FROM hamdata")
        total_count = cursor.fetchone()
        total = total_count[0] if total_count else 0
        print(f"📊 Toplam Kayıt: {total:,}")
        
        if total == 0:
            print("⚠️ Tabloda hiç veri yok!")
            return
        
        # Son 5 kayıt
        print(f"\n📋 SON EKLENMİŞ 5 KAYIT:")
        cursor.execute("""
            SELECT mac_id, turnuva_adi, ev_sahibi_takim, deplasman_takim, tarih, skor
            FROM hamdata 
            ORDER BY mac_id DESC 
            LIMIT 5
        """)
        recent_matches = cursor.fetchall()
        
        if recent_matches:
            for i, match in enumerate(recent_matches, 1):
                mac_id = match[0] if match[0] else "?"
                turnuva = match[1] if match[1] else "Bilinmiyor"
                ev_takim = match[2] if match[2] else "?"
                dep_takim = match[3] if match[3] else "?"
                tarih = match[4] if match[4] else "?"
                skor = match[5] if match[5] else "?"
                
                print(f"   {i}. {turnuva}")
                print(f"      {ev_takim} vs {dep_takim}")
                print(f"      Tarih: {tarih} | Skor: {skor}")
                print(f"      Mac ID: {mac_id}")
                print()
        
        # Ülke dağılımı (Top 5)
        print("🌍 ÜLKE DAĞILIMI (TOP 5):")
        cursor.execute("""
            SELECT ulke, COUNT(*) as mac_sayisi
            FROM hamdata 
            WHERE ulke IS NOT NULL AND ulke != ''
            GROUP BY ulke 
            ORDER BY mac_sayisi DESC 
            LIMIT 5
        """)
        countries = cursor.fetchall()
        
        if countries:
            for country in countries:
                oran = (country[1] / total) * 100
                print(f"   • {country[0]}: {country[1]:,} maç (%{oran:.1f})")
        
        # Turnuva dağılımı (Top 5)
        print(f"\n🏆 TURNUVA DAĞILIMI (TOP 5):")
        cursor.execute("""
            SELECT turnuva_adi, COUNT(*) as mac_sayisi
            FROM hamdata 
            WHERE turnuva_adi IS NOT NULL AND turnuva_adi != ''
            GROUP BY turnuva_adi 
            ORDER BY mac_sayisi DESC 
            LIMIT 5
        """)
        tournaments = cursor.fetchall()
        
        if tournaments:
            for tournament in tournaments:
                oran = (tournament[1] / total) * 100
                print(f"   • {tournament[0]}: {tournament[1]:,} maç (%{oran:.1f})")
        
        # Tarih aralığı kontrolü
        print(f"\n📆 TARİH ANALİZİ:")
        cursor.execute("""
            SELECT 
                MIN(tarih) as en_eski,
                MAX(tarih) as en_yeni,
                COUNT(DISTINCT tarih) as farkli_gun
            FROM hamdata 
            WHERE tarih IS NOT NULL AND tarih != ''
        """)
        date_info = cursor.fetchone()
        
        if date_info:
            en_eski = date_info[0] if date_info[0] else "Bilinmiyor"
            en_yeni = date_info[1] if date_info[1] else "Bilinmiyor"
            farkli_gun = date_info[2] if date_info[2] else 0
            
            print(f"   📅 En Eski: {en_eski}")
            print(f"   📅 En Yeni: {en_yeni}")
            print(f"   📊 Farklı Gün: {farkli_gun}")
        
        # Veri kalitesi kontrolü
        print(f"\n🔍 VERİ KALİTESİ KONTROLÜ:")
        
        # Boş/null değerler
        critical_fields = ['mac_id', 'ev_sahibi_takim', 'deplasman_takim', 'turnuva_adi']
        
        for field in critical_fields:
            cursor.execute(f"""
                SELECT COUNT(*) 
                FROM hamdata 
                WHERE {field} IS NULL OR {field} = ''
            """)
            null_count = cursor.fetchone()
            null_val = null_count[0] if null_count else 0
            
            if null_val > 0:
                oran = (null_val / total) * 100
                print(f"   ⚠️ {field}: {null_val:,} boş kayıt (%{oran:.1f})")
            else:
                print(f"   ✅ {field}: Tüm kayıtlar dolu")
        
        # Bahis oranları kontrolü
        cursor.execute("""
            SELECT 
                COUNT(CASE WHEN oran_1 IS NOT NULL AND oran_1 != '' THEN 1 END) as oran_1_var,
                COUNT(CASE WHEN oran_x IS NOT NULL AND oran_x != '' THEN 1 END) as oran_x_var,
                COUNT(CASE WHEN oran_2 IS NOT NULL AND oran_2 != '' THEN 1 END) as oran_2_var
            FROM hamdata
        """)
        odds_info = cursor.fetchone()
        
        if odds_info:
            print(f"\n💰 BAHİS ORANLARI:")
            oran_1_oran = (odds_info[0] / total) * 100
            oran_x_oran = (odds_info[1] / total) * 100
            oran_2_oran = (odds_info[2] / total) * 100
            
            print(f"   • Oran 1: {odds_info[0]:,} kayıt (%{oran_1_oran:.1f})")
            print(f"   • Oran X: {odds_info[1]:,} kayıt (%{oran_x_oran:.1f})")
            print(f"   • Oran 2: {odds_info[2]:,} kayıt (%{oran_2_oran:.1f})")
        
        cursor.close()
        pg_conn.close()
        
        print(f"\n{'='*50}")
        print("✅ Hamdata kontrol tamamlandı!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        print(f"Detay: {traceback.format_exc()}")

if __name__ == "__main__":
    check_hamdata_table()
