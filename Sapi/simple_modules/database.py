#!/usr/bin/env python3
"""
Database Connection Module - Veritabanı Bağlantı Modülü
Bu modül sadece veritabanı bağlantısı ile ilgilenir
"""

import psycopg2
from typing import Optional

class DatabaseConnection:
    """Basit veritabanı bağlantı sınıfı"""
    
    def __init__(self):
        """Veritabanı ayarları"""
        self.config = {
            "dbname": "soccerdb",
            "user": "ahmet21", 
            "password": "diclem2121.",
            "host": "165.227.130.23",
            "port": 5432  # int olarak
        }
        self.connection: Optional[psycopg2.extensions.connection] = None
        self.cursor: Optional[psycopg2.extensions.cursor] = None
    
    def connect(self):
        """Veritabanına bağlan"""
        try:
            print("🔗 Veritabanına bağlanılıyor...")
            self.connection = psycopg2.connect(**self.config)
            self.cursor = self.connection.cursor()
            print("✅ Bağlantı başarılı!")
            return True
        except Exception as e:
            print(f"❌ Bağlantı hatası: {e}")
            return False
    
    def disconnect(self):
        """Bağlantıyı kapat"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("🔐 Bağlantı kapatıldı")
    
    def test_connection(self):
        """Bağlantıyı test et"""
        if self.connect():
            try:
                if self.cursor:
                    self.cursor.execute("SELECT 1")
                    result = self.cursor.fetchone()
                    if result:
                        print("✅ Bağlantı testi başarılı!")
                        return True
            except Exception as e:
                print(f"❌ Test hatası: {e}")
                return False
            finally:
                self.disconnect()
        return False
    
    def get_table_count(self, table_name):
        """Tablo kayıt sayısını al"""
        try:
            if self.cursor:
                self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                result = self.cursor.fetchone()
                return result[0] if result else 0
        except Exception as e:
            print(f"❌ Tablo sayım hatası: {e}")
            return 0

# Test fonksiyonu
if __name__ == "__main__":
    print("🧪 VERİTABANI BAĞLANTI TESTİ")
    print("="*40)
    
    db = DatabaseConnection()
    if db.test_connection():
        print("🎉 Modül çalışıyor!")
    else:
        print("❌ Modül problemi var!")
