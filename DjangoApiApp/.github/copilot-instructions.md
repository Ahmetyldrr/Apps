# DjangoApiApp - Kapsamlı Geliştirici Kılavuzu

## 🏗️ Proje Genel Yapısı ve Mimari

### Proje Hiyerarşisi
```
DjangoApiApp/
├── manage.py                    # Django'nun ana komut arayüzü
├── db.sqlite3                   # SQLite veritabanı dosyası
├── forecast_api/                # Ana proje konfigürasyonu
│   ├── __init__.py
│   ├── settings.py              # Proje ayarları (KRITIK)
│   ├── urls.py                  # Ana URL yönlendirmeleri
│   ├── wsgi.py                  # WSGI server konfigürasyonu
│   └── asgi.py                  # ASGI server konfigürasyonu
└── data_generator/              # Ana uygulama modülü
    ├── models.py                # Veri modelleri (ForecastData)
    ├── views.py                 # İş mantığı ve API endpoint'leri
    ├── urls.py                  # Uygulama URL'leri
    ├── serializers.py           # REST API serializers
    ├── admin.py                 # Django admin konfigürasyonu
    ├── apps.py                  # Uygulama konfigürasyonu
    ├── tests.py                 # Unit testler (boş)
    ├── migrations/              # Veritabanı migrasyon dosyaları
    │   ├── 0001_initial.py      # İlk migrasyon
    │   └── __init__.py
    └── templates/data_generator/
        └── forecast_dashboard.html  # Dashboard HTML template'i
```

### Mimari Prensipleri
- **Monolitik Django Yapısı**: Tek proje altında organizasyon
- **MVT Pattern**: Model-View-Template Django design pattern'i
- **REST API + Web Dashboard**: Hibrit yaklaşım (API + geleneksel web)
- **SQLite Backend**: Geliştirme için hafif veritabanı çözümü

## 🔧 Teknoloji Stack'i ve Bağımlılıklar

