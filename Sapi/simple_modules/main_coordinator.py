#!/usr/bin/env python3
"""
Main Coordinator Module - Ana Koordinatör Modülü
Bu modül tüm diğer modülleri koordine eder ve basit arayüz sağlar
"""

from datetime import datetime, timedelta
from typing import Optional

from .api_fetcher import APIFetcher
from .data_processor import DataProcessor  
from .database_writer import DatabaseWriter

class MainCoordinator:
    """Ana koordinatör sınıfı - Tüm işlemleri yönetir"""
    
    def __init__(self):
        """Modülleri başlat"""
        print("🚀 Sistem başlatılıyor...")
        self.api = APIFetcher()
        self.processor = DataProcessor()
        self.writer = DatabaseWriter()
        print("✅ Tüm modüller hazır!")
    
    def fetch_and_save_today(self) -> bool:
        """Bugünün maçlarını çek ve kaydet"""
        print("\n🎯 BUGÜNÜN MAÇLARI İŞLENİYOR")
        print("="*50)
        
        # 1. API'den veri çek
        raw_matches = self.api.fetch_today_matches()
        if not raw_matches:
            print("❌ Bugün için maç verisi bulunamadı")
            return False
        
        # 2. Veriyi işle
        cleaned_matches = self.processor.process_matches_batch(raw_matches)
        if not cleaned_matches:
            print("❌ Veri işleme başarısız")
            return False
        
        # 3. Veritabanına kaydet
        success = self.writer.insert_matches_batch(cleaned_matches)
        
        if success:
            print("🎉 Bugünün maçları başarıyla işlendi!")
            self.processor.show_processing_stats()
            return True
        else:
            print("❌ Veritabanına kaydetme başarısız")
            return False
    
    def fetch_and_save_date(self, date_str: str) -> bool:
        """Belirli bir tarihin maçlarını çek ve kaydet"""
        print(f"\n🎯 {date_str} TARİHİ İŞLENİYOR")
        print("="*50)
        
        # 1. API'den veri çek
        raw_matches = self.api.fetch_matches_for_date(date_str)
        if not raw_matches:
            print(f"❌ {date_str} için maç verisi bulunamadı")
            return False
        
        # 2. Veriyi işle
        cleaned_matches = self.processor.process_matches_batch(raw_matches)
        if not cleaned_matches:
            print("❌ Veri işleme başarısız")
            return False
        
        # 3. Veritabanına kaydet
        success = self.writer.insert_matches_batch(cleaned_matches)
        
        if success:
            print(f"🎉 {date_str} tarihi başarıyla işlendi!")
            self.processor.show_processing_stats()
            return True
        else:
            print("❌ Veritabanına kaydetme başarısız")
            return False
    
    def fetch_last_week(self) -> bool:
        """Son 7 günün maçlarını çek"""
        print("\n🎯 SON 7 GÜNÜN MAÇLARI İŞLENİYOR")
        print("="*50)
        
        today = datetime.now()
        success_count = 0
        
        for i in range(7):
            date = today - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            
            if self.fetch_and_save_date(date_str):
                success_count += 1
            
            print("-" * 30)  # Ayırıcı
        
        print(f"\n📊 {success_count}/7 gün başarıyla işlendi")
        return success_count > 0
    
    def system_check(self) -> bool:
        """Tüm sistemi kontrol et"""
        print("\n🔍 SİSTEM KONTROLÜ")
        print("="*40)
        
        checks_passed = 0
        total_checks = 3
        
        # 1. API kontrolü
        print("1️⃣ API kontrolü...")
        if self.api.test_api():
            checks_passed += 1
        
        # 2. Veritabanı kontrolü
        print("\n2️⃣ Veritabanı kontrolü...")
        if self.writer.check_table_exists():
            checks_passed += 1
        
        # 3. Veri işleme kontrolü
        print("\n3️⃣ Veri işleme kontrolü...")
        test_data = [{
            "id": 99999,
            "date": "2024-01-01T12:00:00",
            "homeTeam": {"id": 1, "name": "Test Home"},
            "awayTeam": {"id": 2, "name": "Test Away"},
            "league": {"id": 1, "name": "Test League"},
            "result": {"homeGoals": 1, "awayGoals": 0},
            "status": "Finished"
        }]
        
        processed = self.processor.process_matches_batch(test_data)
        if processed and len(processed) == 1:
            print("✅ Veri işleme modülü çalışıyor")
            checks_passed += 1
        else:
            print("❌ Veri işleme modülü problemi var")
        
        # Sonuç
        print(f"\n📊 {checks_passed}/{total_checks} kontrol başarılı")
        
        if checks_passed == total_checks:
            print("🎉 Sistem tamamen hazır!")
            return True
        else:
            print("⚠️ Bazı modüllerde problem var")
            return False
    
    def show_menu(self):
        """Basit kullanıcı menüsü"""
        while True:
            print("\n" + "="*50)
            print("🏈 FUTBOL VERİ SİSTEMİ")
            print("="*50)
            print("1. Bugünün maçlarını çek")
            print("2. Belirli tarih için maç çek")
            print("3. Son 7 günün maçlarını çek")
            print("4. Sistem kontrolü yap")
            print("5. Veritabanı bilgilerini göster")
            print("0. Çıkış")
            print("-"*50)
            
            choice = input("Seçiminiz (0-5): ").strip()
            
            if choice == "1":
                self.fetch_and_save_today()
            
            elif choice == "2":
                date_input = input("Tarih (YYYY-MM-DD): ").strip()
                if date_input:
                    self.fetch_and_save_date(date_input)
                else:
                    print("❌ Geçersiz tarih formatı")
            
            elif choice == "3":
                self.fetch_last_week()
            
            elif choice == "4":
                self.system_check()
            
            elif choice == "5":
                self.writer.get_table_info()
            
            elif choice == "0":
                print("👋 Sistem kapatılıyor...")
                break
            
            else:
                print("❌ Geçersiz seçim!")
            
            input("\nDevam etmek için Enter'a basın...")

# Test fonksiyonu
if __name__ == "__main__":
    print("🧪 ANA KOORDİNATÖR TESTİ")
    print("="*40)
    
    coordinator = MainCoordinator()
    
    # Sistem kontrolü yap
    if coordinator.system_check():
        print("\n🎉 Ana koordinatör hazır!")
        print("💡 coordinator.show_menu() ile menüyü başlatabilirsiniz")
    else:
        print("❌ Sistem problemleri var!")
