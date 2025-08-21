import openai
import json
import time
from typing import Dict, List, Optional
from config import OPENAI_API_KEY

class AIQuestionService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.max_retries = 3
        self.retry_delay = 2
    
    def test_connection(self) -> bool:
        """API bağlantısını test et"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=10
            )
            return True
        except Exception as e:
            print(f"API bağlantı testi başarısız: {e}")
            return False
    
    def generate_question(self, topic: str, level: str) -> Optional[Dict]:
        """
        Belirtilen konu ve seviyeye göre çoktan seçmeli soru üret
        """
        if level == "Basit":
            level_desc = "lise düzeyinde temel"
        elif level == "Orta":
            level_desc = "üniversite düzeyinde orta seviye"
        else:  # Zor
            level_desc = "uzman düzeyinde ileri seviye"
        
        prompt = f"""
        {topic} konusunda {level_desc} bir çoktan seçmeli soru oluştur.
        
        Soru formatı şu şekilde olmalı:
        - Açık ve net bir soru
        - 4 şık (A, B, C, D)
        - Sadece bir doğru cevap
        - Diğer şıklar mantıklı ama yanlış olmalı
        
        Cevabı JSON formatında ver:
        {{
            "question": "Soru metni",
            "options": {{
                "A": "Şık A",
                "B": "Şık B", 
                "C": "Şık C",
                "D": "Şık D"
            }},
            "correct_answer": "A",
            "explanation": "Doğru cevabın açıklaması"
        }}
        
        Sadece JSON formatında cevap ver, başka metin ekleme.
        """
        
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system", 
                            "content": "Sen eğitim alanında uzman bir soru hazırlayıcısısın. Sadece JSON formatında cevap verirsin."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                
                content = response.choices[0].message.content.strip()
                
                # JSON parse etmeye çalış
                try:
                    # Bazen ```json ile wrap edilebilir, temizle
                    if content.startswith("```json"):
                        content = content[7:]
                    if content.endswith("```"):
                        content = content[:-3]
                    
                    question_data = json.loads(content)
                    
                    # Gerekli alanları kontrol et
                    required_fields = ["question", "options", "correct_answer", "explanation"]
                    if all(field in question_data for field in required_fields):
                        if all(option in question_data["options"] for option in ["A", "B", "C", "D"]):
                            return question_data
                    
                except json.JSONDecodeError as e:
                    print(f"JSON parse hatası (attempt {attempt + 1}): {e}")
                    print(f"Response content: {content}")
                
            except openai.APIConnectionError as e:
                print(f"API bağlantı hatası (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    return self._get_fallback_question(topic, level)
                    
            except openai.RateLimitError as e:
                print(f"Rate limit hatası (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * 2)  # Rate limit için daha uzun bekle
                    continue
                else:
                    return self._get_fallback_question(topic, level)
                    
            except openai.APIError as e:
                print(f"API hatası (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    return self._get_fallback_question(topic, level)
                    
            except Exception as e:
                print(f"Beklenmeyen hata (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    return self._get_fallback_question(topic, level)
        
        return self._get_fallback_question(topic, level)
    
    def _get_fallback_question(self, topic: str, level: str) -> Dict:
        """API bağlantısı olmadığında kullanılacak yedek sorular"""
        fallback_questions = {
            "Matematik": {
                "Basit": {
                    "question": "2 + 3 × 4 işleminin sonucu kaçtır?",
                    "options": {
                        "A": "20",
                        "B": "14", 
                        "C": "10",
                        "D": "24"
                    },
                    "correct_answer": "B",
                    "explanation": "Çarpma işlemi toplama işleminden önce yapılır: 3 × 4 = 12, sonra 2 + 12 = 14"
                },
                "Orta": {
                    "question": "f(x) = 2x + 1 fonksiyonunun tersi hangisidir?",
                    "options": {
                        "A": "f⁻¹(x) = (x-1)/2",
                        "B": "f⁻¹(x) = 2x-1",
                        "C": "f⁻¹(x) = x/2+1", 
                        "D": "f⁻¹(x) = 2/(x+1)"
                    },
                    "correct_answer": "A",
                    "explanation": "y = 2x + 1, x = (y-1)/2 olduğundan f⁻¹(x) = (x-1)/2"
                },
                "Zor": {
                    "question": "∫(x²+1)/(x³+3x+2) dx integralinin çözümü için hangi yöntem kullanılır?",
                    "options": {
                        "A": "Kısmi kesirler",
                        "B": "Substitution",
                        "C": "Parçalı integral",
                        "D": "Trigonometrik substitution"
                    },
                    "correct_answer": "A",
                    "explanation": "Payda çarpanlarına ayrılıp kısmi kesirler yöntemi kullanılır"
                }
            },
            "Fizik": {
                "Basit": {
                    "question": "Işık hızı yaklaşık kaç m/s'dir?",
                    "options": {
                        "A": "3 × 10⁶ m/s",
                        "B": "3 × 10⁸ m/s",
                        "C": "3 × 10¹⁰ m/s",
                        "D": "3 × 10⁴ m/s"
                    },
                    "correct_answer": "B",
                    "explanation": "Işık hızı vakumda yaklaşık 3 × 10⁸ m/s'dir"
                }
            }
        }
        
        # Yedek soru varsa döndür
        if topic in fallback_questions and level in fallback_questions[topic]:
            return fallback_questions[topic][level]
        
        # Genel yedek soru
        return {
            "question": f"{topic} konusunda {level} seviyesinde bir soru (Bağlantı hatası nedeniyle örnek soru)",
            "options": {
                "A": "Seçenek A",
                "B": "Seçenek B", 
                "C": "Seçenek C",
                "D": "Seçenek D"
            },
            "correct_answer": "A",
            "explanation": "Bu örnek bir sorudur. İnternet bağlantınızı kontrol edin."
        }

# Global AI service instance
ai_service = AIQuestionService()
