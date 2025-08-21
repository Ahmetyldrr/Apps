import openai
import json
from config import OPENAI_API_KEY, LEVELS

class QuestionGenerator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    def generate_question(self, topic, level):
        """Belirtilen konu ve seviyede çoktan seçmeli soru üretir"""
        
        system_message = f"""
        Sen bir eğitim uzmanısın ve çoktan seçmeli sorular hazırlıyorsun.
        Konu: {topic}
        Seviye: {level} - {LEVELS[level]}
        
        Sadece JSON formatında bir soru döndür. Format:
        {{
            "question": "Soru metni",
            "options": {{
                "A": "Seçenek A",
                "B": "Seçenek B", 
                "C": "Seçenek C",
                "D": "Seçenek D"
            }},
            "correct_answer": "A/B/C/D"
        }}
        
        Kurallat:
        - Soru açık ve net olmalı
        - 4 seçenek olmalı (A, B, C, D)
        - Sadece bir doğru cevap olmalı
        - Diğer seçenekler mantıklı ama yanlış olmalı
        - Türkçe dilinde olmalı
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"{topic} konusunda {level} seviyesinde bir soru oluştur"}
                ],
                temperature=0.8,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            if content:
                content = content.strip()
                # JSON parsing
                if content.startswith("```json"):
                    content = content[7:-3]
                elif content.startswith("```"):
                    content = content[3:-3]
            else:
                content = "{}"
                
            question_data = json.loads(content)
            return question_data
            
        except Exception as e:
            print(f"Soru üretme hatası: {e}")
            # Fallback soru
            return {
                "question": f"{topic} ile ilgili temel bir soru?",
                "options": {
                    "A": "Seçenek A",
                    "B": "Seçenek B",
                    "C": "Seçenek C", 
                    "D": "Seçenek D"
                },
                "correct_answer": "A"
            }
    
    def check_answer(self, user_answer, correct_answer):
        """Kullanıcı cevabını kontrol eder"""
        return user_answer.upper() == correct_answer.upper()
    
    def get_explanation(self, question_data, user_answer):
        """Cevap açıklaması üretir"""
        try:
            system_message = """
            Sen bir eğitim uzmanısın. Verilen soru ve cevaplara göre kısa bir açıklama yap.
            Doğru cevabı belirt ve neden doğru olduğunu açıkla.
            Maksimum 2-3 cümle ile açıkla.
            """
            
            user_message = f"""
            Soru: {question_data['question']}
            Seçenekler: {question_data['options']}
            Doğru Cevap: {question_data['correct_answer']}
            Kullanıcı Cevabı: {user_answer}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            content = response.choices[0].message.content
            return content.strip() if content else "Açıklama üretilemedi."
            
        except Exception as e:
            print(f"Açıklama üretme hatası: {e}")
            return f"Doğru cevap: {question_data['correct_answer']}"
