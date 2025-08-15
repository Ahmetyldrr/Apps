import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError # MSE kaybını import edin

# Kaydedilen dosyaların yolları (masaüstünüzdeki yollara göre güncelleyin)
model_load_path = 'lstm_model.h5' # Model dosyasının yolu
scaler_load_path = 'scaler_y.pkl' # Scaler dosyasının yolu

# Modeli yükle
try:
    # custom_objects={} içine özel katmanları, fonksiyonları, metrikleri ekleyin
    custom_objects = {'mse': MeanSquaredError()} # MSE kaybını belirtiyoruz
    loaded_model = load_model(model_load_path, custom_objects=custom_objects)
    print(f"Model başarıyla yüklendi: {model_load_path}")
except Exception as e:
    print(f"Model yüklenirken bir hata oluştu: {e}")
    loaded_model = None # Hata durumunda loaded_model'ı None olarak ayarla

# Scaler'ı yükle
try:
    loaded_scaler_y = joblib.load(scaler_load_path)
    print(f"Scaler başarıyla yüklendi: {scaler_load_path}")
except Exception as e:
    print(f"Scaler yüklenirken bir hata oluştu: {e}")
    loaded_scaler_y = None # Hata durumunda loaded_scaler_y'yi None olarak ayarla


print("\nYüklenen modelin özeti:")
if loaded_model:
    loaded_model.summary()
else:
    print("Model yüklenemedi, özet gösterilemiyor.")
    


window_size=24
excel_file_path = 'data.xlsx' # Masaüstünüzdeki yol
df_input_data = pd.read_excel(excel_file_path)
df_long = pd.melt(df_input_data, value_vars=df_input_data.columns, var_name="date", value_name="data")["data"]
df_final = pd.DataFrame(df_long)
df_final.columns = ["data"]
raw_input_data = df_final['data'].values[:-window_size] # Son 72 saat, numpy array
    
    
scaled_input_data = loaded_scaler_y.transform(raw_input_data.reshape(-1, 1)) # Scaler 2D input bekler
X_input_for_prediction = scaled_input_data[np.newaxis, ...] # veya scaled_input_data.reshape(1, window_size, 1)
scaled_prediction = loaded_model.predict(X_input_for_prediction) # Çıktı (1, 24) şeklinde olacak
raw_prediction = loaded_scaler_y.inverse_transform(scaled_prediction) # Çıktı (1, 24) şeklinde olacak
final_prediction = raw_prediction.flatten() # İsterseniz 1D diziye çevirebilirsiniz (24)
df_result = pd.DataFrame()
df_result["Tahmin"] = final_prediction
raw_predict_data = df_final['data'].values[-window_size:] # Son 72 saat, numpy array
df_result["gerçek"]=raw_predict_data
df_result["Fark"] = df_result["Tahmin"]-df_result["gerçek"]

