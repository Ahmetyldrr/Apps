# SERA PROJESİ VBA MAKRO VE KULLANIM KILAVUZU

## 🎯 VBA MAKRO EKLEME ADIMları

### 1. Excel'de Geliştirici Sekmesini Aktifleştirin
- Excel'i açın
- Dosya > Seçenekler > Şeridi Özelleştir
- "Geliştirici" seçeneğini işaretleyin

### 2. VBA Editörünü Açın
- Geliştirici sekmesi > Visual Basic
- Veya ALT + F11 tuşlarına basın

### 3. Makro Kodunu Ekleyin
- Sol panelde "VBAProject (Sera_Ultimate_Professional_System.xlsx)" öğesini bulun
- "Microsoft Excel Objects" > "Sheet1 (Dashboard)" öğesine çift tıklayın
- Aşağıdaki kodu yapıştırın:

```vba
Private Sub Worksheet_Change(ByVal Target As Range)
    Application.EnableEvents = False
    Application.ScreenUpdating = False
    
    ' SARI hücrelerde değişiklik olduğunda çalışır
    If Target.Interior.Color = RGB(255, 255, 0) Then
        ' Hesaplama sayfasındaki sonuçları güncelle
        Worksheets("Dashboard").Range("C10").Value = "Güncelleniyor..."
        Application.Calculate
        DoEvents
        
        ' Durum güncelle
        Dim totalCost As Double
        totalCost = Worksheets("Hesaplama").Range("C35").Value
        
        If totalCost > 0 Then
            Worksheets("Dashboard").Range("C10").Value = "Hesaplandı ✓"
        Else
            Worksheets("Dashboard").Range("C10").Value = "Hata ⚠"
        End If
    End If
    
    Application.EnableEvents = True
    Application.ScreenUpdating = True
End Sub

Sub HesaplamaGuncelle()
    Application.Calculate
    MsgBox "Tüm hesaplamalar güncellendi!", vbInformation
End Sub

Sub YeniProje()
    ' Tüm SARI hücreleri temizle
    Dim ws As Worksheet
    For Each ws In ActiveWorkbook.Worksheets
        Dim cell As Range
        For Each cell In ws.UsedRange
            If cell.Interior.Color = RGB(255, 255, 0) Then
                If IsNumeric(cell.Value) Then
                    cell.Value = 0
                Else
                    cell.Value = ""
                End If
            End If
        Next cell
    Next ws
    
    MsgBox "Yeni proje için sistem temizlendi!", vbInformation
End Sub
```

### 4. Dosyayı Makro Etkin Olarak Kaydedin
- Dosya > Farklı Kaydet
- "Excel Macro-Enabled Workbook (*.xlsm)" formatını seçin

## 📋 KULLANIM KILAVUZU

### ⭐ Dashboard (Kontrol Paneli)
- **Amaç**: Projenin genel durumunu görme
- **Özellikler**: 
  - Toplam maliyet otomatik hesaplanır
  - M² başına maliyet gösterilir
  - Sistem durumu takip edilir

### 🔧 Montaj Sekmesi
- **SARI hücreler**: Miktar ve fiyat bilgilerini girin
- **Özellikler**:
  - 1 montaj noktası için gerekli malzemeler
  - Otomatik toplam hesaplama
  - Hesaplama sekmesine veri aktarımı

### 📏 Direk Sekmesi  
- **SARI hücreler**: Miktar ve fiyat bilgilerini girin
- **Özellikler**:
  - 1 metre ara direk için malzemeler
  - Otomatik toplam hesaplama

### 🏗️ Müştemilat Sekmesi
- **SARI hücreler**: Miktar ve fiyat bilgilerini girin
- **Özellikler**:
  - 1 adet müştemilat direk için malzemeler
  - Özel işçilik ve beton hesaplamaları

### 🧮 Hesaplama Sekmesi
- **SARI hücreler**: Proje parametrelerini girin
  - Tünel uzunluğu (m)
  - Tünel sayısı 
  - Tünel genişlik (m)
  - Orta kolon aralığı (m)
  - Müştemilat direk sayısı (manuel)

- **Otomatik Hesaplamalar**:
  - Toplam alan
  - Montaj noktası sayısı
  - Ara direk uzunluğu
  - Tüm maliyet kalemleri

## 🎯 ÖZEL ÖZELLİKLER

### 🟡 Akıllı Input Sistemi
- Tüm SARI hücreler input alanıdır
- Değiştirdiğinizde sistem otomatik güncellenir
- VBA makro sayesinde anlık hesaplama

### ⚡ Otomatik Güncelleme
- SARI hücrede değişiklik → Otomatik hesaplama
- Dashboard durumu güncellenir
- Cross-sheet formüller çalışır

### 🔄 Yedek İşlemler
- `HesaplamaGuncelle()` makrosu: Manuel güncelleme
- `YeniProje()` makrosu: Tüm verileri temizle

## ⚠️ ÖNEMLİ NOTLAR

1. **Makro Güvenliği**: Excel'de makrolar etkinleştirilmeli
2. **Dosya Formatı**: .xlsm olarak kaydedin
3. **SARI Hücreler**: Sadece bunlara veri girin
4. **Formüller**: Diğer hücrelerdeki formülleri değiştirmeyin

## 🎉 AVANTAJLAR

✅ Profesyonel görünüm
✅ Kolay kullanım (SARI = INPUT)
✅ Otomatik hesaplama
✅ Sayfalar arası entegrasyon
✅ VBA makro desteği
✅ Hata kontrolü
✅ Dashboard kontrol paneli
✅ Maliyet takibi
