# 🚀 DJANGO PROJESİ OTOMATIK OLUŞTURMA TALİMATNAMESİ

Bu talimatname ile GitHub Copilot'a Django projenizi baştan sona oluşturması için gerekli tüm bilgileri sağlayabilirsiniz. Aşağıdaki alanları doldurun ve bu dosyayı Copilot'a vererek projenizin otomatik olarak oluşturulmasını isteyin.

## 📋 PROJE TEMEL BİLGİLERİ

### 🎯 Proje Tanımı

- **Proje Adı:** `[Projenizin adını yazın - örn: eticaret_sitesi]`
- **Proje Açıklaması:** `[Projenin ne yaptığını kısaca açıklayın - örn: Online kitap satış sitesi]`
- **Hedef Kitle:** `[Kimler kullanacak - örn: Kitap severler, öğrenciler]`
- **Ana Özellikler:** `[Temel özellikleri listeleyin - örn: Ürün katalogu, sepet, ödeme, kullanıcı kayıt]`

### 🏗️ Teknik Gereksinimler

- **Django Versiyonu:** `[Örn: 5.0.x, 4.2.x LTS]`
- **Python Versiyonu:** `[Örn: 3.11, 3.12]`
- **Veritabanı:** `[PostgreSQL / MySQL / SQLite]`
- **Cache:** `[Redis / Memcached / Yok]`
- **Frontend Framework:** `[Bootstrap / Tailwind / Custom CSS / React]`
- **API:** `[Django REST Framework gerekli mi? Evet/Hayır]`

## 🎨 KULLANICI ARAYÜZÜ VE TASARIM

### 📱 Sayfalar ve İşlevsellik

**Ana Sayfalar:** `[Hangi sayfalar olacak - örn: Ana sayfa, ürün listesi, ürün detay, sepet, ödeme, profil]`

**Kullanıcı Türleri:**

- [ ] Misafir kullanıcı (kayıtsız)
- [ ] Kayıtlı kullanıcı
- [ ] Admin/Yönetici
- [ ] Satıcı (çok satıcılı platform ise)

**Özel İşlevler:** `[Ekstra özellikler - örn: Wishlist, yorumlar, puanlama, kupon sistemi, kargo takibi]`

### 🎨 Tasarım Tercihleri

- **Renk Teması:** `[Örn: Mavi-beyaz, koyu tema, minimalist]`
- **Stil:** `[Modern, klasik, minimalist, renkli]`
- **Logo/Marka:** `[Var/Yok - varsa açıklama]`

## 🗄️ VERİTABANI YAPISI VE MODELLER

### 📊 Ana Veri Modelleri

**Gerekli Modeller:** `[Hangi ana modeller olacak - örn: User, Product, Category, Order, Cart]`

**Özel Alanlar ve İlişkiler:**

```yaml
# Örnek format:
Product Model:
  - name: CharField
  - description: TextField
  - price: DecimalField
  - stock_quantity: IntegerField
  - category: ForeignKey to Category
  - images: çoklu resim gerekli mi?
  - tags: ManyToMany field gerekli mi?

User Profile:
  - phone: CharField
  - address: TextField
  - birth_date: DateField
  - preferred_categories: ManyToMany
```

**Özel İlişkiler:** `[Karmaşık ilişkiler varsa açıklayın]`

## 🔐 GÜVENLİK VE KULLANICI YÖNETİMİ

### 👤 Kimlik Doğrulama

- **Kayıt Sistemi:** `[Email/Kullanıcı adı ile kayıt]`
- **Giriş Seçenekleri:** `[Email/Username + şifre, sosyal medya girişi]`
- **Sosyal Giriş:** `[Google, Facebook, GitHub - hangilerini istiyorsanız]`
- **Email Doğrulama:** `[Gerekli/Gerekli değil]`
- **Şifre Sıfırlama:** `[Email ile/SMS ile]`

### 🛡️ Güvenlik Özellikleri

- [ ] reCAPTCHA
- [ ] Rate Limiting
- [ ] CSRF Protection
- [ ] XSS Protection
- [ ] SQL Injection koruması (Django default)
- [ ] Admin panel güvenliği

## 💳 ÖDEME VE E-TİCARET

### 💰 Ödeme Sistemi

