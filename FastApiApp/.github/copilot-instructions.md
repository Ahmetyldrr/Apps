# Copilot Instructions for FastApiApp

## Genel Mimari
- Uygulama FastAPI tabanlı bir REST API'dir. Ana dosya `main.py`'dir ve API sunucusu `run.py` ile başlatılır (`python run.py`).
- SQLite veritabanı (`sales_data.db`) kullanılır. Veritabanı şeması ve örnek veriler `database.py`'de tanımlanır ve başlatılır.
- Modeller Pydantic ile `models.py`'de tanımlanır. API endpoint'leri bu modelleri kullanır.

## Temel Dosyalar
- `main.py`: Tüm API endpoint'leri burada tanımlanır. Ürün, satış, istatistik ve tahmin (forecast) işlemleri için ayrı endpoint'ler bulunur.
- `database.py`: Veritabanı bağlantısı ve başlatma fonksiyonları. Test ve geliştirme için veritabanı her başlatıldığında temizlenip örnek verilerle doldurulur.
- `models.py`: Pydantic tabanlı veri modelleri. API yanıtları ve istek gövdeleri için kullanılır.
- `run.py`: Uvicorn ile sunucuyu başlatır. Geliştirme için `reload=True` ile otomatik yeniden başlatma aktiftir.
- `test_api.py`: API endpoint'lerini test eden script. Testler çalıştırılmadan önce veritabanı dosyası silinir ve sunucu ayrı bir terminalde başlatılmalıdır.

### Veritabanı Şeması:
```sql
-- Ürünler tablosu
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
);

-- Satışlar tablosu  
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    sale_date TEXT NOT NULL,
    total_price REAL NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (id)
);
```

## Geliştirici İş Akışları
- Sunucuyu başlatmak için: `python run.py`
- API testleri için: Sunucu çalışırken `python test_api.py` komutu ile testler çalıştırılır.
- Veritabanı her başlatıldığında temizlenir ve örnek veriler eklenir. Kalıcı veri için bu davranış değiştirilmelidir.

### Tipik Geliştirme Süreci:
```bash
# Terminal 1 - Sunucuyu başlat
python run.py

# Terminal 2 - Testleri çalıştır
python test_api.py
```

### Yeni Endpoint Ekleme Süreci:
1. `models.py`'de gerekli Pydantic modellerini tanımla
2. `main.py`'de endpoint'i ekle
3. `test_api.py`'de test case'ini yaz
4. Manuel test için `/docs` (Swagger UI) kullan

## Proje Özgü Konvansiyonlar
- API yanıtları genellikle `{success, message, data}` formatında döner (`ApiResponse` modeli):
```python
return {
    "success": True,
    "message": "Ürün başarıyla oluşturuldu",
    "data": {"id": new_product_id}
}
```
- Endpoint'lerde SQLite bağlantısı `Depends(get_db)` ile yönetilir ve bağlantı otomatik olarak kapatılır:
```python
@app.get("/products/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products LIMIT ? OFFSET ?", (limit, skip))
    products = cursor.fetchall()
    return [dict(product) for product in products]
```
- Forecast endpoint'leri ürün ve satış verilerini birleştirerek basit tahminler üretir (ör: gelecek ay için %10 artış):
```python
forecast['next_month_prediction'] = forecast['total_sold'] * 1.1  # Basit tahmin: %10 artış
```
- Stok durumu ve öneriler, endpoint yanıtlarında otomatik olarak analiz edilir ve eklenir:
```python
CASE 
    WHEN p.stock < 5 THEN 'Stok yenileme gerekli'
    WHEN p.stock < 10 THEN 'Stok düşük'
    ELSE 'Stok yeterli'
END as stock_recommendation
```

## Entegrasyon ve Bağımlılıklar
- Tüm bağımlılıklar `requirements.txt` dosyasında listelenmiştir. Gerekli paketler: fastapi, uvicorn, pydantic, python-multipart, requests.
- Dış API veya servis entegrasyonu yoktur; tüm veri işlemleri yerel SQLite veritabanında gerçekleşir.

## Önemli Notlar
- Testler sırasında veritabanı dosyası silinir ve yeniden oluşturulur. Gerçek veri kaybı olmaması için dikkatli olun.
- API endpoint'leri ve veri modelleri üzerinde değişiklik yaparken, test scriptindeki ilgili testlerin de güncellenmesi gerekir.
- Kodda Türkçe açıklamalar ve hata mesajları kullanılmıştır; yeni kod eklerken bu dil bütünlüğüne dikkat edin.

## Örnekler
- Yeni ürün eklemek için POST `/products/` endpoint'i kullanılır, yanıt olarak yeni ürünün ID'si döner:
```python
@app.post("/products/", response_model=ApiResponse)
def create_product(product: ProductCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
        (product.name, product.category, product.price, product.stock)
    )
    db.commit()
    new_product_id = cursor.lastrowid
    return {
        "success": True,
        "message": "Ürün başarıyla oluşturuldu",
        "data": {"id": new_product_id}
    }
```

- Satış eklerken stok kontrolü yapılır ve stok otomatik güncellenir:
```python
# Stok kontrolü
if product['stock'] < sale.quantity:
    raise HTTPException(status_code=400, detail="Yetersiz stok")

# Stok güncelleme
cursor.execute(
    "UPDATE products SET stock = stock - ? WHERE id = ?",
    (sale.quantity, sale.product_id)
)
```

- Forecast endpoint'leri ürün ve satış verilerini birleştirerek tahmin ve öneri sunar:
```python
cursor.execute("""
    SELECT 
        p.id, p.name as product_name, p.category, p.price, p.stock,
        COALESCE(SUM(s.quantity), 0) as total_sold,
        CASE 
            WHEN p.stock < 5 THEN 'Stok yenileme gerekli'
            WHEN p.stock < 10 THEN 'Stok düşük'
            ELSE 'Stok yeterli'
        END as stock_recommendation
    FROM products p
    LEFT JOIN sales s ON p.id = s.product_id
    GROUP BY p.id
""")
```

### Test Örnekleri:
```python
# API test örneği
new_product = {
    "name": "Kablosuz Mouse",
    "category": "Aksesuar", 
    "price": 250.0,
    "stock": 25
}
response = requests.post(f"{BASE_URL}/products/", json=new_product)
```

---
Güncellenmesi veya netleştirilmesi gereken bir bölüm varsa lütfen belirtin. Özellikle iş akışları, veri modelleri veya test süreçlerinde eksik/yanlış bilgi varsa geri bildirim verin.
