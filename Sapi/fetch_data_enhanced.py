import pandas as pd
from sqlalchemy import create_engine, text
import os

def get_db_config():
    """
    Veritabanı konfigürasyonunu environment variables'dan veya default değerlerden alır.
    GitHub Codespaces'te güvenlik için environment variables kullanın.
    """
    return {
        "dbname": os.getenv("DB_NAME", "soccerdb"),
        "user": os.getenv("DB_USER", "ahmet21"),
        "password": os.getenv("DB_PASSWORD", "diclem2121."),
        "host": os.getenv("DB_HOST", "165.227.130.23"),
        "port": os.getenv("DB_PORT", "5432")
    }

def fetch_data_from_db(query=None, limit=None):
    """
    Veritabanından verileri DataFrame olarak çeker.
    
    Parameters:
    - query: Özel SQL sorgusu (opsiyonel). Verilmezse tüm veriler çekilir.
    - limit: Çekilecek maksimum kayıt sayısı (opsiyonel)
    
    Returns:
    - pandas.DataFrame: Veritabanından çekilen veriler
    """
    db_config = get_db_config()
    
    engine = create_engine(
        f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    )
    
    try:
        with engine.connect() as conn:
            print("✅ Veritabanı bağlantısı başarılı.")
            
            # Özel sorgu verilmemişse tüm verileri çek
            if query is None:
                if limit:
                    query = f"SELECT * FROM hamdata LIMIT {limit}"
                else:
                    query = "SELECT * FROM hamdata"
            
            # Verileri DataFrame olarak çek
            df = pd.read_sql(query, conn)
            print(f"📊 Toplam {len(df)} kayıt çekildi.")
            
            return df
            
    except Exception as e:
        print(f"❌ Veritabanı işlemi sırasında bir hata oluştu: {e}")
        return pd.DataFrame()  # Boş DataFrame döndür
    finally:
        engine.dispose()
        print("🔌 Veritabanı bağlantısı kapatıldı.")

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

def get_matches_by_date(start_date, end_date=None):
    """
    Belirli tarih aralığındaki maçları çeker.
    
    Parameters:
    - start_date: Başlangıç tarihi (YYYY-MM-DD formatında)
    - end_date: Bitiş tarihi (opsiyonel, verilmezse sadece start_date)
    
    Returns:
    - pandas.DataFrame: Belirtilen tarihlerdeki maçlar
    """
    if end_date:
        query = f"""
        SELECT * FROM hamdata 
        WHERE col_1::date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY col_1 DESC
        """
    else:
        query = f"""
        SELECT * FROM hamdata 
        WHERE col_1::date = '{start_date}'
        ORDER BY col_1 DESC
        """
    return fetch_data_from_db(query)

def get_match_statistics():
    """
    Veritabanındaki maç istatistiklerini çeker.
    
    Returns:
    - dict: Çeşitli istatistikler
    """
    db_config = get_db_config()
    
    engine = create_engine(
        f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    )
    
    try:
        with engine.connect() as conn:
            print("✅ Veritabanı bağlantısı başarılı.")
            
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
            
            # Benzersiz takım sayısı (yaklaşık)
            unique_teams = pd.read_sql("""
                SELECT COUNT(DISTINCT team) as unique_teams FROM (
                    SELECT col_2 as team FROM hamdata 
                    UNION 
                    SELECT col_3 as team FROM hamdata
                ) t
            """, conn)
            stats['unique_teams'] = unique_teams['unique_teams'].iloc[0]
            
            return stats
            
    except Exception as e:
        print(f"❌ Veritabanı işlemi sırasında bir hata oluştu: {e}")
        return {}
    finally:
        engine.dispose()

def export_to_csv(df, filename="football_data.csv"):
    """
    DataFrame'i CSV dosyasına aktarır.
    
    Parameters:
    - df: pandas.DataFrame
    - filename: Dosya adı
    """
    try:
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"📁 Veriler {filename} dosyasına aktarıldı.")
        return True
    except Exception as e:
        print(f"❌ CSV aktarımında hata: {e}")
        return False

def analyze_team_performance(team_name, limit=20):
    """
    Bir takımın performans analizini yapar.
    
    Parameters:
    - team_name: Takım adı
    - limit: Analiz edilecek maksimum maç sayısı
    
    Returns:
    - dict: Takım performans istatistikleri
    """
    matches = search_team_matches(team_name)
    
    if matches.empty:
        return {"error": f"{team_name} takımı için maç bulunamadı."}
    
    # İlk 'limit' kadar maçı analiz et
    matches = matches.head(limit)
    
    analysis = {
        "team_name": team_name,
        "total_matches": len(matches),
        "date_range": f"{matches['col_1'].min()} - {matches['col_1'].max()}",
        "sample_matches": matches[['col_1', 'col_2', 'col_3']].head().to_dict('records')
    }
    
    return analysis

# Örnek kullanımlar
if __name__ == "__main__":
    print("🚀 === Veritabanından Veri Çekme Örnekleri ===\n")
    
    # 1. Veritabanı bağlantısını test et
    print("1. 📊 Veritabanı istatistikleri:")
    stats = get_match_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n" + "="*50)
    
    # 2. İlk 5 kaydı çek
    print("2. 📋 İlk 5 kaydı çekiyor...")
    df_sample = fetch_data_from_db(limit=5)
    if not df_sample.empty:
        print("   Örnek veriler:")
        print(df_sample)
        print(f"   📊 Toplam sütun sayısı: {len(df_sample.columns)}")
    
    print("\n" + "="*50)
    
    # 3. Son 3 günün verilerini çek
    print("3. 🗓️ Son 3 günün verileri:")
    recent_matches = get_latest_matches(3)
    print(f"   Son 3 günde {len(recent_matches)} maç bulundu.")
    
    print("\n" + "="*50)
    
    # 4. Belirli bir tarihteki maçları çek
    print("4. 📅 Belirli tarihteki maçlar (2025-08-01):")
    date_matches = get_matches_by_date("2025-08-01")
    print(f"   2025-08-01 tarihinde {len(date_matches)} maç bulundu.")
    
    print("\n" + "="*50)
    
    # 5. Takım arama örneği
    print("5. 🔍 Takım arama örneği (Galatasaray):")
    team_matches = search_team_matches("Galatasaray")
    print(f"   Galatasaray ile ilgili {len(team_matches)} maç bulundu.")
    
    if not team_matches.empty:
        # Takım analizi yap
        analysis = analyze_team_performance("Galatasaray", 10)
        print("   📈 Takım analizi:")
        for key, value in analysis.items():
            if key != "sample_matches":
                print(f"      {key}: {value}")
    
    print("\n🎉 Analiz tamamlandı!")
