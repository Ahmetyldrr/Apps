#!/usr/bin/env python3
"""
Basit API Script - Minimal Mackolik API Testi
Sadece API bağlantısını test eder ve basit veri çeker
"""

import http.client
import json
from datetime import datetime

def minimal_api_test():
    """En basit API testi"""
    
    print("🌐 MİNİMAL API TEST")
    print("="*30)
    
    # Bugünün tarihi
    today = datetime.now().strftime("%d/%m/%Y")
    
    try:
        print(f"📅 {today} tarihi test ediliyor...")
        
        # Basit bağlantı
        conn = http.client.HTTPSConnection('vd.mackolik.com')
        headers = {
            'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        conn.request('GET', f'/livedata?date={today}', headers=headers)
        response = conn.getresponse()
        
        print(f"📡 Response: {response.status}")
        
        if response.status == 200:
            data = response.read()
            json_data = json.loads(data)
            matches = json_data.get("m", [])
            
            print(f"✅ {len(matches)} maç bulundu")
            
            # İlk maçı göster
            if matches:
                first_match = matches[0]
                print(f"\n📋 İLK MAÇ ÖRNEĞİ:")
                print(f"   Mac ID: {first_match[0] if len(first_match) > 0 else '?'}")
                print(f"   Ev Takım: {first_match[2] if len(first_match) > 2 else '?'}")
                print(f"   Dep Takım: {first_match[4] if len(first_match) > 4 else '?'}")
                print(f"   Skor: {first_match[7] if len(first_match) > 7 else '?'}")
                print(f"   Toplam Sütun: {len(first_match)}")
                
                # Turnuva bilgisi var mı?
                if len(first_match) > 36 and isinstance(first_match[36], list):
                    turnuva_info = first_match[36]
                    print(f"   Turnuva Bilgisi: {len(turnuva_info)} eleman")
                    if len(turnuva_info) > 3:
                        print(f"   Turnuva Adı: {turnuva_info[3]}")
                
        else:
            print(f"❌ Hata: {response.status}")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")

def simple_data_structure_check():
    """Basit veri yapısı kontrolü"""
    
    print(f"\n🔍 VERİ YAPISI KONTROLÜ")
    print("="*30)
    
    today = datetime.now().strftime("%d/%m/%Y")
    
    try:
        conn = http.client.HTTPSConnection('vd.mackolik.com')
        headers = {'user-agent': 'Mozilla/5.0'}
        
        conn.request('GET', f'/livedata?date={today}', headers=headers)
        response = conn.getresponse()
        
        if response.status == 200:
            data = response.read()
            json_data = json.loads(data)
            matches = json_data.get("m", [])
            
            if matches:
                print(f"📊 Toplam Maç: {len(matches)}")
                
                # Sütun sayıları
                column_counts = [len(match) for match in matches]
                min_cols = min(column_counts)
                max_cols = max(column_counts)
                avg_cols = sum(column_counts) / len(column_counts)
                
                print(f"📈 Sütun Sayıları:")
                print(f"   • Minimum: {min_cols}")
                print(f"   • Maksimum: {max_cols}")
                print(f"   • Ortalama: {avg_cols:.1f}")
                
                # İlk maçın detayları
                first_match = matches[0]
                print(f"\n🎯 İLK MAÇIN ÖZELLİKLERİ:")
                
                # Önemli indeksleri kontrol et
                important_indices = [0, 1, 2, 3, 4, 7, 16, 35, 36]
                labels = ['Mac ID', 'Ev ID', 'Ev Takım', 'Dep ID', 'Dep Takım', 
                         'Skor', 'Saat', 'Tarih', 'Turnuva Info']
                
                for i, label in zip(important_indices, labels):
                    if i < len(first_match):
                        value = first_match[i]
                        if isinstance(value, list):
                            print(f"   • {label} [{i}]: Liste ({len(value)} eleman)")
                        else:
                            value_str = str(value)[:50]  # İlk 50 karakter
                            print(f"   • {label} [{i}]: {value_str}")
                    else:
                        print(f"   • {label} [{i}]: İndeks bulunamadı")
                
        conn.close()
        
    except Exception as e:
        print(f"❌ Hata: {e}")

def quick_connectivity_test():
    """Hızlı bağlantı testi"""
    
    print(f"\n⚡ HIZLI BAĞLANTI TESTİ")
    print("="*30)
    
    try:
        start_time = datetime.now()
        
        conn = http.client.HTTPSConnection('vd.mackolik.com', timeout=10)
        conn.request('GET', '/livedata?date=10/08/2025')
        response = conn.getresponse()
        
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds() * 1000
        
        print(f"📡 Status: {response.status}")
        print(f"⚡ Response Time: {response_time:.2f}ms")
        
        if response.status == 200:
            print("✅ Bağlantı başarılı")
        else:
            print("⚠️ Bağlantı problemli")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Bağlantı başarısız: {e}")

def test_different_dates():
    """Farklı tarihleri test et"""
    
    print(f"\n📅 FARKLI TARİHLER TESTİ")
    print("="*30)
    
    test_dates = [
        "09/08/2025",  # Dün
        "10/08/2025",  # Bugün 
        "11/08/2025",  # Yarın
        "05/08/2025",  # 5 gün önce
        "01/08/2025"   # Ay başı
    ]
    
    for date in test_dates:
        try:
            conn = http.client.HTTPSConnection('vd.mackolik.com')
            headers = {'user-agent': 'Mozilla/5.0'}
            
            conn.request('GET', f'/livedata?date={date}', headers=headers)
            response = conn.getresponse()
            
            if response.status == 200:
                data = response.read()
                json_data = json.loads(data)
                matches = json_data.get("m", [])
                print(f"   • {date}: {len(matches)} maç")
            else:
                print(f"   • {date}: HTTP {response.status}")
            
            conn.close()
            
        except Exception as e:
            print(f"   • {date}: Hata - {str(e)[:50]}")

def main():
    """Ana fonksiyon"""
    
    print("🚀 BASİT API SCRIPT")
    print("="*40)
    print(f"🕒 Zaman: {datetime.now().strftime('%H:%M:%S')}")
    
    # Testleri sırayla çalıştır
    minimal_api_test()
    simple_data_structure_check()
    quick_connectivity_test()
    test_different_dates()
    
    print(f"\n🎉 Tüm testler tamamlandı!")
    print(f"🕒 Bitiş: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
