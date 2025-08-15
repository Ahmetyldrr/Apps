# Football Data Analysis Project

Bu proje Mackolik'ten futbol maç verilerini çekip PostgreSQL veritabanına kaydeden ve analiz eden bir Python uygulamasıdır.

## Dosyalar

- `api.py`: Tek tarih için veri çeken script
- `api_multi.py`: Birden fazla tarih için veri çeken script  
- `fetch_data.py`: Veritabanından veri çeken ve analiz eden script
- `r_count.py`: Veritabanındaki kayıt sayısını kontrol eden script

## Kurulum

### GitHub Codespaces ile (Önerilen)

1. Bu repository'yi GitHub'da açın
2. "Code" butonuna tıklayın
3. "Codespaces" sekmesini seçin
4. "Create codespace on main" butonuna tıklayın
5. Codespace açıldıktan sonra gerekli paketler otomatik olarak yüklenecek

### Yerel Kurulum

```bash
pip install -r requirements.txt
```

## Kullanım

### Veri Çekme

```python
# Tek tarih için
python api.py

# Birden fazla tarih için
python api_multi.py
```

### Veritabanından Veri Okuma

```python
from fetch_data import fetch_data_from_db, get_latest_matches, search_team_matches

# Tüm verileri çek (ilk 100 kayıt)
df = fetch_data_from_db(limit=100)

# Son 7 günün verilerini çek
recent_matches = get_latest_matches(7)

# Belirli takımı ara
team_data = search_team_matches("Galatasaray")
```

### Kayıt Sayısını Kontrol Etme

```python
python r_count.py
```

## Veritabanı Bağlantısı

Proje PostgreSQL veritabanı kullanmaktadır. Bağlantı bilgileri kodun içinde tanımlanmıştır.

## GitHub Codespaces Avantajları

- Bulut tabanlı geliştirme ortamı
- Otomatik paket kurulumu
- VS Code entegrasyonu
- İnternet üzerinden veritabanı erişimi
- Platformdan bağımsız çalışma

## Önemli Notlar

- Veritabanı bağlantı bilgileri güvenlik açısından environment variables olarak kullanılmalıdır
- API çağrıları için rate limiting dikkate alınmalıdır
- Büyük veri setleri için chunk'lı okuma önerilir
