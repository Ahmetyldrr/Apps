# 💳 Gerçek Ödeme Sistemleri Entegrasyon Rehberi

Bu rehber, test uygulamanızı gerçek ödeme sistemleriyle nasıl entegre edeceğinizi gösterir.

## 🚀 Genel Hazırlık Adımları

### 1. Environment Variables Kurulumu
```bash
# .env dosyası oluşturun ve API anahtarlarınızı ekleyin
SECRET_KEY=your-django-secret-key
DEBUG=True

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# PayPal
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-secret
PAYPAL_MODE=sandbox

# İyzico
IYZICO_API_KEY=your-iyzico-api-key
IYZICO_SECRET_KEY=your-iyzico-secret
IYZICO_BASE_URL=https://sandbox-api.iyzipay.com

# Papara
PAPARA_API_KEY=your-papara-api-key
PAPARA_API_SECRET=your-papara-secret

# Square
SQUARE_APPLICATION_ID=your-square-app-id
SQUARE_ACCESS_TOKEN=your-square-token
SQUARE_ENVIRONMENT=sandbox

# Razorpay
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-secret
```

### 2. Gerekli Paketleri Yükleyin
```bash
pip install python-decouple stripe paypalrestsdk iyzipay razorpay squareup
```

---

## 💯 1. STRIPE ENTEGRASYONu

### Neden Stripe?
- En developer-friendly ödeme sistemi
- Mükemmel dokümantasyon
- 190+ ülkede kullanılabilir
- Güçlü fraud protection

### Gerekli Adımlar:

#### 1. Stripe Hesabı Açın
- https://stripe.com adresine gidin
- Hesap oluşturun
- Dashboard'a erişin

#### 2. API Anahtarlarını Alın
- Dashboard > Developers > API keys
- Publishable key (pk_test_...) ve Secret key (sk_test_...) alın

#### 3. Webhook Ayarlayın
- Dashboard > Developers > Webhooks
- Endpoint ekleyin: `https://yoursite.com/stripe/webhook/`
- Events seçin: `payment_intent.succeeded`, `payment_intent.payment_failed`

#### 4. Test Kartları
```
Başarılı: 4242424242424242
Declined: 4000000000000002
Insufficient Funds: 4000000000009995
```

#### 5. Kod Entegrasyonu
```python
# views.py
from payments.payment_processors import StripePaymentProcessor

def stripe_payment(request):
    processor = StripePaymentProcessor()
    result = processor.create_payment_intent(order)
    if result['success']:
        # Frontend'e client_secret gönderin
        # Stripe.js ile ödeme tamamlayın
```

---

## 🌍 2. PAYPAL ENTEGRASYONu

### Neden PayPal?
- Dünya çapında tanınan marka
- Kullanıcılar kart bilgisi girmek zorunda değil
- Buyer protection

### Gerekli Adımlar:

#### 1. PayPal Developer Hesabı
- https://developer.paypal.com adresine gidin
- Hesap oluşturun veya mevcut PayPal hesabınızla giriş yapın

#### 2. Uygulama Oluşturun
- My Apps & Credentials > Create App
- App Name girin
- Sandbox/Live environment seçin
- Client ID ve Secret alın

#### 3. Test Hesapları
- Sandbox > Accounts
- Buyer ve Seller test hesapları oluşturun

#### 4. Kod Entegrasyonu
```python
# settings.py
PAYPAL_CLIENT_ID = 'your-client-id'
PAYPAL_CLIENT_SECRET = 'your-secret'
PAYPAL_MODE = 'sandbox'  # production için 'live'
```

---

## 🇹🇷 3. İYZICO ENTEGRASYONu

### Neden İyzico?
- Türkiye'de yerli çözüm
- Türk bankalarıyla kolay entegrasyon
- 3D Secure desteği
- Taksit seçenekleri

### Gerekli Adımlar:

#### 1. İyzico Başvurusu
- https://iyzico.com adresine gidin
- İş yeri başvurusu yapın
- Gerekli belgeler:
  - Vergi levhası
  - İmza sirküleri
  - Ticaret sicil gazetesi (limited şirket ise)

#### 2. Test Hesabı
- Başvuru sırasında test hesabı da talep edin
- API Key ve Secret Key alın

#### 3. Test Kartları
```
Başarılı: 5528790000000008
3D Secure: 5526080000000006
Hatalı: 4059030000000009
```

#### 4. Kod Entegrasyonu
```python
# Test için gerekli bilgiler
IYZICO_API_KEY = 'sandbox-your-api-key'
IYZICO_SECRET_KEY = 'sandbox-your-secret'
IYZICO_BASE_URL = 'https://sandbox-api.iyzipay.com'
```

---

## 💰 4. PAPARA ENTEGRASYONu

### Neden Papara?
- Türkiye'de hızla büyüyen platform
- Düşük komisyon oranları
- Anında para transferi
- Mobil odaklı

### Gerekli Adımlar:

#### 1. Papara İş Yeri Başvurusu
- Papara İş Yeri portalına başvuru yapın
- İş yeri onayı bekleyin

#### 2. API Erişimi
- API Key ve Secret alın
- Test ortamı erişimi isteyin

