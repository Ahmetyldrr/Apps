import openai
import os
from django.conf import settings
import pandas as pd
import json
from typing import Dict, List, Any

class AIAnalysisService:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def analyze_data_trends(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Veri trendlerini AI ile analiz et"""
        try:
            # Veri özetini hazırla
            data_summary = self._prepare_data_summary(data)
            
            prompt = f"""
            Aşağıdaki zaman serisi verilerini analiz edin ve Türkçe olarak detaylı bir rapor yazın:
            
            Veri Özeti:
            {data_summary}
            
            Lütfen şunları analiz edin:
            1. Genel trend (yükseliş, düşüş, sabit)
            2. Mevsimsellik varsa belirtin
            3. Anomaliler veya dikkat çekici noktalar
            4. Gelecek için tahminler ve öneriler
            5. Risk faktörleri
            
            Analizi iş dünyasından anlayan birisi için yazın.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sen bir veri analisti ve iş zekası uzmanısın. Zaman serisi verilerini analiz etmek ve iş öngörüleri sağlamakta uzmanlaşmışsın."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return {
                'analysis': response.choices[0].message.content,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'analysis': f'AI analizi sırasında hata oluştu: {str(e)}',
                'status': 'error'
            }
    
    def evaluate_model_performance(self, model_results: Dict) -> Dict[str, Any]:
        """Model performanslarını AI ile değerlendir"""
        try:
            prompt = f"""
            Aşağıdaki tahmin modeli sonuçlarını analiz edin ve Türkçe olarak değerlendirin:
            
            Model Sonuçları:
            {json.dumps(model_results, indent=2)}
            
            Lütfen şunları değerlendirin:
            1. Hangi model en iyi performans gösteriyor?
            2. Her modelin güçlü ve zayıf yönleri nelerdir?
            3. Hangi durumda hangi modeli kullanmak daha uygun?
            4. Model sonuçlarından çıkarılabilecek iş öngörüleri
            5. Modellerin güvenilirlik seviyeleri
            
            Teknik olmayan kişilerin de anlayabileceği şekilde açıklayın.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sen bir makine öğrenmesi uzmanı ve iş danışmanısın. Karmaşık model sonuçlarını basit ve anlaşılır şekilde açıklıyorsun."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,
                temperature=0.7
            )
            
            return {
                'evaluation': response.choices[0].message.content,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'evaluation': f'AI değerlendirmesi sırasında hata oluştu: {str(e)}',
                'status': 'error'
            }
    
    def generate_forecast_insights(self, forecast_data: List[Dict]) -> Dict[str, Any]:
        """Tahmin sonuçları için AI öngörüleri üret"""
        try:
            # Son 10 tahmini al
            recent_forecasts = forecast_data[:10] if len(forecast_data) > 10 else forecast_data
            
            prompt = f"""
            Aşağıdaki tahmin verilerini analiz edin ve Türkçe olarak iş öngörüleri sağlayın:
            
            Son Tahminler:
            {json.dumps(recent_forecasts, indent=2)}
            
            Lütfen şunları sağlayın:
            1. Tahminlerdeki genel eğilim nedir?
            2. Dikkat edilmesi gereken riskler
            3. Fırsatlar ve potansiyel büyüme alanları
            4. Operasyonel öneriler
            5. Kısa ve uzun vadeli stratejik öneriler
            
            CEO ve üst yönetim için hazırlanmış bir özet gibi yazın.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sen bir stratejik iş danışmanısın. Veri analizi sonuçlarından iş stratejileri ve operasyonel öneriler çıkarıyorsun."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return {
                'insights': response.choices[0].message.content,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'insights': f'AI öngörü analizi sırasında hata oluştu: {str(e)}',
                'status': 'error'
            }
    
    def _prepare_data_summary(self, data: pd.DataFrame) -> str:
        """Veri özetini hazırla"""
        summary = {
            'toplam_kayit': len(data),
            'tarih_araligi': f"{data['date'].min()} - {data['date'].max()}",
            'ortalama_deger': round(data['actual_value'].mean(), 2),
            'min_deger': round(data['actual_value'].min(), 2),
            'max_deger': round(data['actual_value'].max(), 2),
            'standart_sapma': round(data['actual_value'].std(), 2),
            'son_5_deger': data['actual_value'].tail(5).tolist()
        }
        return json.dumps(summary, indent=2, ensure_ascii=False)
