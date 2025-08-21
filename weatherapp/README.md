# PyQt5 Gelişmiş Saatlik Hava Durumu Takip Sistemi

Bu proje, Diyarbakır, Mardin, Siirt, Şırnak, Şanlıurfa ve Batman illeri için gelişmiş saatlik hava durumu takibi yapar. Modern PyQt5 arayüzü, gerçek zamanlı veri güncellemesi, grafiksel görselleştirme ve kapsamlı analitik özellikler sunar.

## 🌟 Özellikler

### Temel Özellikler
- **Modern PyQt5 Arayüzü**: Gradyan renkler, kartlar ve sekme tabanlı tasarım
- **6 İl Desteği**: Diyarbakır, Mardin, Siirt, Şırnak, Şanlıurfa, Batman
- **Gerçek Zamanlı Güncelleme**: Her 10 saniyede otomatik veri yenileme
- **SQLite Veritabanı**: Geliştirilmiş veri yapısı ve performans

### Görselleştirme
- **Şehir Kartları**: Modern tasarım ile anlık hava durumu
- **İnteraktif Grafikler**: Matplotlib ile çizilen dinamik grafikler
- **Çoklu Görünüm**: Sıcaklık, rüzgar, nem, basınç grafikleri
- **Seaborn Stil**: Profesyonel grafik görünümü

### Veri Özellikleri
- **Sıcaklık**: Gerçek ve hissedilen sıcaklık
- **Hava Durumu**: Güneşli, bulutlu, yağmurlu durumlar
- **Rüzgar Hızı**: km/h cinsinden ölçüm
- **Nem Oranı**: Yüzde cinsinden nem
- **Basınç**: hPa cinsinden atmosfer basıncı
- **UV İndeksi**: Güneş radyasyonu seviyesi
- **Görüş Mesafesi**: km cinsinden görüş kalitesi
- **Bulutlanma**: Yüzde cinsinden bulut kapsamı

### Analitik Araçlar
- **İstatistiksel Analiz**: Min, max, ortalama değerler
- **Şehir Karşılaştırması**: Çoklu şehir veri analizi
- **Trend Analizi**: Saatlik değişim grafikleri
- **Excel Export**: Çoklu sayfa Excel raporu

## 🚀 Kurulum

### Gereksinimler
```bash
Python 3.7+
PyQt5
pandas
openpyxl
matplotlib
seaborn
sqlite3 (Python ile birlikte gelir)
```

### Paket Kurulumu
```bash
pip install pyqt5 pandas openpyxl matplotlib seaborn
```

## 📱 Kullanım

### Uygulamayı Başlatma
```bash
python main_ultimate.py
```

### Ana Özellikler
1. **Ana Panel**: Tüm şehirler için hava durumu kartları
2. **Grafikler**: İnteraktif veri görselleştirme
3. **Detaylar**: Şehir bazında saatlik detaylar
4. **Analitik**: İstatistiksel raporlar

### Veri Yönetimi
- **Otomatik Yenileme**: Gerçek zamanlı checkbox ile kontrol
- **Manuel Yenileme**: Yenile butonu ile anlık güncelleme
- **Excel Export**: Tüm veriler ve şehir bazında sayfalar

## 📊 Ekran Görüntüleri

### Ana Panel
- Modern şehir kartları
- Gradyan arka plan
- Anlık hava durumu bilgileri

### Grafikler
- Çoklu şehir karşılaştırması
- Seçilebilir veri türleri
- Profesyonel görselleştirme

### Detaylı Görünüm
- Saatlik veri tabloları
- Kapsamlı bilgi sütunları
- Şehir seçim filtreleri

## 🔧 Teknik Detaylar

### Veritabanı Yapısı
- **Ana Tablo**: weather
- **Sütunlar**: 13 farklı veri alanı
- **İndeksler**: Hızlı sorgu için optimize edilmiş

### Performans
- **Gerçek Zamanlı Thread**: Arayüz donmaması için ayrı thread
- **Optimize Sorgular**: SQLite performans optimizasyonu
- **Bellek Yönetimi**: Verimli veri kullanımı

### Mimari
- **MVC Pattern**: Model-View-Controller yapısı
- **Modüler Tasarım**: Ayrı class'lar ile organize kod
- **Thread Safety**: Güvenli çoklu thread işlemleri

## 🔄 Veri Akışı

1. **Başlangıç**: Örnek veriler SQLite'a yüklenir
2. **Görselleştirme**: Kartlar ve tablolar oluşturulur
3. **Güncelleme**: Thread ile otomatik veri yenileme
4. **Analiz**: Grafikler ve istatistikler hesaplanır
5. **Export**: Excel formatında kapsamlı raporlar

## 🎨 Tasarım Özellikleri

### Renk Paleti
- **Mavi Tonları**: #74b9ff, #0984e3
- **Gradient Efektler**: Modern görsel deneyim
- **Beyaz Altyapı**: Temiz ve okunabilir tasarım

### Tipografi
- **Arial Font**: Tüm metinler için standart
- **Bold Vurgular**: Önemli bilgiler için
- **Uyumlu Boyutlar**: 10px - 20px arası

## 🚀 Gelecek Geliştirmeler

### Planlanan Özellikler
- **Gerçek API Entegrasyonu**: OpenWeatherMap, AccuWeather
- **Coğrafi Haritalar**: Harita üzerinde hava durumu
- **Bildirimler**: Kritik hava durumu uyarıları
- **Tema Desteği**: Karanlık/Aydınlık mod
- **Çoklu Dil**: İngilizce, Türkçe dil desteği

### Performans İyileştirmeleri
- **Veri Önbellekleme**: Hızlı erişim için cache
- **Lazy Loading**: İhtiyaç anında veri yükleme
- **Async Operations**: Asenkron veri işlemleri

## 🐛 Bilinen Sorunlar

- Yoğun veri güncellemelerinde hafif performans düşüşü
- Windows'ta ilk başlatmada gecikmeli açılış olabilir
- Excel export'ta büyük veri setlerinde yavaşlık

## 📝 Notlar

- Veriler şimdilik simülasyon amaçlıdır
- Gerçek API entegrasyonu v3.0'da eklenecektir
- Test verileri rastgele oluşturulmaktadır
- 24 saatlik veri döngüsü kullanılmaktadır

## 👨‍💻 Geliştirici

Bu proje, modern Python GUI teknolojileri kullanılarak geliştirilmiştir. PyQt5, matplotlib ve pandas gibi güçlü kütüphaneler ile profesyonel bir hava durumu takip sistemi oluşturulmuştur.