#### 3. Kod Entegrasyonu
```python
# Papara API henüz public değil, özel başvuru gerekli
PAPARA_API_KEY = 'your-api-key'
PAPARA_API_SECRET = 'your-secret'
```

---

## ⬜ 5. SQUARE ENTEGRASYONu

### Neden Square?
- Hem online hem offline ödemeler
- POS entegrasyonu
- Güçlı analytics
- ABD ve bazı ülkelerde popüler

### Gerekli Adımlar:

#### 1. Square Developer Hesabı
- https://developer.squareup.com adresine gidin
- Hesap oluşturun

#### 2. Uygulama Oluşturun
- Dashboard > Applications > Create App
- Application ID ve Access Token alın

#### 3. Test Kartları
```
Visa: 4111 1111 1111 1111
Mastercard: 5105 1051 0510 5100
```

---

## 🇮🇳 6. RAZORPAY ENTEGRASYONu

### Neden Razorpay?
- Hindistan'da lider ödeme sistemi
- 100+ ödeme yöntemi
- UPI, Net Banking desteği

### Gerekli Adımlar:

#### 1. Razorpay Hesabı
- https://razorpay.com adresine gidin
- Hindistan iş adresi gerekli

#### 2. API Anahtarları
- Dashboard > Settings > API Keys
- Key ID ve Secret alın

---

## 🔐 GÜVENLİK ÖNEMLİ NOTLAR

### 1. API Anahtarları Güvenliği
```python
# ❌ YANLIŞ - settings.py'da hardcode
STRIPE_SECRET_KEY = 'sk_test_123...'

# ✅ DOĞRU - Environment variables
import os
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
```

### 2. HTTPS Zorunluluğu
- Tüm ödeme sistemleri HTTPS gerektirir
- Production'da SSL sertifikası zorunlu

### 3. Webhook Güvenliği
```python
# Webhook signature'ları doğrulayın
def verify_stripe_webhook(payload, sig_header):
    try:
        stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        return True
    except:
        return False
```

### 4. PCI Compliance
- Kart bilgilerini asla sunucunuzda saklamayın
- Tokenization kullanın
- PCI DSS standartlarına uyun

---

## 📊 TEST ORTAMI vs PRODUCTION

| Sistem | Test URL | Production URL |
|--------|----------|----------------|
| Stripe | Aynı endpoint | Aynı endpoint |
| PayPal | sandbox-api | api |
| İyzico | sandbox-api | api |
| Square | sandbox | production |

---

## 🛠️ DEBUGİNG İPUÇLARI

### 1. Log Tutun
```python
import logging

logger = logging.getLogger(__name__)

def process_payment(order):
    logger.info(f"Payment started for order {order.order_id}")
    # ... ödeme işlemi
    logger.info(f"Payment completed: {result}")
```

### 2. Test Modunu Açık Tutun
```python
# Tüm test sistemlerinde açık uyarı gösterin
if settings.DEBUG:
    messages.warning(request, "TEST MODU - Gerçek ödeme yapılmıyor!")
```

### 3. Webhook Test Etme
```bash
# Stripe CLI ile webhook test
stripe listen --forward-to localhost:8000/stripe/webhook/
stripe trigger payment_intent.succeeded
```

---

## 📱 FRONTEND ENTEGRASYONu

Her ödeme sisteminin kendi JavaScript SDK'sı var:

### Stripe.js
```html
<script src="https://js.stripe.com/v3/"></script>
<script>
  const stripe = Stripe('pk_test_...');
  // Payment Element kullanın
</script>
```

### PayPal Checkout
```html
<script src="https://www.paypal.com/sdk/js?client-id=your-client-id"></script>
```

### İyzico Checkout
```html
<script src="https://static.iyzipay.com/checkoutform/api/js/iyzipay-checkout-form.js"></script>
```

---

## 💡 PRO İPUÇLARI

1. **Çoklu Ödeme Sistemi**: Kullanıcılara seçenek sunun
2. **Failover**: Bir sistem çökerse diğerine yönlendirin
3. **A/B Test**: Hangi sistem daha iyi conversion veriyor test edin
4. **Analytics**: Her sistemin performansını takip edin
5. **Mobile First**: Mobil deneyimi önceliklendirin

---

## 📞 DESTEK KAYNAKLARI

- **Stripe**: https://stripe.com/docs
- **PayPal**: https://developer.paypal.com/docs
- **İyzico**: https://dev.iyzipay.com
- **Square**: https://developer.squareup.com/docs
- **Razorpay**: https://razorpay.com/docs

---

## ⚡ HIZLI BAŞLATMA

1. Bir ödeme sistemi seçin (önerilen: Stripe)
2. Test hesabı açın
3. API anahtarlarını alın
4. .env dosyasına ekleyin
5. Test kartlarıyla deneyin
6. Webhook'ları ayarlayın
7. Production'a geçin

## 🎯 SONRAKİ ADIMLAR

Test uygulamanız hazır! Şimdi:
1. Gerçek bir ödeme sistemi seçin
2. Hesap açın ve API anahtarlarını alın
3. Kodunuzu güncelleyin
4. Test edin
5. Production'a deploy edin

Başarılar! 🚀
