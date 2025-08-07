from sqlalchemy import create_engine, text

def count_records_in_db():
    """Counts the total number of records in the 'hamdata' table."""
    db_config = {
        "dbname": "soccerdb",
        "user": "ahmet21",
        "password": "diclem2121.",
        "host": "165.227.130.23",
        "port": "5432"
    }
    engine = create_engine(
        f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    )

    try:
        with engine.connect() as conn:
            print("\nVeritabanı bağlantısı başarılı.")
            count_query = text("SELECT COUNT(*) FROM hamdata;")
            result = conn.execute(count_query).scalar()
            print(f"Veritabanındaki 'hamdata' tablosunda toplam {result} kayıt bulunmaktadır.")
    except Exception as e:
        print(f"\nVeritabanı işlemi sırasında bir hata oluştu: {e}")
    finally:
        engine.dispose()
        print("Veritabanı bağlantısı kapatıldı.")

# Fonksiyonu çalıştır
count_records_in_db()