import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from question_service import HybridQuestionService
from config import TOPICS, LEVELS, COLORS

class QuizApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.question_service = HybridQuestionService()
        self.current_question = None
        self.current_player = 1
        self.scores = {"player1": 0, "player2": 0}
        self.players = {"player1": "", "player2": ""}
        self.game_settings = {"topic": "", "level": "", "question_count": 10}
        self.question_counter = 0
        
        self.init_ui()
        self.init_database()
    
    def init_database(self):
        """Veritabanını başlat"""
        try:
            conn = sqlite3.connect('db/quizapp.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT UNIQUE NOT NULL
            )''')
            c.execute('''CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user1_id INTEGER,
                user2_id INTEGER,
                user1_name TEXT,
                user2_name TEXT,
                score1 INTEGER,
                score2 INTEGER,
                topic TEXT,
                level TEXT,
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user1_id) REFERENCES users(id),
                FOREIGN KEY(user2_id) REFERENCES users(id)
            )''')
            conn.commit()
            conn.close()
            print("✅ Veritabanı hazır")
        except Exception as e:
            print(f"❌ Veritabanı hatası: {e}")
    
    def init_ui(self):
        """Arayüzü başlat"""
        self.setWindowTitle("🧠 AI Destekli Soru-Cevap Yarışması")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #f0f0f0; font-family: Arial;")
        
        # Ana widget ve stack
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        
        # Sayfaları oluştur
        self.create_welcome_page()
        self.create_setup_page()
        self.create_game_page()
        self.create_results_page()
    
    def create_welcome_page(self):
        """Hoş geldin sayfası"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        
        # Başlık
        title = QLabel("🧠 AI Destekli Soru-Cevap Yarışması")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #2c3e50; margin: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Açıklama
        desc = QLabel("İki oyuncu karşılıklı yarışarak bilgi seviyelerini test edebilir!")
        desc.setStyleSheet("font-size: 16px; color: #7f8c8d; margin-bottom: 30px;")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)
        
        # Başlat butonu
        start_btn = QPushButton("🚀 Yarışmaya Başla")
        start_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                padding: 15px 30px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        start_btn.clicked.connect(self.show_setup_page)
        layout.addWidget(start_btn)
        
        self.stacked_widget.addWidget(page)
    
    def create_setup_page(self):
        """Oyun kurulumu sayfası"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Başlık
        title = QLabel("⚙️ Oyun Kurulumu")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Oyuncu isimleri
        players_group = QGroupBox("👥 Oyuncular")
        players_group.setStyleSheet("font-size: 16px; font-weight: bold;")
        players_layout = QFormLayout(players_group)
        
        self.player1_input = QLineEdit()
        self.player1_input.setPlaceholderText("1. Oyuncu adı...")
        self.player1_input.setStyleSheet("padding: 10px; font-size: 14px; border: 2px solid #bdc3c7; border-radius: 5px;")
        
        self.player2_input = QLineEdit()
        self.player2_input.setPlaceholderText("2. Oyuncu adı...")
        self.player2_input.setStyleSheet("padding: 10px; font-size: 14px; border: 2px solid #bdc3c7; border-radius: 5px;")
        
        players_layout.addRow("🟡 1. Oyuncu:", self.player1_input)
        players_layout.addRow("🔵 2. Oyuncu:", self.player2_input)
        layout.addWidget(players_group)
        
        # Oyun ayarları
        settings_group = QGroupBox("🎮 Oyun Ayarları")
        settings_group.setStyleSheet("font-size: 16px; font-weight: bold;")
        settings_layout = QFormLayout(settings_group)
        
        # Konu seçimi
        self.topic_combo = QComboBox()
        self.topic_combo.addItems(TOPICS)
        self.topic_combo.setStyleSheet("padding: 8px; font-size: 14px;")
        self.topic_combo.currentTextChanged.connect(self.on_topic_changed)
        
        # Özel konu girişi
        self.custom_topic_input = QLineEdit()
        self.custom_topic_input.setPlaceholderText("Özel konuyu buraya yazın...")
        self.custom_topic_input.setStyleSheet("padding: 8px; font-size: 14px; border: 2px solid #bdc3c7; border-radius: 5px;")
        self.custom_topic_input.setVisible(False)
        
        # Seviye seçimi
        self.level_combo = QComboBox()
        self.level_combo.addItems(list(LEVELS.keys()))
        self.level_combo.setStyleSheet("padding: 8px; font-size: 14px;")
        
        # Soru sayısı
        self.question_count_spin = QSpinBox()
        self.question_count_spin.setRange(5, 20)
        self.question_count_spin.setValue(10)
        self.question_count_spin.setStyleSheet("padding: 8px; font-size: 14px;")
        
        settings_layout.addRow("📚 Konu:", self.topic_combo)
        settings_layout.addRow("", self.custom_topic_input)
        settings_layout.addRow("📊 Seviye:", self.level_combo)
        settings_layout.addRow("🔢 Soru Sayısı:", self.question_count_spin)
        layout.addWidget(settings_group)
        
        # Butonlar
        button_layout = QHBoxLayout()
        
        back_btn = QPushButton("⬅️ Geri")
        back_btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 10px 20px;
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        back_btn.clicked.connect(self.show_welcome_page)
        
        start_game_btn = QPushButton("🎮 Oyunu Başlat")
        start_game_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 12px 25px;
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        start_game_btn.clicked.connect(self.start_game)
        
        button_layout.addWidget(back_btn)
        button_layout.addStretch()
        button_layout.addWidget(start_game_btn)
        layout.addLayout(button_layout)
        
        self.stacked_widget.addWidget(page)
    
    def create_game_page(self):
        """Oyun sayfası"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Üst panel - skorlar ve bilgiler
        top_panel = QWidget()
        top_layout = QHBoxLayout(top_panel)
        
        # Oyuncu 1 skoru
        self.player1_score_label = QLabel("🟡 Oyuncu 1: 0")
        self.player1_score_label.setStyleSheet(f"""
            background-color: {COLORS['player1']};
            padding: 15px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            color: #2c3e50;
        """)
        
        # Ortadaki bilgiler
        self.game_info_label = QLabel("Soru 1/10")
        self.game_info_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #2c3e50;
            text-align: center;
        """)
        self.game_info_label.setAlignment(Qt.AlignCenter)
        
        # Oyuncu 2 skoru
        self.player2_score_label = QLabel("🔵 Oyuncu 2: 0")
        self.player2_score_label.setStyleSheet(f"""
            background-color: {COLORS['player2']};
            padding: 15px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            color: #2c3e50;
        """)
        
        top_layout.addWidget(self.player1_score_label)
        top_layout.addWidget(self.game_info_label)
        top_layout.addWidget(self.player2_score_label)
        layout.addWidget(top_panel)
        
        # Sıra göstergesi
        self.turn_label = QLabel("🟡 1. Oyuncunun Sırası")
        self.turn_label.setStyleSheet(f"""
            background-color: {COLORS['player1']};
            padding: 10px;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            border-radius: 8px;
            color: #2c3e50;
        """)
        self.turn_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.turn_label)
        
        # Soru alanı
        self.question_label = QLabel("Soru yükleniyor...")
        self.question_label.setStyleSheet("""
            background-color: white;
            padding: 20px;
            font-size: 18px;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
            min-height: 100px;
        """)
        self.question_label.setWordWrap(True)
        layout.addWidget(self.question_label)
        
        # Şıklar
        self.option_buttons = []
        options_layout = QVBoxLayout()
        
        for i, option in enumerate(['A', 'B', 'C', 'D']):
            btn = QPushButton(f"{option}) Seçenek {option}")
            btn.setStyleSheet("""
                QPushButton {
                    padding: 15px;
                    font-size: 16px;
                    text-align: left;
                    background-color: white;
                    border: 2px solid #bdc3c7;
                    border-radius: 8px;
                    margin: 2px;
                }
                QPushButton:hover {
                    background-color: #ecf0f1;
                    border-color: #3498db;
                }
            """)
            btn.clicked.connect(lambda checked, opt=option: self.answer_question(opt))
            self.option_buttons.append(btn)
            options_layout.addWidget(btn)
        
        layout.addLayout(options_layout)
        
        # Alt panel - açıklama ve sonraki buton
        self.explanation_label = QLabel("")
        self.explanation_label.setStyleSheet("""
            background-color: #f8f9fa;
            padding: 15px;
            font-size: 14px;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            margin-top: 10px;
        """)
        self.explanation_label.setWordWrap(True)
        self.explanation_label.setVisible(False)
        layout.addWidget(self.explanation_label)
        
        self.next_button = QPushButton("➡️ Sonraki Soru")
        self.next_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 12px 25px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.next_button.clicked.connect(self.next_question)
        self.next_button.setVisible(False)
        layout.addWidget(self.next_button)
        
        self.stacked_widget.addWidget(page)
    
    def create_results_page(self):
        """Sonuçlar sayfası"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        
        # Başlık
        self.results_title = QLabel("🏆 Yarışma Sonucu")
        self.results_title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50; margin: 20px;")
        self.results_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.results_title)
        
        # Sonuç detayları
        self.results_detail = QLabel()
        self.results_detail.setStyleSheet("""
            font-size: 18px;
            color: #34495e;
            background-color: white;
            padding: 30px;
            border-radius: 15px;
            border: 2px solid #bdc3c7;
        """)
        self.results_detail.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.results_detail)
        
        # Butonlar
        button_layout = QHBoxLayout()
        
        new_game_btn = QPushButton("🔄 Yeni Oyun")
        new_game_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 12px 25px;
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        new_game_btn.clicked.connect(self.new_game)
        
        exit_btn = QPushButton("🚪 Çıkış")
        exit_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 12px 25px;
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        exit_btn.clicked.connect(self.close)
        
        button_layout.addWidget(new_game_btn)
        button_layout.addWidget(exit_btn)
        layout.addLayout(button_layout)
        
        self.stacked_widget.addWidget(page)
    
    def on_topic_changed(self, topic):
        """Konu değiştiğinde özel konu girişini göster/gizle"""
        if topic == "Özel Konu (Kendin Belirle)":
            self.custom_topic_input.setVisible(True)
        else:
            self.custom_topic_input.setVisible(False)
    
    def show_welcome_page(self):
        """Hoş geldin sayfasını göster"""
        self.stacked_widget.setCurrentIndex(0)
    
    def show_setup_page(self):
        """Kurulum sayfasını göster"""
        self.stacked_widget.setCurrentIndex(1)
    
    def start_game(self):
        """Oyunu başlat"""
        # Oyuncu isimlerini kontrol et
        player1_name = self.player1_input.text().strip()
        player2_name = self.player2_input.text().strip()
        
        if not player1_name or not player2_name:
            QMessageBox.warning(self, "Uyarı", "Lütfen her iki oyuncunun da adını girin!")
            return
        
        if player1_name == player2_name:
            QMessageBox.warning(self, "Uyarı", "Oyuncu isimleri farklı olmalıdır!")
            return
        
        # Ayarları kaydet
        self.players["player1"] = player1_name
        self.players["player2"] = player2_name
        
        selected_topic = self.topic_combo.currentText()
        if selected_topic == "Özel Konu (Kendin Belirle)":
            custom_topic = self.custom_topic_input.text().strip()
            if not custom_topic:
                QMessageBox.warning(self, "Uyarı", "Lütfen özel konuyu girin!")
                return
            self.game_settings["topic"] = custom_topic
        else:
            self.game_settings["topic"] = selected_topic
        
        self.game_settings["level"] = self.level_combo.currentText()
        self.game_settings["question_count"] = self.question_count_spin.value()
        
        # Oyunu başlat
        self.current_player = 1
        self.scores = {"player1": 0, "player2": 0}
        self.question_counter = 0
        
        # Oyuncuları veritabanına ekle
        self.add_players_to_db()
        
        # İlk soruyu yükle
        self.load_next_question()
        
        # Oyun sayfasını göster
        self.stacked_widget.setCurrentIndex(2)
    
    def add_players_to_db(self):
        """Oyuncuları veritabanına ekle"""
        try:
            conn = sqlite3.connect('db/quizapp.db')
            c = conn.cursor()
            
            for player in [self.players["player1"], self.players["player2"]]:
                c.execute("INSERT OR IGNORE INTO users (nickname) VALUES (?)", (player,))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Oyuncu ekleme hatası: {e}")
    
    def load_next_question(self):
        """Sonraki soruyu yükle"""
        if self.question_counter >= self.game_settings["question_count"]:
            self.end_game()
            return
        
        self.question_counter += 1
        
        # Soru üret
        question = self.question_service.generate_question(
            self.game_settings["topic"], 
            self.game_settings["level"]
        )
        
        if not question:
            QMessageBox.critical(self, "Hata", "Soru oluşturulamadı!")
            return
        
        self.current_question = question
        
        # Arayüzü güncelle
        self.update_game_ui()
        self.display_question()
    
    def update_game_ui(self):
        """Oyun arayüzünü güncelle"""
        # Skorları güncelle
        self.player1_score_label.setText(f"🟡 {self.players['player1']}: {self.scores['player1']}")
        self.player2_score_label.setText(f"🔵 {self.players['player2']}: {self.scores['player2']}")
        
        # Soru sayacını güncelle
        self.game_info_label.setText(f"Soru {self.question_counter}/{self.game_settings['question_count']}")
        
        # Sıra göstergesini güncelle
        if self.current_player == 1:
            self.turn_label.setText(f"🟡 {self.players['player1']}'in Sırası")
            self.turn_label.setStyleSheet(f"""
                background-color: {COLORS['player1']};
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                border-radius: 8px;
                color: #2c3e50;
            """)
        else:
            self.turn_label.setText(f"🔵 {self.players['player2']}'nin Sırası")
            self.turn_label.setStyleSheet(f"""
                background-color: {COLORS['player2']};
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                border-radius: 8px;
                color: #2c3e50;
            """)
    
    def display_question(self):
        """Soruyu ekranda göster"""
        if not self.current_question:
            return
        
        # Soru metnini göster
        self.question_label.setText(self.current_question["question"])
        
        # Şıkları güncelle
        for i, (option_key, option_text) in enumerate(self.current_question["options"].items()):
            btn = self.option_buttons[i]
            btn.setText(f"{option_key}) {option_text}")
            btn.setEnabled(True)
            btn.setStyleSheet("""
                QPushButton {
                    padding: 15px;
                    font-size: 16px;
                    text-align: left;
                    background-color: white;
                    border: 2px solid #bdc3c7;
                    border-radius: 8px;
                    margin: 2px;
                }
                QPushButton:hover {
                    background-color: #ecf0f1;
                    border-color: #3498db;
                }
            """)
        
        # Açıklama ve sonraki butonunu gizle
        self.explanation_label.setVisible(False)
        self.next_button.setVisible(False)
    
    def answer_question(self, selected_option):
        """Soruyu cevapla"""
        if not self.current_question:
            return
        
        correct_option = self.current_question["correct"]
        is_correct = selected_option == correct_option
        
        # Butonları devre dışı bırak
        for btn in self.option_buttons:
            btn.setEnabled(False)
        
        # Cevap renklerini göster
        for btn in self.option_buttons:
            option_key = btn.text()[0]  # A, B, C, D
            
            if option_key == correct_option:
                # Doğru cevap yeşil
                btn.setStyleSheet(f"""
                    QPushButton {{
                        padding: 15px;
                        font-size: 16px;
                        text-align: left;
                        background-color: {COLORS['correct']};
                        border: 2px solid #27ae60;
                        border-radius: 8px;
                        margin: 2px;
                        font-weight: bold;
                    }}
                """)
            elif option_key == selected_option and not is_correct:
                # Yanlış seçilen kırmızı
                btn.setStyleSheet(f"""
                    QPushButton {{
                        padding: 15px;
                        font-size: 16px;
                        text-align: left;
                        background-color: {COLORS['incorrect']};
                        border: 2px solid #e74c3c;
                        border-radius: 8px;
                        margin: 2px;
                        font-weight: bold;
                    }}
                """)
        
        # Skoru güncelle
        if is_correct:
            if self.current_player == 1:
                self.scores["player1"] += 1
            else:
                self.scores["player2"] += 1
        
        # Açıklamayı göster
        explanation = self.current_question.get("explanation", "")
        if explanation:
            status = "✅ Doğru!" if is_correct else "❌ Yanlış!"
            self.explanation_label.setText(f"{status}\n\n📝 Açıklama: {explanation}")
            self.explanation_label.setVisible(True)
        
        # UI'yi güncelle
        self.update_game_ui()
        
        # Sonraki butonu göster
        self.next_button.setVisible(True)
    
    def next_question(self):
        """Sonraki soruya geç"""
        # Oyuncu sırasını değiştir
        self.current_player = 2 if self.current_player == 1 else 1
        
        # Sonraki soruyu yükle
        self.load_next_question()
    
    def end_game(self):
        """Oyunu bitir"""
        # Sonuçları hesapla
        score1 = self.scores["player1"]
        score2 = self.scores["player2"]
        
        if score1 > score2:
            winner = self.players["player1"]
            result_text = f"🏆 Tebrikler {winner}!\n\n"
        elif score2 > score1:
            winner = self.players["player2"]
            result_text = f"🏆 Tebrikler {winner}!\n\n"
        else:
            result_text = "🤝 Beraberlik!\n\n"
        
        result_text += f"""
📊 Final Skorları:
🟡 {self.players['player1']}: {score1}/{self.game_settings['question_count']}
🔵 {self.players['player2']}: {score2}/{self.game_settings['question_count']}

📚 Konu: {self.game_settings['topic']}
📊 Seviye: {self.game_settings['level']}
        """
        
        self.results_detail.setText(result_text)
        
        # Sonucu veritabanına kaydet
        self.save_match_result()
        
        # Sonuçlar sayfasını göster
        self.stacked_widget.setCurrentIndex(3)
    
    def save_match_result(self):
        """Maç sonucunu veritabanına kaydet"""
        try:
            conn = sqlite3.connect('db/quizapp.db')
            c = conn.cursor()
            
            # Oyuncu ID'lerini al
            c.execute("SELECT id FROM users WHERE nickname = ?", (self.players["player1"],))
            user1_id = c.fetchone()[0]
            
            c.execute("SELECT id FROM users WHERE nickname = ?", (self.players["player2"],))
            user2_id = c.fetchone()[0]
            
            # Maç sonucunu kaydet
            c.execute("""
                INSERT INTO matches (user1_id, user2_id, user1_name, user2_name, score1, score2, topic, level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user1_id, user2_id,
                self.players["player1"], self.players["player2"],
                self.scores["player1"], self.scores["player2"],
                self.game_settings["topic"], self.game_settings["level"]
            ))
            
            conn.commit()
            conn.close()
            print("✅ Maç sonucu kaydedildi")
        
        except Exception as e:
            print(f"❌ Maç sonucu kaydetme hatası: {e}")
    
    def new_game(self):
        """Yeni oyun başlat"""
        # Ayarları sıfırla
        self.current_question = None
        self.current_player = 1
        self.scores = {"player1": 0, "player2": 0}
        self.question_counter = 0
        
        # Kurulum sayfasına dön
        self.show_setup_page()

def main():
    app = QApplication(sys.argv)
    window = QuizApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
