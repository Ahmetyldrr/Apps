from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import PolynomialFeatures, LabelEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score, classification_report
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from .models import ForecastData, ModelPerformance, AIAnalysis, EnergyMarketData
from .forms import ExcelUploadForm
from .ai_service import AIAnalysisService

def home(request):
    """Ana sayfa görünümü"""
    recent_energy_data = EnergyMarketData.objects.all()[:10]
    recent_performance = ModelPerformance.objects.all()[:5]
    recent_ai_analysis = AIAnalysis.objects.all()[:3]
    
    # SMF Yön dağılımı
    smf_direction_stats = EnergyMarketData.objects.values('smf_direction').annotate(
        count=models.Count('id')
    ).order_by('-count')
    
    context = {
        'recent_energy_data': recent_energy_data,
        'recent_performance': recent_performance,
        'recent_ai_analysis': recent_ai_analysis,
        'smf_direction_stats': smf_direction_stats,
    }
    return render(request, 'home.html', context)

def upload_excel(request):
    """Excel dosyası yükleme görünümü"""
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            try:
                # Excel dosyasını oku
                df = pd.read_excel(excel_file, engine='openpyxl')
                
                # Enerji piyasası verilerini işle
                processed_count = process_energy_market_data(df)
                
                messages.success(request, f'{processed_count} satır enerji piyasası verisi başarıyla yüklendi!')
                return redirect('energy_analysis')
                
            except Exception as e:
                messages.error(request, f'Excel dosyası işlenirken hata oluştu: {str(e)}')
    else:
        form = ExcelUploadForm()
    
    return render(request, 'upload_excel.html', {'form': form})

def process_energy_market_data(df):
    """Enerji piyasası verilerini işle ve veritabanına kaydet"""
    processed_count = 0
    
    # Sütun isimlerini standartlaştır
    column_mapping = {
        'Tarih': 'date',
        'Saat': 'hour', 
        'PTF': 'ptf',
        'SMF': 'smf',
        'Pozitif Dengesizlik Fiyatı (TL/MWh)': 'positive_imbalance_price',
        'Negatif Dengesizlik Fiyatı (TL/MWh)': 'negative_imbalance_price',
        'SMF Yön': 'smf_direction'
    }
    
    df = df.rename(columns=column_mapping)
    
    # SMF Yön değerlerini standartlaştır
    smf_direction_mapping = {
        'Enerji Açığı': 'enerji_acigi',
        'Enerji Fazlası': 'enerji_fazlasi', 
        'Dengede': 'dengede'
    }
    
    for index, row in df.iterrows():
        try:
            # Tarih ve saat parsing
            date_value = pd.to_datetime(row['date']).date()
            hour_value = pd.to_datetime(row['hour'], format='%H:%M').time()
            
            # Fiyat verilerini temizle (virgül -> nokta)
            ptf_value = float(str(row['ptf']).replace(',', '.'))
            smf_value = float(str(row['smf']).replace(',', '.'))
            pos_imb_price = float(str(row['positive_imbalance_price']).replace(',', '.'))
            neg_imb_price = float(str(row['negative_imbalance_price']).replace(',', '.'))
            
            # SMF Yön mapping
            smf_direction = smf_direction_mapping.get(row['smf_direction'], 'dengede')
            
            energy_data, created = EnergyMarketData.objects.get_or_create(
                date=date_value,
                hour=hour_value,
                defaults={
                    'ptf': ptf_value,
                    'smf': smf_value,
                    'positive_imbalance_price': pos_imb_price,
                    'negative_imbalance_price': neg_imb_price,
                    'smf_direction': smf_direction
                }
            )
            
            if not created:
                energy_data.ptf = ptf_value
                energy_data.smf = smf_value
                energy_data.positive_imbalance_price = pos_imb_price
                energy_data.negative_imbalance_price = neg_imb_price
                energy_data.smf_direction = smf_direction
                energy_data.save()
            
            processed_count += 1
            
        except (ValueError, TypeError) as e:
            print(f"Satır {index} işlenirken hata: {e}")
            continue
    
    return processed_count

