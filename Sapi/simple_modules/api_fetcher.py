#!/usr/bin/env python3
"""
API Fetcher Module - API Çekme Modülü
Bu modül sadece Mackolik API'sından veri çekmekle ilgilenir
"""

import requests
import json
from datetime import datetime

class APIFetcher:
    """Basit API veri çekme sınıfı"""
    
    def __init__(self):
        """API ayarları"""
        self.base_url = "https://vd.mackolik.com/api/matches/by-date"
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def fetch_matches_for_date(self, date_str: str):
        """Belirtilen tarih için maçları çek"""
        try:
            print(f"📥 {date_str} tarihi için veri çekiliyor...")
            
            # URL oluştur
            url = f"{self.base_url}/{date_str}"
            
            # API'ye istek gönder
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get("data", [])
                print(f"✅ {len(matches)} maç verisi alındı")
                return matches
            else:
                print(f"❌ API hatası: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Veri çekme hatası: {e}")
            return []
    
    def fetch_today_matches(self):
        """Bugünün maçlarını çek"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.fetch_matches_for_date(today)
    
    def test_api(self):
        """API bağlantısını test et"""
        try:
            print("🧪 API testi yapılıyor...")
            matches = self.fetch_today_matches()
            if matches:
                print(f"✅ API çalışıyor! {len(matches)} maç bulundu")
                return True
            else:
                print("⚠️ API çalışıyor ama veri yok")
                return True
        except Exception as e:
            print(f"❌ API test hatası: {e}")
            return False
    
    def show_sample_match(self):
        """Örnek maç verisini göster"""
        matches = self.fetch_today_matches()
        if matches:
            print("\n📊 ÖRNEK MAÇ VERİSİ:")
            print("="*40)
            first_match = matches[0]
            
            # Temel bilgileri göster
            print(f"ID: {first_match.get('id', 'N/A')}")
            print(f"Tarih: {first_match.get('date', 'N/A')}")
            print(f"Durum: {first_match.get('status', 'N/A')}")
            
            # Takım bilgilerini göster
            home_team = first_match.get("homeTeam", {})
            away_team = first_match.get("awayTeam", {})
            print(f"Ev Sahibi: {home_team.get('name', 'N/A')}")
            print(f"Deplasman: {away_team.get('name', 'N/A')}")
            
            # Skor bilgilerini göster
            result = first_match.get("result", {})
            print(f"Skor: {result.get('homeGoals', 0)} - {result.get('awayGoals', 0)}")
            
            print("\n🔍 Tüm alanlar:")
            for key in first_match.keys():
                print(f"  - {key}")
        else:
            print("❌ Gösterilecek maç verisi yok")

# Test fonksiyonu
if __name__ == "__main__":
    print("🧪 API ÇEKME TESTİ")
    print("="*40)
    
    api = APIFetcher()
    if api.test_api():
        print("🎉 API modülü çalışıyor!")
        api.show_sample_match()
    else:
        print("❌ API modülü problemi var!")
