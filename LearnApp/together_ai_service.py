import together
import json
import traceback
import ssl
import urllib3
import os
from config import TOGETHER_API_KEY, MODEL_NAME

# SSL sertifika doğrulamasını devre dışı bırak
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxy/SSL ayarları
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['CURL_CA_BUNDLE'] = ''

class TogetherAIService:
    def __init__(self):
        together.api_key = TOGETHER_API_KEY
        self.model = MODEL_NAME
    
    def ask_together(self, content):
        """Together AI ile soru sorma fonksiyonu"""
        try:
            response = together.Complete.create(
                prompt=content,
                model=self.model,
                max_tokens=1000,
                temperature=0.91,
                top_p=0.91
            )
            
            # Response formatını kontrol et
            print(f"Response type: {type(response)}")
            print(f"Response: {response}")
            
            # Farklı response formatlarını dene
            if isinstance(response, dict):
                if 'output' in response and 'choices' in response['output']:
                    return response['output']['choices'][0]['text']
                elif 'choices' in response:
                    return response['choices'][0]['text']
                elif 'text' in response:
                    return response['text']
            elif isinstance(response, str):
                return response
            else:
                return str(response)
                
        except Exception as e:
            print(f"Together AI hatası: {e}")
            traceback.print_exc()
            return None
    
    def generate_question(self, topic, level, question_count=1):
        """Belirtilen konu ve seviyede çoktan seçmeli soru üretir"""
        
        level_descriptions = {
            "Basit": "Lise düzeyi temel bilgiler",
            "Orta": "Üniversite düzeyi orta seviye bilgiler", 
            "Zor": "Uzman düzeyi ileri seviye bilgiler"
        }
        
        prompt = f"""
Türkçe olarak {topic} konusunda {level_descriptions[level]} seviyesinde {question_count} adet çoktan seçmeli soru üret.

Her soru için:
- Soru metni
- 4 adet şık (A, B, C, D)
- Doğru cevap (A, B, C, D harfi)
- Kısa açıklama

JSON formatında döndür:
{{
    "questions": [
        {{
            "question": "Soru metni burada",
            "options": {{
                "A": "İlk şık",
                "B": "İkinci şık", 
                "C": "Üçüncü şık",
                "D": "Dördüncü şık"
            }},
            "correct_answer": "A",
            "explanation": "Doğru cevabın açıklaması"
        }}
    ]
}}

Konu: {topic}
Seviye: {level}
Soru Sayısı: {question_count}
"""

        try:
            response = self.ask_together(prompt)
            if response:
                # JSON parse etmeye çalış
                try:
                    # Eğer response'da ```json başlığı varsa temizle
                    if "```json" in response:
                        response = response.split("```json")[1].split("```")[0].strip()
                    elif "```" in response:
                        response = response.split("```")[1].strip()
                    
                    questions_data = json.loads(response)
                    return questions_data.get("questions", [])
                except json.JSONDecodeError:
                    print("JSON parse hatası, ham response:")
                    print(response)
                    return self._create_fallback_question(topic, level)
            else:
                return self._create_fallback_question(topic, level)
                
        except Exception as e:
            print(f"Soru üretme hatası: {e}")
            traceback.print_exc()
            return self._create_fallback_question(topic, level)
    
    def _create_fallback_question(self, topic, level):
        """API hatası durumunda kullanılacak örnek soru"""
        fallback_questions = {
            "Matematik": {
                "Basit": {
                    "question": "2 + 2 işleminin sonucu nedir?",
                    "options": {"A": "3", "B": "4", "C": "5", "D": "6"},
                    "correct_answer": "B",
                    "explanation": "2 + 2 = 4'tür, temel toplama işlemi."
                }
            }
        }
        
        default_question = {
            "question": f"{topic} konusunda {level} seviyede örnek soru",
            "options": {
                "A": "Seçenek A",
                "B": "Seçenek B", 
                "C": "Seçenek C",
                "D": "Seçenek D"
            },
            "correct_answer": "A",
            "explanation": "Bu örnek bir açıklamadır."
        }
        
        return [fallback_questions.get(topic, {}).get(level, default_question)]
    
    def test_connection(self):
        """API bağlantısını test eder"""
        try:
            response = together.Complete.create(
                prompt="Test",
                model=self.model,
                max_tokens=10,
                temperature=0.7
            )
            return response is not None
        except Exception as e:
            print(f"Bağlantı test hatası: {e}")
            return False

# Global instance
together_ai = TogetherAIService()
