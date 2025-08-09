# 🏈 Basit Futbol Veri Sistemi

Bu sistem, Mackolik API'sinden futbol maç verilerini çekerek PostgreSQL veritabanına kaydeden **basit ve anlaşılır** bir Python uygulamasıdır.

## 📁 Dosya Yapısı

```
simple_modules/
├── __init__.py              # Paket tanımlama dosyası
├── database.py              # Veritabanı bağlantı modülü
├── api_fetcher.py           # API veri çekme modülü
├── data_processor.py        # Veri işleme modülü
├── database_writer.py       # Veritabanı yazma modülü
└── main_coordinator.py      # Ana koordinatör modülü

simple_start.py              # Sistem başlatma dosyası
README.md                    # Bu dosya
```

## 🔧 Gereksinimler

- Python 3.7+
- psycopg2 (PostgreSQL bağlantısı)
- requests (API çağrıları)

```bash
pip install psycopg2-binary requests
```

## 🚀 Kullanım

### Basit Başlatma
```bash
python simple_start.py
```

### Manuel Kullanım
```python
from simple_modules import MainCoordinator

# Sistemi başlat
coordinator = MainCoordinator()

# Bugünün maçlarını çek
coordinator.fetch_and_save_today()

# Belirli bir tarihi çek
coordinator.fetch_and_save_date("2024-01-15")

# Son 7 günü çek
coordinator.fetch_last_week()
```

### Tek Tek Modül Kullanımı

#### 1. Veritabanı Testi
```python
from simple_modules.database import DatabaseConnection

db = DatabaseConnection()
db.test_connection()
```

#### 2. API Testi
```python
from simple_modules.api_fetcher import APIFetcher

api = APIFetcher()
api.test_api()
api.show_sample_match()
```

#### 3. Veri İşleme Testi
```python
from simple_modules.data_processor import DataProcessor

processor = DataProcessor()
# Test verisi ile dene...
```

## 📊 Modül Açıklamaları

### 🔗 database.py
- **Görev**: Sadece veritabanı bağlantısı
- **Fonksiyonlar**: Bağlan, test et, bağlantıyı kapat
- **Kullanım**: Diğer modüller için temel bağlantı sağlar

### 📥 api_fetcher.py  
- **Görev**: Sadece API'den veri çekmek
- **Fonksiyonlar**: Tarih bazlı maç verisi çekme
- **Kullanım**: Mackolik API'sinden JSON veri alır

### 🔄 data_processor.py
- **Görev**: Sadece veri temizleme ve düzenleme
- **Fonksiyonlar**: Ham veriyi temizle, doğrula
- **Kullanım**: API verisini veritabanı formatına çevirir

### 💾 database_writer.py
- **Görev**: Sadece veritabanına yazma
- **Fonksiyonlar**: UPSERT işlemleri, toplu ekleme
- **Kullanım**: İşlenmiş veriyi hamdata tablosuna kaydeder

### 🎯 main_coordinator.py
- **Görev**: Tüm modülleri koordine etmek
- **Fonksiyonlar**: Tam süreç yönetimi, kullanıcı arayüzü
- **Kullanım**: Sistemin ana kontrol merkezi

## 🎮 Menü Seçenekleri

1. **Bugünün maçlarını çek**: Güncel maçları API'den alır
2. **Belirli tarih için maç çek**: İstediğiniz tarihi girebilirsiniz
3. **Son 7 günün maçlarını çek**: Geçmiş haftalık veri
4. **Sistem kontrolü yap**: Tüm modülleri test eder
5. **Veritabanı bilgilerini göster**: Tablo yapısı ve kayıt sayısı

## ⚙️ Veritabanı Ayarları

`database.py` dosyasındaki ayarları değiştirerek farklı veritabanlarına bağlanabilirsiniz:

```python
self.config = {
    "dbname": "soccerdb",
    "user": "ahmet21", 
    "password": "diclem2121.",
    "host": "165.227.130.23",
    "port": 5432
}
```

## 🛠️ Hata Ayıklama

### API Problemi
```python
from simple_modules.api_fetcher import APIFetcher
api = APIFetcher()
api.test_api()  # API durumunu kontrol et
```

### Veritabanı Problemi
```python
from simple_modules.database import DatabaseConnection
db = DatabaseConnection()
db.test_connection()  # Bağlantıyı test et
```

### Veri İşleme Problemi
```python
from simple_modules.data_processor import DataProcessor
processor = DataProcessor()
# Test verisi ile deneyin
```

## 📈 İstatistikler

Sistem her işlem sonunda detaylı istatistikler verir:
- ✅ Kaç maç eklendi
- 🔄 Kaç maç güncellendi  
- ❌ Kaç hatalar oluştu
- 📊 Başarı oranı

## 🎯 Avantajlar

1. **Modüler Yapı**: Her modül tek bir işle ilgilenir
2. **Kolay Anlama**: Her dosya kısa ve açık
3. **Kolay Test**: Her modül ayrı ayrı test edilebilir
4. **Kolay Geliştirme**: Yeni özellikler kolayca eklenebilir
5. **Hata Ayıklama**: Problemler kolayca bulunabilir

## 🔄 Genişletme

Yeni özellikler eklemek için:

1. **Yeni modül oluştur** (örn: `email_sender.py`)
2. **MainCoordinator'a ekle**
3. **Menüye yeni seçenek ekle**

Bu şekilde sistem büyürken karmaşıklığı kontrolde tutabilirsiniz!

---
🎉 **Artık basit ve anlaşılır bir futbol veri sisteminiz var!**