def energy_analysis(request):
    """Enerji piyasası analizi görünümü"""
    data = EnergyMarketData.objects.all().order_by('date', 'hour')
    
    if not data.exists():
        messages.warning(request, 'Analiz için enerji piyasası verisi bulunamadı. Lütfen önce Excel dosyası yükleyin.')
        return redirect('upload_excel')
    
    # Veri istatistikleri
    df = pd.DataFrame(list(data.values()))
    
    stats = {
        'count': len(df),
        'ptf_mean': df['ptf'].mean(),
        'smf_mean': df['smf'].mean(),
        'ptf_std': df['ptf'].std(),
        'smf_std': df['smf'].std(),
        'first_date': df['date'].min(),
        'last_date': df['date'].max(),
    }
    
    # SMF Yön dağılımı
    smf_distribution = df['smf_direction'].value_counts()
    
    # Saatlik ortalamalar
    df['hour_only'] = pd.to_datetime(df['hour'], format='%H:%M:%S').dt.hour
    hourly_avg = df.groupby('hour_only')[['ptf', 'smf']].mean()
    
    # AI analizi yap (geçici olarak devre dışı)
    ai_analysis = {'status': 'disabled', 'analysis': 'AI servisi geçici olarak devre dışı'}
    
    # AI analizini kaydet
    if ai_analysis['status'] == 'success':
        AIAnalysis.objects.create(
            analysis_type='energy_market_analysis',
            content=ai_analysis['analysis'],
            status=ai_analysis['status']
        )
    
    # Grafik oluştur
    chart_data = create_energy_market_chart(df)
    
    context = {
        'data': data[:100],  # Son 100 kayıt göster
        'stats': stats,
        'smf_distribution': smf_distribution,
        'hourly_avg': hourly_avg,
        'ai_analysis': ai_analysis,
        'chart_data': chart_data,
    }
    return render(request, 'energy_analysis.html', context)

def smf_direction_prediction(request):
    """SMF Yön tahminlemesi görünümü"""
    data = EnergyMarketData.objects.all().order_by('date', 'hour')
    
    if len(data) < 50:
        messages.warning(request, 'SMF Yön tahmini için en az 50 veri noktası gerekli.')
        return redirect('energy_analysis')
    
    # Tahmin modellerini çalıştır
    results = run_smf_direction_models(data)
    
    # AI ile model performansını değerlendir (geçici olarak devre dışı)
    ai_evaluation = {'status': 'disabled', 'evaluation': 'AI servisi geçici olarak devre dışı'}
    
    # AI değerlendirmesini kaydet
    if ai_evaluation['status'] == 'success':
        AIAnalysis.objects.create(
            analysis_type='smf_prediction_evaluation',
            content=ai_evaluation['evaluation'],
            status=ai_evaluation['status']
        )
    
    context = {
        'results': results,
        'ai_evaluation': ai_evaluation,
    }
    return render(request, 'smf_prediction.html', context)

