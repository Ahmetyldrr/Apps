# SERA PROJESİ MALİYET HESAPLAMA SİSTEMİ

## Proje Açıklaması

Bu proje, sera yapı projelerinde kullanılan malzemelerin maliyetini hesaplamak için tasarlanmış bir Excel tabanlı hesaplama sistemidir.

## Proje Kapsamı

Sera projelerinde 3 ana maliyet kalemi bulunmaktadır:

1. **Montaj Noktaları**: Seralarda girintili çıkıntılı montaj noktalarının maliyeti
2. **Ara Direkler**: Montaj noktalarını birbirine bağlayan direkler (metre başına)
3. **Müştemilat Direkleri**: Ortada bulunan teknik oda/kazan alanı direkleri (2.5m aralıklarla)

## Excel Dosyası Yapısı

### 1. Sekme: Proje Tanımları
- Temel proje parametreleri (tünel uzunluğu, sayısı, genişlik vb.)
- Otomatik hesaplanan değerler (toplam alan, montaj noktası sayısı, direk uzunluğu)

### 2. Sekme: 1 Montaj Noktası Maliyeti
- Montaj noktasında kullanılan malzemeler ve fiyatları
- Otomatik toplam maliyet hesaplaması

### 3. Sekme: 1 Metre Direk Maliyeti
- Ara direklerde kullanılan malzemeler ve fiyatları
- Otomatik toplam maliyet hesaplaması

### 4. Sekme: 1 Müştemilat Direk Maliyeti
- Müştemilat direklerinde kullanılan malzemeler ve fiyatları
- Otomatik toplam maliyet hesaplaması

### 5. Sekme: Toplam Maliyet Hesaplama
- Tüm kalemlerin toplam maliyeti
- İşçilik, nakliye, kar marjı hesaplamaları
- KDV dahil/hariç toplam fiyatlar
- M² başına maliyet hesaplaması

## Kullanım Talimatları

### Adım 1: Proje Parametrelerini Girin
1. "1-Proje Tanımları" sekmesinde proje bilgilerini güncelleyin
2. Sistem otomatik olarak hesaplanan değerleri güncelleyecektir

### Adım 2: Birim Maliyetleri Güncelleyin
1. "2-Montaj Noktası" sekmesinde malzeme fiyatlarını güncelleyin
2. "3-Metre Direk" sekmesinde direk maliyetlerini güncelleyin
3. "4-Müştemilat Direk" sekmesinde müştemilat maliyetlerini güncelleyin

### Adım 3: Toplam Maliyeti Kontrol Edin
1. "5-Toplam Maliyet" sekmesinde sonuçları inceleyin
2. Gerekirse müştemilat direk sayısını ayarlayın
3. İşçilik, nakliye ve kar marjı oranlarını kontrol edin

## Önemli Formüller

### Toplam Montaj Noktası Hesaplama
```
=(Tünel Uzunluğu/Orta Kolon Aralığı+1)*(Tünel Sayısı+1)
```

### Toplam Alan Hesaplama
```
=Tünel Uzunluğu * Tünel Sayısı * Tünel Genişlik
```

### Toplam Direk Uzunluğu
```
=Tünel Uzunluğu * Tünel Sayısı
```

## Örnek Hesaplama

### Varsayılan Değerler:
- Tünel Uzunluğu: 250m
- Tünel Sayısı: 50 adet
- Tünel Genişlik: 9.6m
- Toplam Alan: 120.000 m²
- Toplam Montaj Noktası: 2.601 adet
- Toplam Direk Uzunluğu: 12.500m
- Müştemilat Direk: 25 adet

### Maliyet Breakdown:
- 1 Montaj Noktası: ~601.75 TL
- 1 Metre Direk: ~162.00 TL
- 1 Müştemilat Direk: ~444.50 TL

### Sonuç:
- Toplam Malzeme Maliyeti: ~3.601.328 TL
- KDV Dahil Toplam: ~5.618.072 TL
- M² Başına Maliyet: ~46.82 TL/m²

## Dosya Bilgileri

- **Ana Excel Dosyası**: `Sera_Proje_Maliyet_Hesaplama.xlsx`
- **Python Kaynak Kodu**: `create_excel.py`
- **Proje Talimatları**: `talimatlar.md`

## Geliştirme Notları

1. Excel formülleri otomatik güncellenecek şekilde tasarlanmıştır
2. Malzeme fiyatları ve miktarları kolayca değiştirilebilir
3. Sistem yeni malzeme kalemleri eklemeye uygun yapıdadır
4. Tüm hesaplamalar birbirine bağlı olarak çalışmaktadır

## Gelecek Geliştirmeler

1. Malzeme veritabanı entegrasyonu
2. Fiyat güncellemelerinin otomatik çekilmesi
3. Raporlama ve yazdırma özelliklerinin geliştirilmesi
4. Farklı sera tiplerini destekleme
5. Web tabanlı arayüz geliştirme

---

**Geliştirici**: Sera App Team  
**Tarih**: Ağustos 2025  
**Versiyon**: 1.0
