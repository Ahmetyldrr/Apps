import sqlite3
import json
import random
from typing import Dict, List, Optional

class OfflineQuestionService:
    def __init__(self):
        self.questions_db = self._create_sample_questions()
    
    def _create_sample_questions(self) -> Dict:
        """Örnek soruları oluştur"""
        return {
            "Matematik": {
                "Basit": [
                    {
                        "question": "2 + 3 × 4 işleminin sonucu nedir?",
                        "options": {"A": "20", "B": "14", "C": "10", "D": "24"},
                        "correct": "B",
                        "explanation": "Çarpma önceliklidir: 3 × 4 = 12, sonra 2 + 12 = 14"
                    },
                    {
                        "question": "Bir dik üçgenin hipotenüsü 5 cm, bir dik kenarı 3 cm ise diğer dik kenar kaç cm'dir?",
                        "options": {"A": "4 cm", "B": "8 cm", "C": "2 cm", "D": "6 cm"},
                        "correct": "A",
                        "explanation": "Pisagor teoremi: a² + b² = c² → 3² + b² = 5² → b = 4"
                    }
                ],
                "Orta": [
                    {
                        "question": "f(x) = x² - 4x + 3 fonksiyonunun kökleri nelerdir?",
                        "options": {"A": "1 ve 3", "B": "2 ve 4", "C": "0 ve 4", "D": "-1 ve -3"},
                        "correct": "A",
                        "explanation": "x² - 4x + 3 = 0 → (x-1)(x-3) = 0 → x = 1 veya x = 3"
                    }
                ],
                "Zor": [
                    {
                        "question": "∫(x²+1)/(x³+3x+1) dx integralinin çözümü hangi yöntemle bulunur?",
                        "options": {"A": "Parçalı integral", "B": "Yerine koyma", "C": "Kısmi kesirler", "D": "Trigonometrik ikame"},
                        "correct": "C",
                        "explanation": "Payda çarpanlarına ayrılıp kısmi kesirler yöntemi kullanılır"
                    }
                ]
            },
            "Fizik": {
                "Basit": [
                    {
                        "question": "Işık hızı yaklaşık olarak nedir?",
                        "options": {"A": "300.000 km/s", "B": "3.000 km/s", "C": "30.000 km/s", "D": "3.000.000 km/s"},
                        "correct": "A",
                        "explanation": "Işık hızı vakumda yaklaşık 300.000 km/s (3×10⁸ m/s) dir"
                    }
                ],
                "Orta": [
                    {
                        "question": "F = ma formülünde m kütlesi 2 kg, ivme 5 m/s² ise kuvvet nedir?",
                        "options": {"A": "10 N", "B": "7 N", "C": "3 N", "D": "2.5 N"},
                        "correct": "A",
                        "explanation": "F = ma = 2 kg × 5 m/s² = 10 N"
                    }
                ],
                "Zor": [
                    {
                        "question": "Schrödinger denkleminin zamandan bağımsız hali nedir?",
                        "options": {"A": "Hψ = Eψ", "B": "∇²ψ = 0", "C": "ψ = Ae^(ikx)", "D": "E = mc²"},
                        "correct": "A",
                        "explanation": "Hamiltonian operatörü dalga fonksiyonuna uygulandığında enerji özdeğeri elde edilir"
                    }
                ]
            },
            "Tarih": {
                "Basit": [
                    {
                        "question": "Osmanlı İmparatorluğu hangi yılda kurulmuştur?",
                        "options": {"A": "1299", "B": "1453", "C": "1389", "D": "1326"},
                        "correct": "A",
                        "explanation": "Osmanlı İmparatorluğu 1299 yılında Osman Gazi tarafından kurulmuştur"
                    }
                ],
                "Orta": [
                    {
                        "question": "Birinci Dünya Savaşı hangi yıllar arasında yaşanmıştır?",
                        "options": {"A": "1914-1918", "B": "1939-1945", "C": "1912-1916", "D": "1916-1920"},
                        "correct": "A",
                        "explanation": "Birinci Dünya Savaşı 1914-1918 yılları arasında yaşanmıştır"
                    }
                ],
                "Zor": [
                    {
                        "question": "Tanzimat Fermanı'nın getirdiği en önemli yenilik nedir?",
                        "options": {"A": "Eşitlik ilkesi", "B": "Meclis kurulması", "C": "Anayasa yapılması", "D": "Seçim sistemi"},
                        "correct": "A",
                        "explanation": "Tanzimat Fermanı din ve dil farkı gözetmeksizin eşitlik ilkesini getirmiştir"
                    }
                ]
            }
        }
    
    def get_question(self, topic: str, level: str) -> Optional[Dict]:
        """Belirtilen konu ve seviyeye göre rastgele soru getir"""
        try:
            if topic in self.questions_db and level in self.questions_db[topic]:
                questions = self.questions_db[topic][level]
                if questions:
                    return random.choice(questions)
            return None
        except Exception as e:
            print(f"Soru alma hatası: {e}")
            return None
    
    def add_custom_question(self, topic: str, level: str, question_data: Dict):
        """Özel soru ekle"""
        if topic not in self.questions_db:
            self.questions_db[topic] = {"Basit": [], "Orta": [], "Zor": []}
        if level not in self.questions_db[topic]:
            self.questions_db[topic][level] = []
        
        self.questions_db[topic][level].append(question_data)

# AI ile soru üretmeyi deneyen, başarısız olursa offline sorulara geçen hibrit servis
class HybridQuestionService:
    def __init__(self):
        self.offline_service = OfflineQuestionService()
        self.use_ai = False  # Başlangıçta offline mod
        
        # AI servisi test et
        try:
            from ai_service import AIQuestionService
            self.ai_service = AIQuestionService()
            if self.ai_service.test_connection():
                self.use_ai = True
                print("✅ AI servis aktif")
            else:
                print("⚠️ AI servis kullanılamıyor, offline mod aktif")
        except Exception as e:
            print(f"⚠️ AI servis yüklenemedi: {e}, offline mod aktif")
    
    def generate_question(self, topic: str, level: str) -> Optional[Dict]:
        """Hibrit soru üretimi - önce AI dene, sonra offline"""
        if self.use_ai:
            try:
                question = self.ai_service.generate_question(topic, level)
                if question:
                    return question
                print("AI'dan soru alınamadı, offline sorulara geçiliyor...")
            except Exception as e:
                print(f"AI hata: {e}, offline sorulara geçiliyor...")
                self.use_ai = False
        
        # Offline soru getir
        return self.offline_service.get_question(topic, level)
    
    def get_available_topics(self) -> List[str]:
        """Mevcut konuları listele"""
        return list(self.offline_service.questions_db.keys())
