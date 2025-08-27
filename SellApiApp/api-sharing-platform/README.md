# API Sharing Platform

Bu proje, kullanıcıların API'lerini paylaşabileceği bir platform oluşturmak için geliştirilmiştir. Django framework'ü kullanılarak inşa edilmiştir ve kullanıcı hesapları ile API yönetimi için gerekli tüm bileşenleri içermektedir.

## Proje Yapısı

- **api_platform/**: Django uygulamasının ana dizini.
  - **asgi.py**: ASGI uygulaması için giriş noktası.
  - **settings.py**: Proje ayarları.
  - **urls.py**: URL yönlendirmeleri.
  - **wsgi.py**: WSGI uygulaması için giriş noktası.
  
- **apps/**: Uygulama bileşenlerini içeren dizin.
  - **accounts/**: Kullanıcı hesapları ile ilgili işlemleri yöneten uygulama.
  - **apis/**: API'lerin yönetimi ve paylaşımı için uygulama.
  - **core/**: Temel işlevsellik ve yardımcı bileşenler.

- **static/**: CSS, JavaScript ve görsel dosyalarını içeren dizin.
- **templates/**: HTML şablonlarını içeren dizin.
- **manage.py**: Django projesini yönetmek için kullanılan komut dosyası.
- **requirements.txt**: Projede kullanılan Python kütüphanelerinin listesi.

## Kurulum

1. **Gereksinimleri Yükleyin**:
   Proje dizininde aşağıdaki komutu çalıştırarak gerekli kütüphaneleri yükleyin:
   ```
   pip install -r requirements.txt
   ```

2. **Veritabanını Ayarlayın**:
   Veritabanı ayarlarını `settings.py` dosyasında yapılandırın ve veritabanını oluşturun.

3. **Migrate Komutunu Çalıştırın**:
   Veritabanı tablolarını oluşturmak için aşağıdaki komutu çalıştırın:
   ```
   python manage.py migrate
   ```

4. **Sunucuyu Başlatın**:
   Geliştirme sunucusunu başlatmak için aşağıdaki komutu kullanın:
   ```
   python manage.py runserver
   ```

## Kullanım

Kullanıcılar, platforma kaydolabilir, API'lerini ekleyebilir ve diğer kullanıcıların paylaştığı API'leri keşfedebilir. Her API için detaylı bilgi ve kullanım talimatları sağlanacaktır.

## Katkıda Bulunma

Bu projeye katkıda bulunmak isterseniz, lütfen bir pull request oluşturun veya sorunlarınızı bildirin. Her türlü katkı ve geri bildirim için teşekkür ederiz!