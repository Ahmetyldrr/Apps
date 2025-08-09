#!/usr/bin/env python3
"""
Basit API Test Scripti
"""

import http.client
import json
from datetime import datetime

def simple_api_test():
    """Basit API testi"""
    print("🌐 BASİT API TEST")
    print("="*30)
    
    datex = "10/08/2025"  # Bugünün tarihi
    
    try:
        print(f"📅 {datex} tarihli veriler test ediliyor...")
        
        conn = http.client.HTTPSConnection('vd.mackolik.com')
        headers = {
            'accept': '*/*',
            'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://arsiv.mackolik.com',
            'referer': 'https://arsiv.mackolik.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        }
        
        conn.request('GET', f'/livedata?date={datex}', headers=headers)
        response = conn.getresponse()
        
        print(f"📡 HTTP Status: {response.status}")
        
        if response.status == 200:
            data = response.read()
            
            try:
                json_data = json.loads(data)
                matches = json_data.get("m", [])
                
                if matches:
                    print(f"✅ {len(matches)} adet maç verisi bulundu")
                    
                    # İlk 3 maçı göster
                    print(f"\n📋 İLK 3 MAÇ:")
                    for i, match in enumerate(matches[:3], 1):
                        try:
                            # Turnuva bilgisi
                            turnuva_info = match[36] if len(match) > 36 else []
                            turnuva_adi = str(turnuva_info[3]) if len(turnuva_info) > 3 else "Bilinmiyor"
                            
                            ev_takim = str(match[2]) if len(match) > 2 else "?"
                            dep_takim = str(match[4]) if len(match) > 4 else "?"
                            skor = str(match[7]) if len(match) > 7 else "?"
                            saat = str(match[16]) if len(match) > 16 else "?"
                            
                            print(f"   {i}. {turnuva_adi}")
                            print(f"      {ev_takim} vs {dep_takim}")
                            print(f"      Saat: {saat} | Skor: {skor}")
                            print()
                            
                        except Exception as e:
                            print(f"   {i}. Maç verisi okunamadı: {e}")
                    
                    # Veri yapısını analiz et
                    print(f"🔍 VERİ YAPISI ANALİZİ:")
                    if matches:
                        first_match = matches[0]
                        print(f"   • Her maç {len(first_match)} sütuna sahip")
                        
                        # Turnuva bilgisini kontrol et
                        if len(first_match) > 36:
                            turnuva_raw = first_match[36]
                            if isinstance(turnuva_raw, list):
                                print(f"   • Turnuva bilgisi {len(turnuva_raw)} elemanlı liste")
                            else:
                                print(f"   • Turnuva bilgisi tipi: {type(turnuva_raw)}")
                    
                    # Ortalama sütun sayısı
                    total_columns = sum(len(match) for match in matches)
                    avg_columns = total_columns / len(matches)
                    print(f"   • Ortalama sütun sayısı: {avg_columns:.1f}")
                    
                else:
                    print("⚠️ Maç verisi bulunamadı (boş liste)")
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON parse hatası: {e}")
                print(f"İlk 100 karakter: {data[:100]}")
                
        else:
            print(f"❌ API hatası: HTTP {response.status}")
            print(f"Response: {response.read()[:200]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
    
    print(f"\n🕒 Test zamanı: {datetime.now().strftime('%H:%M:%S')}")
    print("🎉 Basit API test tamamlandı!")

def test_different_dates():
    """Farklı tarihleri test et"""
    print(f"\n📅 FARKLI TARİHLERİ TEST")
    print("="*30)
    
    test_dates = [
        "09/08/2025",  # Dün
        "10/08/2025",  # Bugün 
        "11/08/2025",  # Yarın
        "01/01/2025",  # Yılbaşı
        "25/12/2024"   # Geçen yıl
    ]
    
    for date in test_dates:
        try:
            conn = http.client.HTTPSConnection('vd.mackolik.com')
            headers = {
                'accept': '*/*',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
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
            print(f"   • {date}: Hata - {e}")

if __name__ == "__main__":
    simple_api_test()
    test_different_dates()