def run_smf_direction_models(data):
    """SMF Yön tahmin modellerini çalıştır"""
    # Veriyi DataFrame'e çevir
    df = pd.DataFrame(list(data.values()))
    
    print(f"Başlangıç veri sayısı: {len(df)}")  # Debug için
    
    # Temel veri kontrolleri
    if len(df) < 10:
        return {'error': f'Toplam veri sayısı yetersiz: {len(df)} (en az 10 gerekli)'}
    
    # Önce temel sütunları kontrol et
    required_columns = ['ptf', 'smf', 'positive_imbalance_price', 'negative_imbalance_price', 'smf_direction', 'hour']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return {'error': f'Eksik sütunlar: {missing_columns}'}
    
    # Sadece kritik NaN değerleri temizle
    initial_count = len(df)
    df = df.dropna(subset=['ptf', 'smf', 'smf_direction'])
    after_nan_clean = len(df)
    
    print(f"NaN temizleme sonrası: {after_nan_clean} (silinen: {initial_count - after_nan_clean})")
    
    if len(df) < 10:
        return {'error': f'NaN temizleme sonrası yetersiz veri: {len(df)} (en az 10 gerekli)'}
    
    # Feature engineering - daha güvenli
    df['ptf_smf_diff'] = df['ptf'] - df['smf']
    
    # Sıfıra bölmeyi önle
    df['ptf_smf_ratio'] = df.apply(lambda row: row['ptf'] / row['smf'] if row['smf'] != 0 else 0, axis=1)
    
    # Dengesizlik farkı
    df['imbalance_spread'] = df['negative_imbalance_price'] - df['positive_imbalance_price']
    
    # Saat bilgisini çıkar
    try:
        df['hour_only'] = pd.to_datetime(df['hour'], format='%H:%M:%S').dt.hour
    except:
        try:
            df['hour_only'] = pd.to_datetime(df['hour']).dt.hour
        except:
            df['hour_only'] = 0  # Varsayılan değer
    
    # Sadece extreme infinity değerleri temizle
    for col in ['ptf_smf_ratio', 'ptf_smf_diff', 'imbalance_spread']:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        df[col] = df[col].fillna(0)
    
    after_inf_clean = len(df)
    print(f"Infinity temizleme sonrası: {after_inf_clean}")
    
    # Saatlik dummy variables (sadece mevcut saatler için)
    unique_hours = df['hour_only'].unique()
    for hour in unique_hours:
        df[f'hour_{hour}'] = (df['hour_only'] == hour).astype(int)
    
    # Feature'ları seç - sadece mevcut olanlar
    base_features = ['ptf', 'smf', 'positive_imbalance_price', 'negative_imbalance_price', 
                    'ptf_smf_diff', 'ptf_smf_ratio', 'imbalance_spread']
    
    hour_features = [f'hour_{hour}' for hour in unique_hours]
    feature_columns = base_features + hour_features
    
    # Eksik feature'ları kontrol et
    available_features = [col for col in feature_columns if col in df.columns]
    print(f"Kullanılabilir feature sayısı: {len(available_features)}")
    
    X = df[available_features].fillna(0)
    y = df['smf_direction']
    
    # Son veri kontrolü
    if len(X) < 10 or len(y.unique()) < 2:
        return {'error': f'Model eğitimi için yetersiz veri veya sınıf çeşitliliği: {len(X)} veri, {len(y.unique())} sınıf'}
    
    print(f"Final veri: {len(X)} satır, {len(X.columns)} feature, {len(y.unique())} sınıf")
    
    try:
        # Train-test split - stratify problemini çöz
        test_size = min(0.3, max(0.1, (len(X) - 5) / len(X)))  # Adaptif test boyutu
        
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y
            )
        except ValueError:  # Stratify başarısız olursa
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )
        
        print(f"Train/Test split: {len(X_train)}/{len(X_test)}")
        
        results = {}
        
        # 1. Logistic Regression (daha toleranslı)
        try:
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # NaN kontrolü
            X_train_scaled = np.nan_to_num(X_train_scaled)
            X_test_scaled = np.nan_to_num(X_test_scaled)
            
            lr_model = LogisticRegression(random_state=42, max_iter=1000, solver='liblinear')
            lr_model.fit(X_train_scaled, y_train)
            lr_pred = lr_model.predict(X_test_scaled)
            lr_proba = lr_model.predict_proba(X_test_scaled)
            
            results['logistic_regression'] = {
                'name': 'Logistic Regression',
                'accuracy': accuracy_score(y_test, lr_pred),
                'predictions': lr_pred,
                'probabilities': lr_proba,
                'classification_report': classification_report(y_test, lr_pred, output_dict=True, zero_division=0)
            }
            print("Logistic Regression başarılı")
            
        except Exception as e:
            print(f"Logistic Regression hatası: {e}")
            results['logistic_regression'] = {
                'name': 'Logistic Regression',
                'accuracy': 0,
                'error': str(e)
            }
        
        # 2. Random Forest (daha sağlam)
        try:
            rf_model = RandomForestClassifier(
                n_estimators=50,  # Daha az ağaç
                random_state=42,
                min_samples_split=5,  # Daha esnek
                min_samples_leaf=2
            )
            rf_model.fit(X_train, y_train)
            rf_pred = rf_model.predict(X_test)
            rf_proba = rf_model.predict_proba(X_test)
            
            results['random_forest'] = {
                'name': 'Random Forest',
                'accuracy': accuracy_score(y_test, rf_pred),
                'predictions': rf_pred,
                'probabilities': rf_proba,
                'feature_importance': dict(zip(available_features, rf_model.feature_importances_)),
                'classification_report': classification_report(y_test, rf_pred, output_dict=True, zero_division=0)
            }
            print("Random Forest başarılı")
            
        except Exception as e:
            print(f"Random Forest hatası: {e}")
            results['random_forest'] = {
                'name': 'Random Forest',
                'accuracy': 0,
                'error': str(e)
            }
        
        # En iyi modeli belirle
        best_accuracy = 0
        best_model_key = None
        
        for key, model_data in results.items():
            if 'error' not in model_data and model_data['accuracy'] > best_accuracy:
                best_accuracy = model_data['accuracy']
                best_model_key = key
        
        if best_model_key and best_accuracy > 0:
            print(f"En iyi model: {best_model_key} (accuracy: {best_accuracy:.3f})")
            
            # Gelecek tahmin
            try:
                latest_data = df.tail(1)
                if not latest_data.empty:
                    latest_features = latest_data[available_features].fillna(0)
                    
                    if best_model_key == 'random_forest' and 'error' not in results['random_forest']:
                        future_prediction = rf_model.predict(latest_features)[0]
                        future_confidence = max(rf_model.predict_proba(latest_features)[0]) * 100
                    elif best_model_key == 'logistic_regression' and 'error' not in results['logistic_regression']:
                        latest_scaled = scaler.transform(latest_features)
                        latest_scaled = np.nan_to_num(latest_scaled)
                        future_prediction = lr_model.predict(latest_scaled)[0]
                        future_confidence = max(lr_model.predict_proba(latest_scaled)[0]) * 100
                    else:
                        future_prediction = 'dengede'
                        future_confidence = 50.0
                    
                    results['future_prediction'] = {
                        'predicted_direction': future_prediction,
                        'confidence': future_confidence,
                        'model_used': best_model_key
                    }
                    
            except Exception as e:
                print(f"Gelecek tahmin hatası: {e}")
        
        return results
        
    except Exception as e:
        return {'error': f'Model eğitimi genel hatası: {str(e)}'}

