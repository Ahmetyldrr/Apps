#!/usr/bin/env python3
"""
Data Processor Module - Veri İşleme Modülü
Bu modül API'den gelen verileri temizlemek ve düzenlemekle ilgilenir
"""

from datetime import datetime
from typing import List, Dict, Any, Optional

class DataProcessor:
    """Basit veri işleme sınıfı"""
    
    def __init__(self):
        """Veri işleme ayarları"""
        self.processed_count = 0
        self.error_count = 0
    
    def clean_match_data(self, raw_match: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Tek bir maç verisini temizle ve düzenle"""
        try:
            # Temel bilgileri al
            match_id = raw_match.get("id")
            if not match_id:
                return None
            
            # Tarih ve saat bilgilerini işle
            date_str = raw_match.get("date", "")
            match_datetime = self._parse_datetime(date_str)
            
            # Takım bilgilerini al
            home_team = raw_match.get("homeTeam", {})
            away_team = raw_match.get("awayTeam", {})
            
            # Lig bilgilerini al
            league = raw_match.get("league", {})
            
            # Skor bilgilerini al
            result = raw_match.get("result", {})
            
            # Temizlenmiş veri yapısı
            cleaned_data = {
                "match_id": match_id,
                "match_date": match_datetime.strftime("%Y-%m-%d") if match_datetime else None,
                "match_time": match_datetime.strftime("%H:%M:%S") if match_datetime else None,
                "home_team_id": home_team.get("id"),
                "home_team_name": home_team.get("name", "").strip(),
                "away_team_id": away_team.get("id"),
                "away_team_name": away_team.get("name", "").strip(),
                "league_id": league.get("id"),
                "league_name": league.get("name", "").strip(),
                "home_goals": result.get("homeGoals", 0),
                "away_goals": result.get("awayGoals", 0),
                "status": raw_match.get("status", "").strip(),
                "week": raw_match.get("week"),
                "season": raw_match.get("season")
            }
            
            self.processed_count += 1
            return cleaned_data
            
        except Exception as e:
            print(f"❌ Veri temizleme hatası: {e}")
            self.error_count += 1
            return None
    
    def process_matches_batch(self, raw_matches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Maç listesini toplu olarak işle"""
        print(f"🔄 {len(raw_matches)} maç verisi işleniyor...")
        
        cleaned_matches = []
        self.processed_count = 0
        self.error_count = 0
        
        for raw_match in raw_matches:
            cleaned_match = self.clean_match_data(raw_match)
            if cleaned_match:
                cleaned_matches.append(cleaned_match)
        
        print(f"✅ {self.processed_count} maç işlendi, {self.error_count} hata")
        return cleaned_matches
    
    def _parse_datetime(self, date_str: str) -> Optional[datetime]:
        """Tarih string'ini datetime objesine çevir"""
        if not date_str:
            return None
        
        try:
            # Farklı tarih formatlarını dene
            formats = [
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d"
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_str[:len(fmt)], fmt)
                except ValueError:
                    continue
            
            print(f"⚠️ Tarih formatı tanınmadı: {date_str}")
            return None
            
        except Exception as e:
            print(f"❌ Tarih parse hatası: {e}")
            return None
    
    def validate_match_data(self, match_data: Dict[str, Any]) -> bool:
        """Maç verisinin geçerli olup olmadığını kontrol et"""
        required_fields = ["match_id", "home_team_name", "away_team_name"]
        
        for field in required_fields:
            if not match_data.get(field):
                print(f"❌ Eksik alan: {field}")
                return False
        
        return True
    
    def show_processing_stats(self):
        """İşleme istatistiklerini göster"""
        print(f"\n📊 İŞLEME İSTATİSTİKLERİ:")
        print(f"✅ İşlenen: {self.processed_count}")
        print(f"❌ Hatalı: {self.error_count}")
        total = self.processed_count + self.error_count
        if total > 0:
            success_rate = (self.processed_count / total) * 100
            print(f"📈 Başarı Oranı: %{success_rate:.1f}")

# Test fonksiyonu
if __name__ == "__main__":
    print("🧪 VERİ İŞLEME TESTİ")
    print("="*40)
    
    # Test verisi
    test_match = {
        "id": 12345,
        "date": "2024-01-15T15:00:00",
        "homeTeam": {"id": 1, "name": "Galatasaray"},
        "awayTeam": {"id": 2, "name": "Fenerbahçe"},
        "league": {"id": 1, "name": "Süper Lig"},
        "result": {"homeGoals": 2, "awayGoals": 1},
        "status": "Finished",
        "week": 20,
        "season": "2023-24"
    }
    
    processor = DataProcessor()
    cleaned = processor.clean_match_data(test_match)
    
    if cleaned:
        print("🎉 Veri işleme başarılı!")
        print("\n📊 Temizlenmiş veri:")
        for key, value in cleaned.items():
            print(f"  {key}: {value}")
    else:
        print("❌ Veri işleme başarısız!")
