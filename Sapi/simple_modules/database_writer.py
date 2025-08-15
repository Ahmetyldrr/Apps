#!/usr/bin/env python3
"""
Database Writer Module - Veritabanı Yazma Modülü
Bu modül sadece veritabanına veri yazmakla ilgilenir
"""

from typing import List, Dict, Any
from .database import DatabaseConnection

class DatabaseWriter:
    """Basit veritabanı yazma sınıfı"""
    
    def __init__(self):
        """Veritabanı yazma ayarları"""
        self.db = DatabaseConnection()
        self.inserted_count = 0
        self.updated_count = 0
        self.error_count = 0
    
    def insert_match(self, match_data: Dict[str, Any]) -> bool:
        """Tek bir maçı veritabanına ekle"""
        try:
            if not self.db.cursor:
                print("❌ Veritabanı bağlantısı yok")
                return False
            
            # UPSERT sorgusu (varsa güncelle, yoksa ekle)
            query = """
            INSERT INTO hamdata (
                match_id, match_date, match_time, 
                home_team_id, home_team_name, 
                away_team_id, away_team_name,
                league_id, league_name,
                home_goals, away_goals, status, week, season
            ) VALUES (
                %(match_id)s, %(match_date)s, %(match_time)s,
                %(home_team_id)s, %(home_team_name)s,
                %(away_team_id)s, %(away_team_name)s,
                %(league_id)s, %(league_name)s,
                %(home_goals)s, %(away_goals)s, %(status)s, %(week)s, %(season)s
            )
            ON CONFLICT (match_id) 
            DO UPDATE SET
                home_goals = EXCLUDED.home_goals,
                away_goals = EXCLUDED.away_goals,
                status = EXCLUDED.status,
                updated_at = CURRENT_TIMESTAMP
            """
            
            # Sorguyu çalıştır
            self.db.cursor.execute(query, match_data)
            
            # Eklenen veya güncellenen satır sayısını kontrol et
            if self.db.cursor.rowcount > 0:
                if self.db.cursor.rowcount == 1:
                    # Check if it was an insert or update
                    self.db.cursor.execute(
                        "SELECT created_at, updated_at FROM hamdata WHERE match_id = %s",
                        (match_data['match_id'],)
                    )
                    row = self.db.cursor.fetchone()
                    if row and row[0] == row[1]:  # created_at == updated_at means insert
                        self.inserted_count += 1
                    else:
                        self.updated_count += 1
                
                return True
            else:
                self.error_count += 1
                return False
                
        except Exception as e:
            print(f"❌ Veri ekleme hatası: {e}")
            self.error_count += 1
            return False
    
    def insert_matches_batch(self, matches_data: List[Dict[str, Any]]) -> bool:
        """Maç listesini toplu olarak veritabanına ekle"""
        if not matches_data:
            print("⚠️ Eklenecek veri yok")
            return False
        
        print(f"💾 {len(matches_data)} maç veritabanına ekleniyor...")
        
        # Veritabanına bağlan
        if not self.db.connect():
            return False
        
        try:
            # İstatistikleri sıfırla
            self.inserted_count = 0
            self.updated_count = 0
            self.error_count = 0
            
            # Her maçı tek tek işle
            for match_data in matches_data:
                self.insert_match(match_data)
            
            # Değişiklikleri kaydet
            if self.db.connection:
                self.db.connection.commit()
            
            # Sonuçları göster
            print(f"✅ {self.inserted_count} yeni maç eklendi")
            print(f"🔄 {self.updated_count} maç güncellendi")
            if self.error_count > 0:
                print(f"❌ {self.error_count} hata oluştu")
            
            return True
            
        except Exception as e:
            print(f"❌ Toplu ekleme hatası: {e}")
            if self.db.connection:
                self.db.connection.rollback()
            return False
        finally:
            self.db.disconnect()
    
    def check_table_exists(self) -> bool:
        """hamdata tablosunun var olup olmadığını kontrol et"""
        try:
            if not self.db.connect():
                return False
            
            if self.db.cursor:
                self.db.cursor.execute("""
                    SELECT EXISTS (
                        SELECT 1 FROM information_schema.tables 
                        WHERE table_name = 'hamdata'
                    )
                """)
                result = self.db.cursor.fetchone()
                exists = result[0] if result else False
                
                if exists:
                    print("✅ hamdata tablosu mevcut")
                else:
                    print("❌ hamdata tablosu bulunamadı")
                
                return exists
            else:
                return False
                
        except Exception as e:
            print(f"❌ Tablo kontrol hatası: {e}")
            return False
        finally:
            self.db.disconnect()
    
    def get_table_info(self):
        """hamdata tablosu hakkında bilgi al"""
        try:
            if not self.db.connect():
                return
            
            if self.db.cursor:
                # Tablo yapısını al
                self.db.cursor.execute("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = 'hamdata'
                    ORDER BY ordinal_position
                """)
                
                columns = self.db.cursor.fetchall()
                
                print("\n📊 HAMDATA TABLO YAPISI:")
                print("="*50)
                for col in columns:
                    print(f"  {col[0]} ({col[1]}) - Null: {col[2]}")
                
                # Kayıt sayısını al
                total_count = self.db.get_table_count("hamdata")
                print(f"\n📈 Toplam kayıt sayısı: {total_count}")
                
        except Exception as e:
            print(f"❌ Tablo bilgi hatası: {e}")
        finally:
            self.db.disconnect()

# Test fonksiyonu
if __name__ == "__main__":
    print("🧪 VERİTABANI YAZMA TESTİ")
    print("="*40)
    
    writer = DatabaseWriter()
    
    # Tablo kontrolü
    if writer.check_table_exists():
        writer.get_table_info()
        print("🎉 Veritabanı yazma modülü hazır!")
    else:
        print("❌ hamdata tablosu bulunamadı!")
