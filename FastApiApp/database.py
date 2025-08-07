import sqlite3
import os

# Veritabanı dosya yolu
DATABASE_PATH = "sales_data.db"

def init_db():
    """Veritabanını oluşturur ve örnek verilerle doldurur"""
    # Eğer veritabanı zaten varsa sil (temiz başlamak için)
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
    
    # Veritabanı bağlantısı oluştur
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Ürünler tablosu oluştur
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    ''')
    
    # Satışlar tablosu oluştur
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        sale_date TEXT NOT NULL,
        total_price REAL NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')
    
    # Örnek ürün verileri
    products = [
        ('Laptop', 'Elektronik', 5000.0, 20),
        ('Akıllı Telefon', 'Elektronik', 3500.0, 30),
        ('Tablet', 'Elektronik', 2000.0, 15),
        ('Kulaklık', 'Aksesuar', 500.0, 50),
        ('Klavye', 'Aksesuar', 300.0, 40)
    ]
    
    cursor.executemany('INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)', products)
    
    # Örnek satış verileri
    sales = [
        (1, 2, '2023-11-01', 10000.0),
        (2, 1, '2023-11-02', 3500.0),
        (3, 3, '2023-11-03', 6000.0),
        (4, 5, '2023-11-04', 2500.0),
        (5, 2, '2023-11-05', 600.0)
    ]
    
    cursor.executemany('INSERT INTO sales (product_id, quantity, sale_date, total_price) VALUES (?, ?, ?, ?)', sales)
    
    # Değişiklikleri kaydet ve bağlantıyı kapat
    conn.commit()
    conn.close()
    
    print(f"Veritabanı '{DATABASE_PATH}' başarıyla oluşturuldu ve örnek veriler eklendi.")

def get_db_connection():
    """Veritabanı bağlantısı döndürür"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Sözlük benzeri erişim için
    return conn