- **Ödeme Yöntemleri:** `[Kredi kartı, PayPal, Stripe, iyzico, vb.]`
- **Para Birimi:** `[TL, USD, EUR]`
- **Kargo:** `[Gerekli/Gerekli değil]`
- **Stok Takibi:** `[Otomatik/Manuel]`
- **İndirim Sistemi:** `[Kupon, promosyon kodu gerekli mi?]`

## 📧 İLETİŞİM VE BİLDİRİMLER

### 📬 Email Sistemi

- **Email Servisi:** `[Gmail SMTP, SendGrid, AWS SES]`
- **Email Türleri:** `[Kayıt onayı, şifre sıfırlama, sipariş onayı, haber bülteni]`
- **Bildirim Sistemi:** `[In-app notifications, push notifications]`

## 🔧 ENTEGRASYON VE API

### 🌐 Dış Servis Entegrasyonları

- **Harita/Konum:** `[Google Maps, OpenStreetMap]`
- **Dosya Depolama:** `[AWS S3, CloudFlare, yerel sunucu]`
- **Analytics:** `[Google Analytics, özel tracking]`
- **Sosyal Medya:** `[Facebook SDK, Twitter API]`
- **Diğer:** `[Belirli API'ler varsa yazın]`

### 🔌 API Gereksinimleri

- **REST API:** `[Gerekli/Gerekli değil]`
- **GraphQL:** `[Gerekli/Gerekli değil]`
- **API Dokümantasyonu:** `[Swagger/OpenAPI]`
- **API Kimlik Doğrulama:** `[Token, JWT, Session]`

## 🎭 ADMIN PANELİ VE YÖNETİM

### 🔧 Admin Özellikleri

- **Django Admin Kullanımı:** `[Varsayılan/Özelleştirilmiş]`
- **Admin Tema:** `[Varsayılan/Jazzmin/Grappelli/Custom]`
- **Yönetim Özellikleri:** `[Kullanıcı yönetimi, içerik yönetimi, raporlar, analytics]`
- **Bulk İşlemler:** `[Toplu ürün ekleme, toplu güncelleme]`

## 🧪 TEST VE KALİTE

### ✅ Test Gereksinimleri

- **Test Türleri:** `[Unit tests, Integration tests, Functional tests]`
- **Test Coverage:** `[%80+, %90+, önemli değil]`
- **Test Araçları:** `[Django TestCase, pytest, Selenium]`

### 📊 Performans

- **Sayfa Yüklenme Süresi:** `[Hedef süre - örn: <2 saniye]`
- **Eş Zamanlı Kullanıcı:** `[Kaç kullanıcı aynı anda - örn: 100, 1000]`
- **Caching Stratejisi:** `[Redis, Memcached, Database caching]`

## 🚀 DEPLOYMENT VE HOSTING

### 🌐 Hosting Tercihi

- **Platform:** `[Heroku, DigitalOcean, AWS, VPS, shared hosting]`
- **Domain:** `[Var/Yok - varsa hangi]`
- **SSL:** `[Let's Encrypt, paid certificate]`
- **CDN:** `[CloudFlare, AWS CloudFront, gerekli değil]`

### 🔄 CI/CD

- **Version Control:** `[GitHub, GitLab, Bitbucket]`
- **Auto Deployment:** `[GitHub Actions, GitLab CI, Jenkins]`
- **Environment:** `[Development, Staging, Production]`

## 📱 MOBİL UYUMLULUK

### 📲 Responsive Tasarım

- **Mobile First:** `[Evet/Hayır]`
- **Tablet Uyumluluğu:** `[Gerekli/Gerekli değil]`
- **PWA (Progressive Web App):** `[Gerekli/Gerekli değil]`
- **Mobile App:** `[Gelecekte planlanıyor/Şimdilik web only]`

## 🌍 ÇOK DİLLİLİK VE YERELLEŞTIRME

### 🗣️ Dil Desteği

- **Ana Dil:** `[Türkçe, İngilizce, vb.]`
- **Ek Diller:** `[Hangi dillerde olacak]`
- **RTL Desteği:** `[Arapça, İbranice için gerekli mi?]`
- **Tarih/Saat Format:** `[TR, US, ISO]`
- **Para Birimi Format:** `[Türk Lirası, Dolar, vb.]`

## 📈 ANALİTİK VE RAPORLAMA

### 📊 Takip Edilecek Metrikler

