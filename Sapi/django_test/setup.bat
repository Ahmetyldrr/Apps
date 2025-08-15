@echo off
echo 🚀 Django Test Projesi Başlatılıyor...
echo.

REM Sanal ortam kontrol et
if not exist "venv" (
    echo 📦 Sanal ortam oluşturuluyor...
    python -m venv venv
)

REM Sanal ortamı aktif et
echo 🔧 Sanal ortam aktif ediliyor...
call venv\Scripts\activate.bat

REM Gerekli paketleri yükle
echo 📚 Paketler yükleniyor...
pip install -r requirements.txt

REM Database migration
echo 🗄️ Veritabanı migration'ları uygulanıyor...
python manage.py makemigrations
python manage.py migrate

echo.
echo ✅ Django Test Projesi Hazır!
echo.
echo 🎯 Kullanım:
echo    - Admin oluştur: python manage.py createsuperuser
echo    - Sunucu başlat: python manage.py runserver
echo    - Veri import et: python manage.py import_from_simple_modules
echo.
pause