### Core Framework
- **Django 5.2.4**: Ana web framework
- **Django REST Framework**: API geliştirme için
- **SQLite**: Veritabanı (production'da PostgreSQL önerilir)

### Veri İşleme Kütüphaneleri
- **pandas**: Excel dosya oluşturma ve veri manipülasyonu
- **xlsxwriter**: Excel dosya yazma motoru
- **random**: Sentetik veri üretimi
- **datetime**: Tarih işlemleri

### Kurulum Gereksinimleri
```bash
pip install django==5.2.4
pip install djangorestframework
pip install pandas
pip install xlsxwriter
```

## 📊 Veri Modeli ve Veritabanı Yapısı

### ForecastData Modeli Detayları
```python
# data_generator/models.py
class ForecastData(models.Model):
    product_name = models.CharField(max_length=100)     # Ürün adı
    forecast_date = models.DateField()                  # Tahmin tarihi
    sales_forecast = models.IntegerField()              # Satış tahmini (sayısal)
    
    def __str__(self):
        return f"{self.product_name} - {self.forecast_date}"
```

### Veritabanı İşlemleri
- **Tablo Adı**: `data_generator_forecastdata`
- **Primary Key**: Otomatik ID (BigAutoField)
- **İndeksler**: Tarih bazlı sorgular için forecast_date önerilir
- **Veri Hacmi**: 100 kayıt/seferlik batch işlem

### Migrasyon Stratejisi
```bash
# Yeni migrasyon oluşturma
python manage.py makemigrations data_generator

# Migrasyonları uygulama
python manage.py migrate

# Migrasyon durumunu kontrol etme
python manage.py showmigrations
```

## 🌐 API Endpoint'leri ve URL Yapısı

### URL Routing Hiyerarşisi
```
forecast_api/urls.py (Ana routing)
├── /admin/                      → Django Admin Panel
└── /api/                        → data_generator.urls include
    ├── /api/                    → ForecastDashboardView (Dashboard)
    ├── /api/generate-forecast/  → GenerateForecastView (Veri üretimi)
    └── /api/download-forecast/  → DownloadForecastView (Excel indirme)
```

### API Endpoint Detayları

#### 1. Dashboard Endpoint (`/api/`)
- **View**: `ForecastDashboardView`
- **Method**: GET
- **Return**: HTML template render
- **Context**: Tüm ForecastData kayıtları (tarih sıralı)
- **Template**: `data_generator/forecast_dashboard.html`

#### 2. Veri Üretimi Endpoint (`/api/generate-forecast/`)
- **View**: `GenerateForecastView`
- **Method**: GET (POST değil - önemli!)
- **İş Akışı**:
  1. Mevcut tüm verileri sil (`ForecastData.objects.all().delete()`)
  2. 100 adet rastgele veri üret (`generate_synthetic_data()`)
  3. Dashboard'a redirect (`redirect('forecast-dashboard')`)
- **Veri Üretim Algoritması**:
  ```python
  product_names = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
  forecast_date = bugün + random(1-90 gün)
  sales_forecast = random(50-1000)
  ```

#### 3. Excel İndirme Endpoint (`/api/download-forecast/`)
- **View**: `DownloadForecastView`
- **Method**: GET
- **Return**: Excel dosyası (binary stream)
- **Dosya Adı**: `forecast_data.xlsx`
- **İş Akışı**:
  1. Veritabanından tüm verileri çek
  2. Pandas DataFrame'e çevir
  3. XlsxWriter ile Excel oluştur
  4. HTTP response olarak stream et

## 🔄 İş Akışları ve Süreçler

### Geliştirici İş Akışı (Developer Workflow)

#### 1. Proje Başlatma
```bash
# Sanal ortam oluşturma (önerilir)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Bağımlılıkları kurma
pip install -r requirements.txt  # Eğer varsa

# Veritabanını hazırlama
python manage.py migrate

# Admin kullanıcısı oluşturma
python manage.py createsuperuser

# Sunucuyu başlatma
python manage.py runserver
```

#### 2. Geliştirme Döngüsü
1. **Model değişiklikleri**: `models.py` düzenle
2. **Migrasyon oluştur**: `python manage.py makemigrations`
3. **Migrasyonu uygula**: `python manage.py migrate`
4. **View'ları test et**: Tarayıcıda `/api/` kontrol et
5. **Admin panelinde veri kontrol**: `/admin/` ziyaret et

#### 3. Debug ve Geliştirme
```bash
# Debug modunda çalıştırma
DEBUG=True python manage.py runserver

# Django shell ile veri kontrolü
python manage.py shell
>>> from data_generator.models import ForecastData
>>> ForecastData.objects.count()

# Log dosyalarını kontrol etme
# (Şu anda aktif değil, eklenebilir)
```

### Son Kullanıcı İş Akışı (End User Workflow)

#### 1. Dashboard Kullanımı
1. **Erişim**: `http://localhost:8000/api/` adresine git
2. **Veri Görüntüleme**: Mevcut tahmin verilerini tabloda gör
3. **Yeni Veri**: "Generate New Data" butonuna tıkla
4. **İndirme**: "Download as Excel" ile verileri indir

#### 2. Veri Yönetimi Süreci
1. **Veri Üretimi**: GET `/api/generate-forecast/`
   - Eski veriler silinir
   - 100 yeni kayıt oluşturulur
   - Dashboard'a otomatik yönlendirme
2. **Veri İndirme**: GET `/api/download-forecast/`
   - Tüm veriler Excel formatında
   - Tarayıcı otomatik indirme başlatır

## 🎨 Frontend ve Template Yapısı

### Dashboard Template Özellikleri
- **Lokasyon**: `data_generator/templates/data_generator/forecast_dashboard.html`
- **Stil**: Inline CSS (harici dosya yok)
- **Responsive**: Temel responsive tasarım
- **Bileşenler**:
  - Başlık bölümü
  - Buton kontrolleri
  - Veri tablosu
  - Boş durum mesajı

### Template Context Verileri
```python
context = {
    'forecasts': ForecastData.objects.all().order_by('-forecast_date')
}
```

### CSS Stil Özellikleri
- **Tablo**: Border-collapse, padding, hover efektleri
- **Butonlar**: Yeşil (Generate) ve Mavi (Download) renk şeması
- **Responsive**: Temel responsive design
- **Typography**: Sans-serif font ailesi

## 🔐 Güvenlik ve Konfigürasyon

### Settings.py Kritik Ayarları
```python
# GÜVENLİK UYARISI: Production'da değiştirilmeli
SECRET_KEY = 'django-insecure-#_r7w!sdq2_px-y=m8+5qolpx(kj0))ehl*b1t7)9x9zl(-apm'
DEBUG = True  # Production'da False yapılmalı
ALLOWED_HOSTS = []  # Production'da domain ekle

# Uygulamalar
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',           # DRF
    'data_generator',           # Ana uygulama
]
```

### Güvenlik Önerileri
- **SECRET_KEY**: Production'da environment variable kullan
- **DEBUG**: Production'da False yap
- **ALLOWED_HOSTS**: Sadece izin verilen domain'leri ekle
- **CSRF Protection**: Aktif (POST işlemleri için gerekli)

## 🧪 Test Stratejisi ve Kalite Kontrolü

### Mevcut Test Durumu
- **Test Dosyası**: `data_generator/tests.py` (boş)
- **Test Coverage**: %0 (testler yazılmamış)
- **Test Framework**: Django TestCase (hazır)

### Önerilen Test Senaryoları
```python
# data_generator/tests.py (örnek)
class ForecastDataTestCase(TestCase):
    def test_model_creation(self):
        # Model oluşturma testi
        
    def test_generate_forecast_view(self):
        # Veri üretimi endpoint testi
        
    def test_download_excel_view(self):
        # Excel indirme testi
        
    def test_dashboard_view(self):
        # Dashboard render testi
```

### Test Çalıştırma
```bash
# Tüm testleri çalıştır
python manage.py test

# Belirli app testleri
python manage.py test data_generator

# Verbose output ile
python manage.py test --verbosity=2
```

## 🚀 Production ve Deployment

### Production Hazırlık Listesi
1. **Settings ayarları**:
   - `DEBUG = False`
   - `SECRET_KEY` environment variable
   - `ALLOWED_HOSTS` konfigürasyonu
2. **Veritabanı**: SQLite → PostgreSQL/MySQL
3. **Static dosyalar**: `python manage.py collectstatic`
4. **Güvenlik**: HTTPS, CSRF, SQL Injection koruması
5. **Monitoring**: Logging, error tracking

### Önerilen Deployment Stack
- **Web Server**: Nginx + Gunicorn
- **Database**: PostgreSQL
- **Caching**: Redis
- **Monitoring**: Sentry, New Relic

## 📈 Performans ve Optimizasyon

### Mevcut Performans Karakteristikleri
- **Veri Yükleme**: 100 kayıt batch insert
- **Excel Üretimi**: Pandas + XlsxWriter (bellek tabanlı)
- **Database Queries**: N+1 problemi yok (tek sorgu ile veriler)

### Optimizasyon Önerileri
1. **Database İndeksleme**: `forecast_date` alanına index
2. **Caching**: Django cache framework kullanımı
3. **Pagination**: Büyük veri setleri için sayfalama
4. **Background Tasks**: Celery ile asenkron işlemler

## 🔧 Geliştirme İpuçları ve Best Practices

### Kod Konvansiyonları
- **URL patterns**: Kebab-case (`generate-forecast`)
- **View names**: PascalCase + View suffix (`GenerateForecastView`)
- **Model fields**: Snake_case (`product_name`)
- **Template names**: App_name/template_name.html

### Yaygın Geliştirme Görevleri

#### Yeni Endpoint Ekleme
1. `data_generator/views.py`'ye view ekle
2. `data_generator/urls.py`'ye URL pattern ekle
3. Template gerekiyorsa `templates/` altına ekle
4. Serializer gerekiyorsa `serializers.py`'ye ekle

#### Model Değişiklikleri
1. `models.py`'yi düzenle
2. `python manage.py makemigrations`
3. Migrasyon dosyasını kontrol et
4. `python manage.py migrate`
5. `admin.py`'yi güncelle (gerekiyorsa)

#### API Endpoint Test Etme
```bash
# cURL ile test
curl http://localhost:8000/api/generate-forecast/
curl http://localhost:8000/api/download-forecast/ -o test.xlsx

# Browser'da test
http://localhost:8000/api/
```

## 🐛 Yaygın Sorunlar ve Çözümleri

### Database İssues
- **Migrasyon hatası**: `python manage.py migrate --fake-initial`
- **Sqlite locked**: Sunucuyu kapatıp tekrar başlat

### Import Errors
- **ModuleNotFoundError**: Virtual environment aktif mi kontrol et
- **App not found**: `INSTALLED_APPS`'e eklenmiş mi kontrol et

### Template Not Found
- **Template path**: App adı/template adı yapısını kontrol et
- **Template dirs**: `settings.py`'de TEMPLATES ayarını kontrol et

---

Bu kılavuz, DjangoApiApp projesinde etkili çalışabilmek için gereken tüm bilgileri içermektedir. Herhangi bir belirsizlik veya eksik bilgi için geliştirici ekibiyle iletişime geçin.
