# Copilot Instructions for Django E-Commerce Project

## Overview
This project is a Django tabanlı e-ticaret uygulamasıdır. Ana bileşenler şunlardır:
- `ecommerce_project/`: Django projesi ayarları ve URL yönlendirmeleri
- `store/`: Uygulamanın ana iş mantığı, modeller, görünümler ve URL'ler
- `templates/store/`: HTML şablonları
- `media/`: Ürün görselleri
- `staticfiles/`: Statik dosyalar (CSS, JS, img)

## Mimari ve Veri Akışı
- Ürünler, kategoriler, müşteriler ve siparişler `store/models.py` dosyasında tanımlanır.
- Kullanıcılar ürünleri görüntüleyebilir, sepete ekleyebilir ve satın alabilir.
- Sepet işlemleri session tabanlıdır (`request.session['cart']`).
- Sipariş tamamlandığında stoklar güncellenir ve sepet temizlenir.
- Admin paneli ile ürün ve kategori yönetimi mümkündür.

## Geliştirici İş Akışları
- **Kurulum:**
  - `pip install -r requirements.txt`
  - `python manage.py migrate`
  - `python manage.py createsuperuser`
  - `python manage.py runserver`
- **Testler:**
  - Testler `store/tests.py` dosyasında bulunur. Çalıştırmak için:
    - `python manage.py test store`
- **Veritabanı:**
  - SQLite kullanılır, dosya: `db.sqlite3`
- **Statik ve Medya Dosyaları:**
  - Statik dosyalar: `staticfiles/`
  - Medya dosyaları: `media/products/`

## Proje Özgü Konvansiyonlar
- Ürün görselleri `media/products/` altında saklanır, modelde `ImageField(upload_to='products/')` kullanılır.
- Sepet session ile yönetilir, model tabanlı değildir.
- Stok kontrolü ve güncelleme işlemleri `checkout` view'unda atomik olarak yapılır.
- URL'ler `store/urls.py` ile tanımlanır, ana yönlendirme `ecommerce_project/urls.py` üzerinden yapılır.
- Şablonlar `templates/store/` altında organize edilmiştir.

## Entegrasyon ve Bağımlılıklar
- Django'nun standart admin, auth, session, staticfiles ve messages uygulamaları kullanılır.
- Harici bir API veya servis entegrasyonu yoktur.
- Görseller ve statik dosyalar doğrudan dosya sistemi üzerinden sunulur.

## Örnekler ve Referanslar
- Sepet işlemleri: `store/views.py` > `add_to_cart`, `remove_from_cart`, `cart_detail`, `checkout`
- Model ilişkileri: `store/models.py` > `Product`, `Category`, `Order`, `OrderItem`, `Customer`
- Şablon örnekleri: `templates/store/product_list.html`, `templates/store/cart_detail.html`

---
Bu dosya, AI kodlama ajanlarının projede hızlıca üretken olmasını sağlamak için hazırlanmıştır. Eksik veya belirsiz noktalar için lütfen geri bildirim verin.
