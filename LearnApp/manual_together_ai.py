import requests
import json
import ssl
import urllib3
import traceback
from config import TOGETHER_API_KEY

# SSL uyarılarını kapat
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ManualTogetherAI:
    def __init__(self):
        self.api_key = TOGETHER_API_KEY
        self.base_url = "https://api.together.xyz"
        
        # SSL session ayarları
        self.session = requests.Session()
        self.session.verify = False  # SSL doğrulamasını kapat
        
    def ask_together(self, prompt, model="mistralai/Mixtral-8x7B-Instruct-v0.1"):
        """Together AI API'sini manuel olarak çağır"""
        url = f"{self.base_url}/api/inference"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "prompt": prompt,
            "max_tokens": 1000,
            "temperature": 0.91,
            "top_p": 0.91
        }
        
        try:
            response = self.session.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                # Response formatını kontrol et ve text'i çıkar
                if 'output' in result and 'choices' in result['output']:
                    return result['output']['choices'][0]['text']
                elif 'choices' in result:
                    return result['choices'][0]['text']
                elif 'text' in result:
                    return result['text']
                else:
                    print(f"Beklenmeyen response formatı: {result}")
                    return str(result)
            else:
                print(f"API Hatası: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Request hatası: {e}")
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
                },
                "Orta": {
                    "question": "log₂(8) değeri nedir?",
                    "options": {"A": "2", "B": "3", "C": "4", "D": "8"},
                    "correct_answer": "B",
                    "explanation": "2³ = 8 olduğundan log₂(8) = 3'tür."
                },
                "Zor": {
                    "question": "∫₀¹ x² dx integralinin değeri nedir?",
                    "options": {"A": "1/2", "B": "1/3", "C": "2/3", "D": "1"},
                    "correct_answer": "B",
                    "explanation": "∫x² dx = x³/3 ve [x³/3]₀¹ = 1/3 - 0 = 1/3"
                }
            },
            "Fizik": {
                "Basit": {
                    "question": "Işığın havadaki hızı yaklaşık kaç m/s'dir?",
                    "options": {"A": "3×10⁶", "B": "3×10⁷", "C": "3×10⁸", "D": "3×10⁹"},
                    "correct_answer": "C",
                    "explanation": "Işığın boşluktaki hızı c = 3×10⁸ m/s'dir."
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
            response = self.ask_together("Test")
            return response is not None
        except Exception as e:
            print(f"Bağlantı test hatası: {e}")
            return False

# Global instance
manual_together_ai = ManualTogetherAI()
