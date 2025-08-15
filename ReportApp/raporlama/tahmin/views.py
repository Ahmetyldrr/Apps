import numpy as np
import pandas as pd
import joblib
import json
import os
import re
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError

# Global değişkenler - modeli bir kez yükleyip cache'te tutalım
loaded_model = None
loaded_scaler_y = None
window_size = 72  # Model için gereken veri sayısı (72 saatlik pencere)
prediction_window = 24  # Tahmin edilecek saat sayısı
total_required_data = 96  # Toplam gereken veri (72 + 24)

def clean_number_format(value):
    """Türkçe sayı formatını temizler (4.600 -> 4600, 4,5 -> 4.5)"""
    if isinstance(value, (int, float)):
        return float(value)
    
    if isinstance(value, str):
        # Boşlukları temizle
        clean_val = value.strip()
        
        # Hem nokta hem virgül varsa
        if '.' in clean_val and ',' in clean_val:
            # Nokta binlik ayırıcı, virgül ondalık
            clean_val = clean_val.replace('.', '').replace(',', '.')
        elif '.' in clean_val and ',' not in clean_val:
            # Sadece nokta var - binlik mi ondalık mı kontrol et
            parts = clean_val.split('.')
            if len(parts) == 2 and len(parts[1]) == 3:
                # 4.600 formatı - binlik ayırıcı
                clean_val = clean_val.replace('.', '')
            # Aksi halde ondalık nokta olarak bırak
        elif ',' in clean_val:
            # Sadece virgül var - ondalık ayırıcı olarak nokta yap
            clean_val = clean_val.replace(',', '.')
        
        try:
            return float(clean_val)
        except ValueError:
            return None
    
    return None

def load_ml_models():
    """Makine öğrenmesi modellerini yükler"""
    global loaded_model, loaded_scaler_y
    
    if loaded_model is None or loaded_scaler_y is None:
        try:
            # Model yolları
            model_path = os.path.join(settings.BASE_DIR, 'lstm_model.h5')
            scaler_path = os.path.join(settings.BASE_DIR, 'scaler_y.pkl')
            
            # Modeli yükle
            custom_objects = {'mse': MeanSquaredError()}
            loaded_model = load_model(model_path, custom_objects=custom_objects)
            
            # Scaler'ı yükle
            loaded_scaler_y = joblib.load(scaler_path)
            
            print("Model ve scaler başarıyla yüklendi!")
            
        except Exception as e:
            print(f"Model yüklenirken hata oluştu: {e}")
            loaded_model = None
            loaded_scaler_y = None

def index(request):
    """Ana sayfa"""
    return render(request, 'tahmin/index.html')

@csrf_exempt
def predict(request):
    """Tahmin API endpoint'i"""
    if request.method == 'POST':
        try:
            # Modelleri yükle
            
            load_ml_models()
            data = json.loads(request.body)
            input_data = data.get('data', [])

            print("Gelen input_data:", input_data)
          
            df_input = pd.DataFrame(np.array(input_data).reshape(24, 4), columns=["input1", "input2", "input3", "actual"])
            print("Gelen DataFrame:")
            print(df_input)       
           
            # Training data: input1, input2, input3 sütunlarını satır bazlı ardışık ekle
            training_data = df_input[["input1", "input2", "input3",]].values.flatten(order='C')
            print("Training data:", training_data)

            # Actual data
            actual_data = df_input["actual"].values.tolist()

            
            # Model için veriyi hazırla - orijinal savemodel.py'deki gibi
            raw_input_data = np.array(training_data, dtype=float)
            
            # Veriyi ölçekle (72,) -> (72, 1) -> scaled
            scaled_input_data = loaded_scaler_y.transform(raw_input_data.reshape(-1, 1))
            
            # Model input formatına çevir: (1, 72, 1)
            X_input = scaled_input_data[np.newaxis, ...]  # (72, 1) -> (1, 72, 1)
            print(f"Model input boyutu: {X_input.shape}")  # (1, 72, 1) olmalı
            
            # Tahmin yap
            scaled_prediction = loaded_model.predict(X_input)
            
            # Ölçeği geri çevir
            raw_prediction = loaded_scaler_y.inverse_transform(scaled_prediction)
            
            # Sonuçları hazırla
            predictions = raw_prediction.flatten().tolist()
            
            # Grafik için zaman serileri oluştur
            time_labels = [f"Saat {i+1}" for i in range(prediction_window)]
            
            return JsonResponse({
                'success': True,
                'predictions': predictions,
                'actual': actual_data,
                'time_labels': time_labels,
                'training_data_count': len(training_data),
                'actual_data_count': len(actual_data)
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Sadece POST metodu desteklenir'}, status=405)
