import requests
import json
import ssl
import urllib3
from config import TOGETHER_API_KEY

# SSL uyarılarını kapat
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ManualTogetherAIService:
    def __init__(self):
        self.api_key = TOGETHER_API_KEY
        self.base_url = "https://api.together.xyz/v1/completions"
        
        # SSL doğrulamasını bypass et
        self.session = requests.Session()
        self.session.verify = False
        
        # SSL context'i ayarla
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
    
    def ask_together(self, prompt, max_tokens=1000):
        """Manuel Together AI API çağrısı"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 0.9,
            "stop": None
        }
        
        try:
            response = self.session.post(
                self.base_url,
                headers=headers,
                json=data,
                verify=False,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['text']
            else:
                print(f"API Hatası: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Request hatası: {e}")
            return None
    
    def generate_question(self, topic, level, question_count=1):
        """Belirtilen konu ve seviyede çoktan seçmeli soru üretir"""
        
        level_descriptions = {
            "Basit": "Lise düzeyi temel bilgiler",
            "Orta": "Üniversite düzeyi orta seviye bilgiler", 
            "Zor": "Uzman düzeyi ileri seviye bilgiler"
        }
        
        prompt = f"""Türkçe olarak {topic} konusunda {level_descriptions[level]} seviyesinde {question_count} adet çoktan seçmeli soru üret.

Her soru için JSON formatında döndür:
{{
    "soru": "Soru metni burada",
    "secenekler": {{
        "A": "İlk şık",
        "B": "İkinci şık", 
        "C": "Üçüncü şık",
        "D": "Dördüncü şık"
    }},
    "dogru_cevap": "A",
    "aciklama": "Doğru cevabın açıklaması"
}}

Sadece JSON formatında cevap ver, başka açıklama ekleme.
Konu: {topic}
Seviye: {level}"""

        try:
            response = self.ask_together(prompt, max_tokens=800)
            if response:
                # Response'u temizle
                response = response.strip()
                
                # JSON parse etmeye çalış
                try:
                    # Eğer response'da gereksiz metin varsa temizle
                    if '{' in response:
                        start_index = response.find('{')
                        end_index = response.rfind('}') + 1
                        json_str = response[start_index:end_index]
                        
                        question_data = json.loads(json_str)
                        
                        # Formatı standardize et
                        standardized_question = {
                            "question": question_data.get("soru", ""),
                            "options": {
                                "A": question_data.get("secenekler", {}).get("A", ""),
                                "B": question_data.get("secenekler", {}).get("B", ""),
                                "C": question_data.get("secenekler", {}).get("C", ""),
                                "D": question_data.get("secenekler", {}).get("D", "")
                            },
                            "correct_answer": question_data.get("dogru_cevap", "A"),
                            "explanation": question_data.get("aciklama", "")
                        }
                        
                        return [standardized_question]
                        
                except json.JSONDecodeError as e:
                    print(f"JSON parse hatası: {e}")
                    print(f"Response: {response}")
                    return self._create_fallback_question(topic, level)
            else:
                return self._create_fallback_question(topic, level)
                
        except Exception as e:
            print(f"Soru üretme hatası: {e}")
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
                    "question": "f(x) = x² + 2x + 1 fonksiyonunun türevi nedir?",
                    "options": {"A": "2x + 2", "B": "x² + 2", "C": "2x + 1", "D": "x + 2"},
                    "correct_answer": "A",
                    "explanation": "Polinom türev kuralına göre f'(x) = 2x + 2'dir."
                },
                "Zor": {
                    "question": "∫(sin x)/(cos² x) dx integralinin sonucu nedir?",
                    "options": {"A": "tan x + C", "B": "sec x + C", "C": "-cot x + C", "D": "csc x + C"},
                    "correct_answer": "A",
                    "explanation": "u = cos x, du = -sin x dx dönüşümü ile integral tan x + C olur."
                }
            },
            "Fizik": {
                "Basit": {
                    "question": "Hız birimi nedir?",
                    "options": {"A": "m/s", "B": "m/s²", "C": "kg", "D": "N"},
                    "correct_answer": "A",
                    "explanation": "Hız = yol/zaman olduğu için birimi m/s'dir."
                }
            }
        }
        
        topic_questions = fallback_questions.get(topic, {})
        level_question = topic_questions.get(level)
        
        if level_question:
            return [level_question]
        else:
            return [{
                "question": f"{topic} konusunda {level} seviyede örnek soru",
                "options": {
                    "A": "Seçenek A",
                    "B": "Seçenek B", 
                    "C": "Seçenek C",
                    "D": "Seçenek D"
                },
                "correct_answer": "A",
                "explanation": "Bu örnek bir açıklamadır."
            }]
    
    def test_connection(self):
        """API bağlantısını test eder"""
        try:
            response = self.ask_together("Test", max_tokens=10)
            return response is not None
        except Exception as e:
            print(f"Bağlantı test hatası: {e}")
            return False

# Global instance
manual_together_ai = ManualTogetherAIService()