def create_energy_market_chart(df):
    """Enerji piyasası grafiği oluştur"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # PTF vs SMF
    axes[0,0].plot(df.index, df['ptf'], label='PTF', alpha=0.7)
    axes[0,0].plot(df.index, df['smf'], label='SMF', alpha=0.7)
    axes[0,0].set_title('PTF vs SMF Karşılaştırması')
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)
    
    # SMF Yön dağılımı
    smf_counts = df['smf_direction'].value_counts()
    axes[0,1].pie(smf_counts.values, labels=smf_counts.index, autopct='%1.1f%%')
    axes[0,1].set_title('SMF Yön Dağılımı')
    
    # Saatlik ortalama fiyatlar
    df['hour_only'] = pd.to_datetime(df['hour'], format='%H:%M:%S').dt.hour
    hourly_avg = df.groupby('hour_only')[['ptf', 'smf']].mean()
    axes[1,0].plot(hourly_avg.index, hourly_avg['ptf'], marker='o', label='PTF')
    axes[1,0].plot(hourly_avg.index, hourly_avg['smf'], marker='s', label='SMF')
    axes[1,0].set_title('Saatlik Ortalama Fiyatlar')
    axes[1,0].set_xlabel('Saat')
    axes[1,0].legend()
    axes[1,0].grid(True, alpha=0.3)
    
    # PTF-SMF farkı
    df['price_diff'] = df['ptf'] - df['smf']
    axes[1,1].hist(df['price_diff'], bins=30, alpha=0.7)
    axes[1,1].set_title('PTF-SMF Fark Dağılımı')
    axes[1,1].set_xlabel('PTF - SMF (TL/MWh)')
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Grafiği base64 formatına çevir
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return chart_data

def data_analysis(request):
    """Veri analizi görünümü"""
    data = ForecastData.objects.filter(actual_value__isnull=False).order_by('date')
    
    if not data.exists():
        messages.warning(request, 'Analiz için veri bulunamadı. Lütfen önce Excel dosyası yükleyin.')
        return redirect('upload_excel')
    
    # Veri istatistikleri
    df = pd.DataFrame(list(data.values('date', 'actual_value')))
    
    stats = {
        'count': len(df),
        'mean': df['actual_value'].mean(),
        'std': df['actual_value'].std(),
        'min': df['actual_value'].min(),
        'max': df['actual_value'].max(),
        'first_date': df['date'].min(),
        'last_date': df['date'].max(),
    }
    
    # Grafik oluştur
    chart_data = create_data_chart(df)
    
    # AI analizi yap (geçici olarak devre dışı)
    ai_analysis = {'status': 'disabled', 'analysis': 'AI servisi geçici olarak devre dışı'}
    
    # AI analizini kaydet
    if ai_analysis['status'] == 'success':
        AIAnalysis.objects.create(
            analysis_type='data_trends',
            content=ai_analysis['analysis'],
            status=ai_analysis['status']
        )
    
    context = {
        'data': data,
        'stats': stats,
        'chart_data': chart_data,
        'ai_analysis': ai_analysis,
    }
    return render(request, 'data_analysis.html', context)

def create_data_chart(df):
    """Veri grafiği oluştur"""
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['actual_value'], marker='o', linewidth=2)
    plt.title('Zaman Serisi Verileri')
    plt.xlabel('Tarih')
    plt.ylabel('Değer')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Grafiği base64 formatına çevir
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return chart_data

def forecast_models(request):
    """Tahmin modelleri görünümü"""
    data = ForecastData.objects.filter(actual_value__isnull=False).order_by('date')
    
    if len(data) < 10:
        messages.warning(request, 'Tahmin modeli oluşturmak için en az 10 veri noktası gerekli.')
        return redirect('data_analysis')
    
    # Modelleri çalıştır
    results = run_forecast_models(data)
    
    # AI ile model performansını değerlendir (geçici olarak devre dışı)
    ai_evaluation = {'status': 'disabled', 'evaluation': 'AI servisi geçici olarak devre dışı'}
    ai_insights = {'status': 'disabled', 'insights': 'AI servisi geçici olarak devre dışı'}
    
    context = {
        'results': results,
        'ai_evaluation': ai_evaluation,
        'ai_insights': ai_insights,
    }
    return render(request, 'forecast_models.html', context)

def ai_analysis_view(request):
    """AI analiz sonuçları görünümü"""
    analyses = AIAnalysis.objects.all()[:20]
    
    context = {
        'analyses': analyses,
    }
    return render(request, 'ai_analysis.html', context)

@csrf_exempt
def generate_ai_insight(request):
    """Yeni AI öngörü oluştur"""
    if request.method == 'POST':
        try:
            data = ForecastData.objects.filter(actual_value__isnull=False).order_by('-date')[:50]
            
            if not data.exists():
                return JsonResponse({'error': 'Analiz için veri bulunamadı'}, status=400)
            
            # AI servisi geçici olarak devre dışı
            analysis = {'status': 'disabled', 'analysis': 'AI servisi geçici olarak devre dışı'}
            
            return JsonResponse({
                'success': True,
                'analysis': analysis['analysis'],
                'id': 1
            })
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_forecast(request):
    """API endpoint for forecast data"""
    if request.method == 'GET':
        data = ForecastData.objects.all()[:100]
        forecast_data = []
        
        for item in data:
            forecast_data.append({
                'date': item.date.strftime('%Y-%m-%d'),
                'actual': item.actual_value,
                'predicted': item.predicted_value,
                'error': item.error,
            })
        
        return JsonResponse({'data': forecast_data})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def run_forecast_models(data):
    """Tahmin modellerini çalıştır"""
    df = pd.DataFrame(list(data.values('date', 'actual_value')))
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Veriyi hazırla
    df['days'] = (df['date'] - df['date'].min()).dt.days
    X = df['days'].values.reshape(-1, 1)
    y = df['actual_value'].values
    
    # Eğitim/test ayrımı
    split_idx = int(len(X) * 0.8)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    results = {}
    
    # Linear Regression
    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)
    linear_pred = linear_model.predict(X_test)
    
    results['linear'] = {
        'name': 'Linear Regression',
        'predictions': linear_pred,
        'mae': mean_absolute_error(y_test, linear_pred),
        'mse': mean_squared_error(y_test, linear_pred),
        'rmse': np.sqrt(mean_squared_error(y_test, linear_pred)),
        'r2': r2_score(y_test, linear_pred),
    }
    
    # Polynomial Regression
    poly_features = PolynomialFeatures(degree=2)
    X_train_poly = poly_features.fit_transform(X_train)
    X_test_poly = poly_features.transform(X_test)
    
    poly_model = LinearRegression()
    poly_model.fit(X_train_poly, y_train)
    poly_pred = poly_model.predict(X_test_poly)
    
    results['polynomial'] = {
        'name': 'Polynomial Regression',
        'predictions': poly_pred,
        'mae': mean_absolute_error(y_test, poly_pred),
        'mse': mean_squared_error(y_test, poly_pred),
        'rmse': np.sqrt(mean_squared_error(y_test, poly_pred)),
        'r2': r2_score(y_test, poly_pred),
    }
    
    return results