# 🟡 BASİT SERA MALİYET HESAPLAMA SİSTEMİ

## 🎯 TEMEL KURAL
**🟡 SARI HÜCRELER = VERİ GİRİŞ YERLERİ**
Sadece sarı hücrelere veri girin, geri kalanı otomatik hesaplanır!

## 📋 DOSYA: `Sera_Basit_Sistem.xlsx`

## 🔢 NASIL KULLANILIR?

### 1️⃣ PROJE BİLGİLERİ
- Proje adı, müşteri vs. yazın (isteğe bağlı)

### 2️⃣ MALZEME FİYATLARI
**Sayfa 2-3-4'te sadece SARI hücreleri doldurun:**

#### 📍 Sayfa 2: Montaj Malzemeleri
- Miktar ve fiyat sütunlarındaki SARI hücreleri güncelleyin
- Yeni malzeme eklemek için alt satıra yazın

#### 📍 Sayfa 3: Direk Malzemeleri  
- 1 metre direk için gerekli malzemeler
- SARI hücrelerdeki fiyatları güncelleyin

#### 📍 Sayfa 4: Müştemilat Malzemeleri
- 1 adet müştemilat direk malzemeleri
- SARI hücrelerdeki fiyatları güncelleyin

### 3️⃣ PROJE HESAPLAMA
**Sayfa 5'te SARI hücreleri doldurun:**

#### 🟡 GİRİLECEK DEĞERLER:
- **Tünel Uzunluğu**: 250 metre
- **Tünel Sayısı**: 50 adet
- **Tünel Genişlik**: 9.6 metre  
- **Orta Kolon Aralığı**: 5 metre
- **Müştemilat Direk Sayısı**: 25 adet

#### ⚡ OTOMATIK HESAPLANIR:
- Toplam alan
- Montaj noktası sayısı
- Ara direk uzunluğu
- Toplam maliyetler
- M² başına maliyet

## 🔧 FORMÜL MANTIGI

### Basit ve Anlaşılır:
```
Montaj Maliyeti = Montaj Noktası Sayısı × 1 Montaj Maliyeti
Direk Maliyeti = Toplam Metre × 1 Metre Direk Maliyeti
Müştemilat Maliyeti = Direk Sayısı × 1 Direk Maliyeti
```

### Sayfalar Arası Bağlantı:
```
='Montaj Malzemeleri'.D10    (10. satırdaki toplam)
='Direk Malzemeleri'.D9      (9. satırdaki toplam)  
='Müştemilat Malzemeleri'.D10 (10. satırdaki toplam)
```

## ✅ AVANTAJLAR

### 🎯 Basit ve Net
- Sadece SARI hücreler input
- Gereksiz renkler yok
- Anlaşılır formüller

### 🔧 Hata Önleyici  
- String başlıklar formüllerde yok
- #DEĞER hatası olmaz
- Temiz hesaplama

### ⚡ Kolay Kullanım
- Nereden veri gireceğiniz belli
- Otomatik hesaplama
- Basit mantık

## 📊 ÖRNEK KULLANIM

### 1. Proje Parametreleri (Sayfa 5):
```
Tünel Uzunluğu: 250m
Tünel Sayısı: 50 adet
Tünel Genişlik: 9.6m
```

### 2. Otomatik Hesaplanan:
```
Toplam Alan: 120.000 m²
Montaj Noktası: 2.601 adet
Ara Direk: 12.500 m
```

### 3. Sonuç:
```
Toplam Maliyet: ~4.5M TL
M² Başına: ~38 TL/m²
```

## 🎯 ÖNEMLİ NOTLAR

### ✅ YAPILACAKLAR:
- SARI hücrelere değer girin
- Malzeme fiyatlarını güncelleyin
- Proje parametrelerini ayarlayın

### ❌ YAPILMAYACAKLAR:
- Beyaz hücreleri değiştirmeyin
- Formülleri bozmayın
- Gereksiz hücreler eklemeyin

## 🔄 YENİ MALZEME EKLEME

### Basit Adımlar:
1. İlgili sayfaya gidin (2, 3 veya 4)
2. Son malzemeden sonraki satıra yazın
3. TOPLAM satırını aşağı taşıyın
4. Formülü güncelleyin: `=SUM(D4:D[yeni_satır])`

## 📈 SONUÇ ALMA

### Sayfa 5'te Göreceksiniz:
- Toplam malzeme maliyeti
- İşçilik, nakliye, kar marjları
- KDV dahil/hariç fiyatlar
- M² başına maliyet

---

**🎯 ÖZET**: Sadece SARI hücreleri doldurun, gerisini sistem halleder!**

**📁 Dosya**: `Sera_Basit_Sistem.xlsx`  
**📅 Tarih**: Ağustos 2025  
**✅ Durum**: Kullanıma Hazır
