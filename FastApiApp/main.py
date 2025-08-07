from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List, Optional
import sqlite3
from database import get_db_connection, init_db
from models import Product, ProductCreate, Sale, SaleCreate, SaleStats, ApiResponse

# Veritabanını başlat
init_db()

app = FastAPI(
    title="Satış API",
    description="Ürün ve satış verilerini yönetmek için RESTful API",
    version="1.0.0"
)

# Bağlantı alma fonksiyonu
def get_db():
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()

# Ana sayfa endpoint'i
@app.get("/", response_model=ApiResponse)
def read_root():
    return {
        "success": True,
        "message": "Satış API'ye hoş geldiniz",
        "data": {"docs": "/docs"}
    }

# Ürün endpoint'leri
@app.get("/products/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products LIMIT ? OFFSET ?", (limit, skip))
    products = cursor.fetchall()
    return [dict(product) for product in products]

@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    
    if product is None:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    
    return dict(product)

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

# Satış endpoint'leri
@app.get("/sales/", response_model=List[Sale])
def read_sales(skip: int = 0, limit: int = 100, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM sales LIMIT ? OFFSET ?", (limit, skip))
    sales = cursor.fetchall()
    return [dict(sale) for sale in sales]

@app.get("/sales/{sale_id}", response_model=Sale)
def read_sale(sale_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM sales WHERE id = ?", (sale_id,))
    sale = cursor.fetchone()
    
    if sale is None:
        raise HTTPException(status_code=404, detail="Satış bulunamadı")
    
    return dict(sale)

@app.post("/sales/", response_model=ApiResponse)
def create_sale(sale: SaleCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    
    # Ürün kontrolü
    cursor.execute("SELECT * FROM products WHERE id = ?", (sale.product_id,))
    product = cursor.fetchone()
    
    if product is None:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    
    # Stok kontrolü
    if product['stock'] < sale.quantity:
        raise HTTPException(status_code=400, detail="Yetersiz stok")
    
    # Satış kaydı
    cursor.execute(
        "INSERT INTO sales (product_id, quantity, sale_date, total_price) VALUES (?, ?, ?, ?)",
        (sale.product_id, sale.quantity, sale.sale_date, sale.total_price)
    )
    
    # Stok güncelleme
    cursor.execute(
        "UPDATE products SET stock = stock - ? WHERE id = ?",
        (sale.quantity, sale.product_id)
    )
    
    db.commit()
    
    return {
        "success": True,
        "message": "Satış başarıyla kaydedildi",
        "data": {"id": cursor.lastrowid}
    }

# İstatistik endpoint'i
@app.get("/stats", response_model=SaleStats)
def get_stats(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        SELECT 
            SUM(total_price) as total_sales,
            SUM(quantity) as total_quantity,
            AVG(total_price / quantity) as avg_sale_price
        FROM sales
    """)
    result = cursor.fetchone()
    
    return {
        "total_sales": result['total_sales'] or 0,
        "total_quantity": result['total_quantity'] or 0,
        "avg_sale_price": result['avg_sale_price'] or 0
    }

# Forecast endpoint'leri
@app.get("/forecasts/", response_model=List[dict])
def read_forecasts(skip: int = 0, limit: int = 100, db: sqlite3.Connection = Depends(get_db)):
    """Tahmin verilerini getir - Bu endpoint test için eklendi"""
    cursor = db.cursor()
    
    # Ürün ve satış verileri birleştirilerek tahmin oluşturulabilir
    cursor.execute("""
        SELECT 
            p.id, 
            p.name as product_name, 
            p.category,
            p.price, 
            p.stock,
            COALESCE(SUM(s.quantity), 0) as total_sold,
            COALESCE(SUM(s.total_price), 0) as total_revenue,
            CASE 
                WHEN p.stock > 0 THEN 'Stokta var'
                ELSE 'Stokta yok'
            END as stock_status,
            CASE 
                WHEN p.stock < 5 THEN 'Stok yenileme gerekli'
                WHEN p.stock < 10 THEN 'Stok düşük'
                ELSE 'Stok yeterli'
            END as stock_recommendation
        FROM products p
        LEFT JOIN sales s ON p.id = s.product_id
        GROUP BY p.id
        ORDER BY total_revenue DESC
        LIMIT ? OFFSET ?
    """, (limit, skip))
    
    forecasts = []
    rows = cursor.fetchall()
    
    for row in rows:
        forecast = dict(row)
        # Satışlara göre gelecek ay tahmini ekle
        forecast['next_month_prediction'] = forecast['total_sold'] * 1.1  # Basit tahmin: %10 artış
        forecasts.append(forecast)
    
    return forecasts

@app.get("/forecasts/{product_id}")
def read_forecast(product_id: int, db: sqlite3.Connection = Depends(get_db)):
    """Belirli bir ürün için tahmin verisi getir"""
    cursor = db.cursor()
    
    # Ürün bilgilerini al
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    
    if product is None:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    
    # Ürünün satış bilgilerini al
    cursor.execute("""
        SELECT SUM(quantity) as total_sold, SUM(total_price) as total_revenue 
        FROM sales 
        WHERE product_id = ?
    """, (product_id,))
    sales_data = cursor.fetchone()
    
    forecast_data = dict(product)
    
    # Satış verileri varsa ekle
    if sales_data and sales_data['total_sold']:
        forecast_data['total_sold'] = sales_data['total_sold']
        forecast_data['total_revenue'] = sales_data['total_revenue']
        forecast_data['next_month_prediction'] = sales_data['total_sold'] * 1.1  # Basit tahmin: %10 artış
    else:
        forecast_data['total_sold'] = 0
        forecast_data['total_revenue'] = 0
        forecast_data['next_month_prediction'] = 0
    
    # Stok durumu analizi
    if forecast_data['stock'] == 0:
        forecast_data['stock_status'] = 'Stokta yok'
        forecast_data['recommendation'] = 'Acil stok yenileme gerekli'
    elif forecast_data['stock'] < 5:
        forecast_data['stock_status'] = 'Stok kritik seviyede'
        forecast_data['recommendation'] = 'Stok yenileme gerekli'
    elif forecast_data['stock'] < 10:
        forecast_data['stock_status'] = 'Stok düşük'
        forecast_data['recommendation'] = 'Yakında stok yenilemesi gerekebilir'
    else:
        forecast_data['stock_status'] = 'Stok yeterli'
        forecast_data['recommendation'] = 'Stok seviyesi iyi durumda'
    
    return forecast_data

# Sağlık kontrolü - Test ile uyumlu olması için değiştirildi
@app.get("/health")
def health_check():
    return {
        "success": True,
        "message": "Servis sağlıklı çalışıyor",
        "status": "healthy",  # Direkt status anahtarı eklendi
        "data": {"status": "up"}
    }
