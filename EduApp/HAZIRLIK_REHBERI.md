# 🚀 Django Eğitim Platformu - Başlangıç Hazırlık Rehberi

## 🎯 Projeye Başlamadan Önce Yapılması Gerekenler

### 1. 💻 Sistem Gereksinimleri Kontrolü

#### Python Kontrolü
```cmd
python --version
```
**Gerekli:** Python 3.9 veya üzeri

#### Git Kontrolü
```cmd
git --version
```
**Gerekli:** Git 2.x

#### Node.js Kontrolü (Frontend araçları için)
```cmd
node --version
npm --version
```
**Gerekli:** Node.js 16+ (opsiyonel ama önerilen)

---

## 🛠️ Adım 1: Gerekli Yazılımları Kurma

### 1.1 Python Kurulumu (Eğer yoksa)
- [Python.org](https://python.org) adresinden Python 3.11 indirin
- Kurulum sırasında "Add Python to PATH" seçeneğini işaretleyin
- pip'in kurulu geldiğini doğrulayın: `pip --version`

### 1.2 Git Kurulumu (Eğer yoksa)
- [Git-scm.com](https://git-scm.com) adresinden Git indirin
- Kurulum sonrası kullanıcı bilgilerini ayarlayın:
```cmd
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 1.3 PostgreSQL Kurulumu
- [PostgreSQL.org](https://postgresql.org) adresinden indirin
- Kurulum sırasında superuser şifresi belirleyin
- pgAdmin4 ile birlikte kurulmasını sağlayın

### 1.4 Redis Kurulumu (Windows için)
- WSL kullanarak Linux alt sistemi kurun, ya da
- Docker Desktop yükleyip Redis container'ı çalıştırın
- Alternatif: Memurai (Windows için Redis alternatifi)

---

## 🏗️ Adım 2: Geliştirme Ortamı Hazırlığı

### 2.1 Proje Klasörü Oluşturma
```cmd
cd c:\Users\ahmet.yildirir\Desktop\Apps\TestApp
mkdir learning_platform
cd learning_platform
```

### 2.2 Virtual Environment Oluşturma
```cmd
python -m venv venv
venv\Scripts\activate
```

### 2.3 pip Güncellemesi
```cmd
python -m pip install --upgrade pip
```

### 2.4 Git Repository İnisialisasyonu
```cmd
git init
git branch -M main
```

---

## 📦 Adım 3: Temel Paket Kurulumları

### 3.1 requirements.txt Oluşturma
Aşağıdaki içerikle dosya oluşturun:

```txt
# Core Django
Django==4.2.4
djangorestframework==3.14.0

# Environment & Configuration
python-decouple==3.8
django-cors-headers==4.2.0

# Database
psycopg2-binary==2.9.7

# Media & Files
Pillow==10.0.0
django-storages==1.13.2

# Development Tools
django-extensions==3.2.3
django-debug-toolbar==4.2.0

# Task Queue
celery==5.3.1
redis==4.6.0

# Payment (Sonradan eklenecek)
# stripe==5.5.0

# Cloud Storage (Sonradan eklenecek)
# boto3==1.28.25
```

### 3.2 Paketleri Kurma
```cmd
pip install -r requirements.txt
```

---

## 🗃️ Adım 4: Veritabanı Hazırlığı

### 4.1 PostgreSQL Database Oluşturma
pgAdmin4 veya psql ile:
```sql
CREATE DATABASE learning_platform_db;
CREATE USER learning_platform_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE learning_platform_db TO learning_platform_user;
```

### 4.2 Database Connection Test
```cmd
python -c "import psycopg2; print('PostgreSQL connection successful!')"
```

---

## ⚙️ Adım 5: Environment Variables Hazırlığı

### 5.1 .env.example Dosyası Oluşturma
```env
# Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=learning_platform_db
DB_USER=learning_platform_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Email (Development - Console backend)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Media Files
MEDIA_ROOT=media/
STATIC_ROOT=staticfiles/

# Security (Production'da değiştirin)
SECURE_SSL_REDIRECT=False
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
```

### 5.2 .env Dosyası Oluşturma
```cmd
copy .env.example .env
```
Sonra .env dosyasını editleyip gerçek değerleri girin.

---

## 📁 Adım 6: Proje Yapısı Oluşturma

### 6.1 Ana Klasörleri Oluşturma
```cmd
mkdir static
mkdir media
mkdir templates
mkdir apps
mkdir config
mkdir docs
```

### 6.2 .gitignore Dosyası Oluşturma
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/

# Environment
.env
.venv
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Static files
staticfiles/
```

---

## 🎯 Adım 7: Ön Kontroller

### 7.1 Python Virtual Environment Kontrolü
```cmd
where python
```
Çıktı venv klasörünü göstermeli.

### 7.2 Django Kurulum Kontrolü
```cmd
python -c "import django; print(django.get_version())"
```

### 7.3 Database Bağlantı Kontrolü
```cmd
python -c "
import psycopg2
try:
    conn = psycopg2.connect(
        database='learning_platform_db',
        user='learning_platform_user',
        password='your_password',
        host='localhost',
        port='5432'
    )
    print('✅ Database bağlantısı başarılı!')
    conn.close()
except Exception as e:
    print('❌ Database bağlantı hatası:', e)
"
```

---

## 📋 Hazırlık Checklist

### Sistemde Kurulu Olması Gerekenler:
- [ ] Python 3.9+ kurulu ve PATH'e ekli
- [ ] Git kurulu ve yapılandırılmış
- [ ] PostgreSQL kurulu ve çalışıyor
- [ ] Redis kurulu veya Docker ile çalışıyor
- [ ] VS Code kurulu (Markdown eklentileri ile)

### Proje Klasöründe Olması Gerekenler:
- [ ] Virtual environment oluşturulmuş ve aktif
- [ ] requirements.txt oluşturulmuş
- [ ] Temel paketler kurulmuş
- [ ] .env.example ve .env dosyaları oluşturulmuş
- [ ] .gitignore dosyası oluşturulmuş
- [ ] Temel klasör yapısı oluşturulmuş
- [ ] Database oluşturulmuş ve test edilmiş
- [ ] Git repository initialize edilmiş

### Hazırlık Tamamlandıktan Sonra:
- [ ] İlk commit yapılabilir
- [ ] Django projesi oluşturulabilir
- [ ] İlk migration çalıştırılabilir
- [ ] Development server başlatılabilir

---

## 🚨 Önemli Notlar

### Güvenlik:
- **.env dosyasını asla Git'e commitlemeyin**
- Production'da güçlü SECRET_KEY kullanın
- Database şifrelerini güvenli tutun

### Performance:
- Virtual environment her zaman aktif olsun
- pip freeze ile paket listesini güncellemeyi unutmayın

### Backup:
- Database'i düzenli olarak yedekleyin
- Kod değişikliklerini sık sık commit edin

---

## 🎉 Sonraki Adım

Tüm hazırlıklar tamamlandıktan sonra:
1. **Django projesi oluşturma**
2. **İlk app (accounts) oluşturma**
3. **Custom User modeli kurma**
4. **İlk migration**

Hazır olduğunuzda bana haber verin, Django projesini oluşturmaya başlayalım! 🚀
