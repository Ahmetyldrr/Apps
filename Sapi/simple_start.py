#!/usr/bin/env python3
"""
Simple Start - Basit Başlangıç Dosyası
Bu dosya sistemi başlatmak için kullanılır
"""

from simple_modules.main_coordinator import MainCoordinator

def main():
    """Ana fonksiyon"""
    print("🏈 FUTBOL VERİ SİSTEMİ BAŞLATILIYOR")
    print("="*50)
    
    try:
        # Ana koordinatörü başlat
        coordinator = MainCoordinator()
        
        # Sistem kontrolü yap
        if coordinator.system_check():
            print("\n✅ Sistem hazır! Menü başlatılıyor...")
            coordinator.show_menu()
        else:
            print("\n❌ Sistem kontrolü başarısız!")
            print("Lütfen aşağıdaki adımları kontrol edin:")
            print("1. Internet bağlantınız var mı?")
            print("2. Veritabanı bilgileri doğru mu?")
            print("3. Gerekli Python kütüphaneleri yüklü mü?")
            
    except KeyboardInterrupt:
        print("\n\n👋 Kullanıcı tarafından durduruldu")
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        print("Sistem yeniden başlatılmayı deniyor...")

if __name__ == "__main__":
    main()