- **Kullanıcı Davranışı:** `[Sayfa görüntüleme, tıklama, dönüşüm]`
- **Satış Raporları:** `[Günlük, haftalık, aylık satışlar]`
- **Performans:** `[Sayfa hızı, server response time]`
- **Custom Events:** `[Özel takip edilecek olaylar]`

## 🎯 ÖZEL GEREKSINIMLER

### 🔧 Özel İşlevsellik

```yaml
# Buraya projenize özel, yukarıda yer almayan özel gereksinimleri yazın

Örnekler:
  - QR kod ile ürün tarama
  - AI destekli ürün önerisi
  - Canlı chat sistemi
  - Video streaming
  - Dosya upload/download sistemi
  - Multi-vendor marketplace
  - Subscription sistemi
  - Booking/Rezervasyon sistemi
```

## 📋 PROJE TESLİM FORMATI

### 📦 Teslim Edilecekler

- [ ] Tüm kaynak kodlar (GitHub repository)
- [ ] Requirements.txt dosyası
- [ ] README.md dosyası (kurulum kılavuzu)
- [ ] Environment variables şablonu (.env.example)
- [ ] Database schema ve initial data
- [ ] Admin kullanıcısı (username/password)
- [ ] Test verileri ve test kullanıcıları
- [ ] Deployment kılavuzu
- [ ] API dokümantasyonu (varsa)
- [ ] Kullanıcı kılavuzu

### 🔧 Geliştirme Ortamı

- **IDE/Editor:** `[VSCode, PyCharm, diğer]`
- **Virtual Environment:** `[venv, conda, pipenv]`
- **Package Manager:** `[pip, poetry]`

---

## 🤖 COPILOT TALİMATI

Yukarıdaki formu doldurduktan sonra, aşağıdaki talimatı GitHub Copilot'a verin:

```text
Bu Django proje talimatnamesindeki tüm gereksinimlere göre eksiksiz bir Django projesi oluştur. 

PROJE YAPISI:
1. Django projesini başlat ve gerekli ayarları yap
2. Belirtilen modelları oluştur ve migration'ları hazırla
3. Admin panel konfigürasyonunu yap
4. Views, URLs ve templates'leri oluştur
5. Forms ve validation'ları ekle
6. Authentication ve authorization sistemini kur
7. Gerekli static files ve CSS'leri hazırla
8. Test dosyalarını oluştur
9. Requirements.txt ve deployment dosyalarını hazırla
10. README.md ve dokümantasyonu oluştur

GEREKSINIMLER:
- Her adımı detaylı olarak açıkla
- Working code'lar üret
- Production-ready olsun
- Secure olsun
- Scalable olsun
- Best practices uygula
- Comprehensive error handling
- Proper logging

DOSYA YAPISI:
- Clean architecture
- Proper separation of concerns
- Modular design
- Easy to maintain
- Well documented
```

---

## 📝 KULLANIM TALİMATLARI

### 🎯 Nasıl Kullanılır

1. **Formu Doldurun:** Yukarıdaki tüm alanları projenize göre doldurun
2. **Copilot'a Verin:** Doldurduğunuz formu GitHub Copilot'a yapıştırın
3. **Talimat Ekleyin:** En alttaki "COPILOT TALİMATI" bölümünü de ekleyin
4. **İsteyin:** "Bu talimatlara göre Django projemi oluştur" deyin

### 💡 İpuçları

- Belirsiz alanları boş bırakabilirsiniz, Copilot uygun varsayılanları seçer
- Karmaşık projeler için adım adım ilerleyin
- Her aşamada test edin ve eksikleri tamamlayın
- Dokümantasyonu güncel tutun
- Güvenlik ayarlarını production'da mutlaka kontrol edin

### ⚠️ Önemli Notlar

- Bu talimatname kapsamlı projeler için tasarlanmıştır
- Küçük projeler için gerekli bölümleri kullanabilirsiniz
- Güvenlik ayarlarını production'da mutlaka yapın
- Backup stratejinizi unutmayın
- Performance testing yapın
- Code review sürecini atlamamayın

### 🔄 Sürekli Geliştirme

- Kullanıcı geri bildirimlerini toplayın
- Analytics verilerini takip edin
- Performance metrikleri izleyin
- Güvenlik güncellemelerini yapın
- Teknoloji stack'i güncel tutun

---

**Son Güncelleme:** 27 Ağustos 2025  
**Versiyon:** 2.0  
**Oluşturan:** GitHub Copilot Assistant  
**Lisans:** MIT
