import pandas as pd
from sqlalchemy import create_engine, text

def fetch_data_from_db(query=None, limit=None):
    """
    Veritabanından verileri DataFrame olarak çeker.
    
    Parameters:
    - query: Özel SQL sorgusu (opsiyonel). Verilmezse tüm veriler çekilir.
    - limit: Çekilecek maksimum kayıt sayısı (opsiyonel)
    
    Returns:
    - pandas.DataFrame: Veritabanından çekilen veriler
    """
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
            print("Veritabanı bağlantısı başarılı.")
            
            # Özel sorgu verilmemişse tüm verileri çek
            if query is None:
                if limit:
                    query = f"SELECT * FROM hamdata LIMIT {limit}"
                else:
                    query = "SELECT * FROM hamdata"
            
            # Verileri DataFrame olarak çek
            df = pd.read_sql(query, conn)
            print(f"Toplam {len(df)} kayıt çekildi.")
            
            return df
            
    except Exception as e:
        print(f"Veritabanı işlemi sırasında bir hata oluştu: {e}")
        return pd.DataFrame()  # Boş DataFrame döndür
    finally:
        engine.dispose()
        print("Veritabanı bağlantısı kapatıldı.")

def get_latest_matches(days=7):
    """
    Son N günün maç verilerini çeker.
    
    Parameters:
    - days: Kaç günlük veri çekileceği
    
    Returns:
    - pandas.DataFrame: Son günlerin maç verileri
    """
    query = f"""
    SELECT * FROM hamdata 
    WHERE col_1::date >= CURRENT_DATE - INTERVAL '{days} days'
    ORDER BY col_1 DESC
    """
    return fetch_data_from_db(query)

def search_team_matches(team_name):
    """
    Belirli bir takımın maçlarını arar.
    
    Parameters:
    - team_name: Aranacak takım adı
    
    Returns:
    - pandas.DataFrame: Takımın maçları
    """
    query = f"""
    SELECT * FROM hamdata 
    WHERE col_2 ILIKE '%{team_name}%' OR col_3 ILIKE '%{team_name}%'
    ORDER BY col_1 DESC
    """
    return fetch_data_from_db(query)

def get_match_statistics():
    """
    Veritabanındaki maç istatistiklerini çeker.
    
    Returns:
    - dict: Çeşitli istatistikler
    """
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
            print("Veritabanı bağlantısı başarılı.")
            
            stats = {}
            
            # Toplam maç sayısı
            total_matches = pd.read_sql("SELECT COUNT(*) as total FROM hamdata", conn)
            stats['total_matches'] = total_matches['total'].iloc[0]
            
            # En son maç tarihi
            latest_date = pd.read_sql("SELECT MAX(col_1) as latest_date FROM hamdata", conn)
            stats['latest_date'] = latest_date['latest_date'].iloc[0]
            
            # En eski maç tarihi
            earliest_date = pd.read_sql("SELECT MIN(col_1) as earliest_date FROM hamdata", conn)
            stats['earliest_date'] = earliest_date['earliest_date'].iloc[0]
            
            return stats
            
    except Exception as e:
        print(f"Veritabanı işlemi sırasında bir hata oluştu: {e}")
        return {}
    finally:
        engine.dispose()

# Örnek kullanımlar
if __name__ == "__main__":
    print("=== Veritabanından Veri Çekme Örnekleri ===\n")
    
    # 1. Tüm verileri çek (ilk 10 kayıt)
    print("1. İlk 10 kaydı çekiyor...")
    df_all = fetch_data_from_db(limit=10)
    if not df_all.empty:
        print("İlk 5 kayıt:")
        print(df_all.head())
        print(f"Toplam sütun sayısı: {len(df_all.columns)}")
        print(f"Sütun adları: {list(df_all.columns)}")
    
    print("\n" + "="*50)
    
    # 2. İstatistikleri al
    print("2. Veritabanı istatistikleri:")
    stats = get_match_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print("\n" + "="*50)
    
    # 3. Son 3 günün verilerini çek
    print("3. Son 3 günün verileri:")
    recent_matches = get_latest_matches(3)
    print(f"Son 3 günde {len(recent_matches)} maç bulundu.")
    
    print("\n" + "="*50)
    
    # 4. Belirli bir takımı ara (örnek: Galatasaray)
    print("4. Takım arama örneği:")
    team_matches = search_team_matches("Galatasaray")
    print(f"Galatasaray ile ilgili {len(team_matches)} maç bulundu.")
