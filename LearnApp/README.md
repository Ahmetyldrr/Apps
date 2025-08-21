# AI Destekli Soru-Cevap Uygulaması

Bu proje, OpenAI GPT modeli kullanarak dinamik sorular üreten ve iki kullanıcılı yarışma modu sunan PyQt5 tabanlı bir masaüstü uygulamasıdır.

## Özellikler

- **İki Kullanıcılı Yarışma**: Sırayla soru çözen iki oyuncu modu
- **AI Destekli Soru Üretimi**: OpenAI GPT-4 ile dinamik soru üretimi
- **Çoklu Konu Desteği**: 10 hazır konu + özel konu seçeneği
- **3 Zorluk Seviyesi**: Basit (Lise), Orta (Üniversite), Zor (Uzman)
- **Renkli Arayüz**: Oyunculara özel renkler ve doğru/yanlış gösterimi
- **Veritabanı Kaydı**: SQLite ile kullanıcı ve skor kayıtları
- **Geçmiş Sonuçlar**: Oyun geçmişi görüntüleme

## Kurulum

1. Gerekli paketleri kurun:
```bash
pip install -r requirements.txt
```

2. Uygulamayı başlatın:
```bash
python main.py
```

## Kullanım

1. **Kullanıcı Ekleme**: "Yeni Kullanıcı Ekle" ile oyuncuları kaydedin
2. **Oyuncu Seçimi**: İki farklı oyuncu seçin
3. **Konu ve Seviye**: Konu ve zorluk seviyesini belirleyin
4. **Soru Sayısı**: 1-20 arası soru sayısı seçin
5. **Test Başlat**: Yarışmayı başlatın

## Dosya Yapısı

- `main.py`: Ana uygulama dosyası
- `config.py`: Yapılandırma ve sabitler
- `question_generator.py`: OpenAI API entegrasyonu
- `db/database.py`: SQLite veritabanı yönetimi
- `db/quizapp.db`: Veritabanı dosyası (otomatik oluşur)

## API Anahtarı

OpenAI API anahtarınızı `config.py` dosyasında güncellemeniz gerekebilir.

## Teknik Detaylar

- **UI Framework**: PyQt5
- **AI Model**: OpenAI GPT-4
- **Veritabanı**: SQLite
- **Python Version**: 3.8+

## Katkıda Bulunma

Projeye katkıda bulunmak için issue açabilir veya pull request gönderebilirsiniz.
