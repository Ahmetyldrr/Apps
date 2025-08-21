import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QComboBox, QSpinBox, QRadioButton, QButtonGroup,
                             QTextEdit, QMessageBox, QStackedWidget, QFrame)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette
from config import TOPICS, LEVELS, COLORS
from manual_together_ai_service import manual_together_ai

def create_tables():
    """Veritabanı tablolarını oluştur"""
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
        score1 INTEGER,
        score2 INTEGER,
        topic TEXT,
        level TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user1_id) REFERENCES users(id),
        FOREIGN KEY(user2_id) REFERENCES users(id)
    )''')
    
    conn.commit()
    conn.close()

def add_user(nickname):
    """Kullanıcı ekle"""
    conn = sqlite3.connect('db/quizapp.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (nickname) VALUES (?)", (nickname,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Kullanıcı zaten mevcut
    finally:
        conn.close()

def get_user_by_nickname(nickname):
    """Kullanıcıyı nickname ile bul"""
    conn = sqlite3.connect('db/quizapp.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE nickname = ?", (nickname,))
    user = c.fetchone()
    conn.close()
    return user

def save_match_result(user1_id, user2_id, score1, score2, topic, level):
    """Karşılaşma sonucunu kaydet"""
    conn = sqlite3.connect('db/quizapp.db')
    c = conn.cursor()
    c.execute("""INSERT INTO matches (user1_id, user2_id, score1, score2, topic, level) 
                 VALUES (?, ?, ?, ?, ?, ?)""", 
              (user1_id, user2_id, score1, score2, topic, level))
    conn.commit()
    conn.close()

class QuestionGeneratorThread(QThread):
    """Soru üretimi için ayrı thread"""
    question_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, topic, level):
        super().__init__()
        self.topic = topic
        self.level = level
    
    def run(self):
        try:
            questions = manual_together_ai.generate_question(self.topic, self.level)
            if questions and len(questions) > 0:
                self.question_ready.emit(questions[0])
            else:
                self.error_occurred.emit("Soru üretilemedi")
        except Exception as e:
            self.error_occurred.emit(f"Soru üretme hatası: {str(e)}")

class QuizApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Destekli Soru Cevap Yarışması")
        self.setGeometry(100, 100, 1000, 700)
        
        # Veritabanını başlat
        create_tables()
        
        # Ana widget ve stack
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        # Oyun verileri
        self.current_question = None
        self.current_player = 1
        self.player1_score = 0
        self.player2_score = 0
        self.question_count = 0
        self.total_questions = 10
        self.selected_topic = ""
        self.selected_level = ""
        self.player1_name = ""
        self.player2_name = ""
        
        # Thread referansı
        self.question_thread = None
        
        # Ekranları oluştur
        self.create_user_screen()
        self.create_game_setup_screen() 
        self.create_quiz_screen()
        self.create_result_screen()
        
        # İlk ekranı göster
        self.central_widget.setCurrentWidget(self.user_screen)
        
        # API bağlantısını test et
        self.test_api_connection()
    
    def test_api_connection(self):
        """Başlangıçta API bağlantısını test et"""
        if not manual_together_ai.test_connection():
            QMessageBox.warning(self, "Uyarı", 
                              "AI servisi ile bağlantı kurulamadı.\n"
                              "Yedek sorular kullanılacak.\n"
                              "İnternet bağlantınızı kontrol edin.")
    
    def create_user_screen(self):
        """Kullanıcı ekleme ekranı"""
        self.user_screen = QWidget()
        layout = QVBoxLayout()
        
        # Başlık
        title = QLabel("AI Destekli Soru Cevap Yarışması")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(title)
        
        # Kullanıcı 1
        user1_frame = QFrame()
        user1_frame.setFrameStyle(QFrame.Box)
        user1_layout = QVBoxLayout()
        
        user1_label = QLabel("Oyuncu 1 (Sarı)")
        user1_label.setStyleSheet(f"background-color: {COLORS['player1']}; padding: 10px; font-weight: bold;")
        user1_layout.addWidget(user1_label)
        
        self.user1_input = QLineEdit()
        self.user1_input.setPlaceholderText("Kullanıcı adı girin...")
        user1_layout.addWidget(self.user1_input)
        
        user1_frame.setLayout(user1_layout)
        layout.addWidget(user1_frame)
        
        # Kullanıcı 2
        user2_frame = QFrame()
        user2_frame.setFrameStyle(QFrame.Box)
        user2_layout = QVBoxLayout()
        
        user2_label = QLabel("Oyuncu 2 (Mavi)")
        user2_label.setStyleSheet(f"background-color: {COLORS['player2']}; padding: 10px; font-weight: bold;")
        user2_layout.addWidget(user2_label)
        
        self.user2_input = QLineEdit()
        self.user2_input.setPlaceholderText("Kullanıcı adı girin...")
        user2_layout.addWidget(self.user2_input)
        
        user2_frame.setLayout(user2_layout)
        layout.addWidget(user2_frame)
        
        # Kullanıcı kaydet butonu
        self.add_users_btn = QPushButton("Kullanıcıları Kaydet")
        self.add_users_btn.clicked.connect(self.add_users)
        layout.addWidget(self.add_users_btn)
        
        self.user_screen.setLayout(layout)
        # Widget'ı stack'e ekle
        self.central_widget.addWidget(self.user_screen)
    
    def create_game_setup_screen(self):
        """Oyun kurulum ekranı"""
        self.setup_screen = QWidget()
        layout = QVBoxLayout()
        
        # Başlık
        title = QLabel("Oyun Ayarları")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        layout.addWidget(title)
        
        # Konu seçimi
        topic_label = QLabel("Konu Seçin:")
        layout.addWidget(topic_label)
        
        self.topic_combo = QComboBox()
        self.topic_combo.addItems(TOPICS)
        self.topic_combo.currentTextChanged.connect(self.on_topic_changed)
        layout.addWidget(self.topic_combo)
        
        # Özel konu girişi
        self.custom_topic_input = QLineEdit()
        self.custom_topic_input.setPlaceholderText("Özel konunuzu buraya yazın...")
        self.custom_topic_input.setVisible(False)
        layout.addWidget(self.custom_topic_input)
        
        # Seviye seçimi
        level_label = QLabel("Zorluk Seviyesi:")
        layout.addWidget(level_label)
        
        self.level_combo = QComboBox()
        self.level_combo.addItems(LEVELS.keys())
        layout.addWidget(self.level_combo)
        
        # Soru sayısı
        count_label = QLabel("Soru Sayısı:")
        layout.addWidget(count_label)
        
        self.question_count_spin = QSpinBox()
        self.question_count_spin.setRange(5, 50)
        self.question_count_spin.setValue(10)
        layout.addWidget(self.question_count_spin)
        
        # Testi başlat butonu
        self.start_test_btn = QPushButton("Testi Başlat")
        self.start_test_btn.clicked.connect(self.start_quiz)
        layout.addWidget(self.start_test_btn)
        
        self.setup_screen.setLayout(layout)
        # Widget'ı stack'e ekle
        self.central_widget.addWidget(self.setup_screen)
    
    def create_quiz_screen(self):
        """Quiz ekranı"""
        self.quiz_screen = QWidget()
        layout = QVBoxLayout()
        
        # Üst bilgi paneli
        info_layout = QHBoxLayout()
        
        # Oyuncu bilgileri
        self.player1_info = QLabel("Oyuncu 1: 0 puan")
        self.player1_info.setStyleSheet(f"background-color: {COLORS['player1']}; padding: 10px; font-weight: bold;")
        info_layout.addWidget(self.player1_info)
        
        self.player2_info = QLabel("Oyuncu 2: 0 puan") 
        self.player2_info.setStyleSheet(f"background-color: {COLORS['player2']}; padding: 10px; font-weight: bold;")
        info_layout.addWidget(self.player2_info)
        
        layout.addLayout(info_layout)
        
        # Mevcut oyuncu ve soru sayısı
        self.current_info = QLabel("Soru 1/10 - Oyuncu 1'in sırası")
        self.current_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.current_info.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(self.current_info)
        
        # Soru metni
        self.question_label = QLabel("Soru yükleniyor...")
        self.question_label.setWordWrap(True)
        self.question_label.setFont(QFont("Arial", 14))
        self.question_label.setStyleSheet("padding: 20px; border: 2px solid black;")
        layout.addWidget(self.question_label)
        
        # Seçenekler
        self.option_group = QButtonGroup()
        self.option_buttons = {}
        
        for option in ['A', 'B', 'C', 'D']:
            btn = QRadioButton()
            btn.setFont(QFont("Arial", 12))
            self.option_buttons[option] = btn
            self.option_group.addButton(btn)
            layout.addWidget(btn)
        
        # Cevapla butonu
        self.answer_btn = QPushButton("Cevapla")
        self.answer_btn.clicked.connect(self.check_answer)
        layout.addWidget(self.answer_btn)
        
        # Açıklama alanı
        self.explanation_text = QTextEdit()
        self.explanation_text.setMaximumHeight(100)
        self.explanation_text.setVisible(False)
        layout.addWidget(self.explanation_text)
        
        # Sonraki soru butonu
        self.next_btn = QPushButton("Sonraki Soru")
        self.next_btn.clicked.connect(self.next_question)
        self.next_btn.setVisible(False)
        layout.addWidget(self.next_btn)
        
        self.quiz_screen.setLayout(layout)
        # Widget'ı stack'e ekle
        self.central_widget.addWidget(self.quiz_screen)
    
    def create_result_screen(self):
        """Sonuç ekranı"""
        self.result_screen = QWidget()
        layout = QVBoxLayout()
        
        # Başlık
        title = QLabel("Yarışma Sonuçları")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(title)
        
        # Sonuç metni
        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setFont(QFont("Arial", 18))
        layout.addWidget(self.result_label)
        
        # Skorlar
        self.score_label = QLabel()
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_label.setFont(QFont("Arial", 16))
        layout.addWidget(self.score_label)
        
        # Yeni oyun butonu
        self.new_game_btn = QPushButton("Yeni Oyun")
        self.new_game_btn.clicked.connect(self.new_game)
        layout.addWidget(self.new_game_btn)
        
        self.result_screen.setLayout(layout)
        # Widget'ı stack'e ekle
        self.central_widget.addWidget(self.result_screen)
    
    def on_topic_changed(self, topic):
        """Konu değiştiğinde çağrılır"""
        if topic == "Özel Konu (Kendin Belirle)":
            self.custom_topic_input.setVisible(True)
        else:
            self.custom_topic_input.setVisible(False)
    
    def add_users(self):
        """Kullanıcıları veritabanına ekle"""
        user1 = self.user1_input.text().strip()
        user2 = self.user2_input.text().strip()
        
        if not user1 or not user2:
            QMessageBox.warning(self, "Hata", "Lütfen her iki kullanıcı adını da girin!")
            return
        
        if user1 == user2:
            QMessageBox.warning(self, "Hata", "Kullanıcı adları farklı olmalıdır!")
            return
        
        try:
            add_user(user1)
            add_user(user2)
            self.player1_name = user1
            self.player2_name = user2
            self.central_widget.setCurrentWidget(self.setup_screen)
        except Exception as e:
            QMessageBox.information(self, "Bilgi", f"Kullanıcılar zaten mevcut veya eklendi: {str(e)}")
            self.player1_name = user1
            self.player2_name = user2
            self.central_widget.setCurrentWidget(self.setup_screen)
    
    def start_quiz(self):
        """Quiz'i başlat"""
        topic = self.topic_combo.currentText()
        if topic == "Özel Konu (Kendin Belirle)":
            topic = self.custom_topic_input.text().strip()
            if not topic:
                QMessageBox.warning(self, "Hata", "Lütfen özel konuyu belirtin!")
                return
        
        self.selected_topic = topic
        self.selected_level = self.level_combo.currentText()
        self.total_questions = self.question_count_spin.value()
        
        # Oyun değişkenlerini sıfırla
        self.current_player = 1
        self.player1_score = 0
        self.player2_score = 0
        self.question_count = 0
        
        # Quiz ekranına geç ve ilk soruyu yükle
        self.central_widget.setCurrentWidget(self.quiz_screen)
        self.load_next_question()
    
    def load_next_question(self):
        """Sonraki soruyu yükle"""
        self.question_count += 1
        
        if self.question_count > self.total_questions:
            self.show_results()
            return
        
        # UI'yi güncelle
        current_player_name = self.player1_name if self.current_player == 1 else self.player2_name
        self.current_info.setText(f"Soru {self.question_count}/{self.total_questions} - {current_player_name}'in sırası")
        
        # Ekran rengini değiştir
        color = COLORS['player1'] if self.current_player == 1 else COLORS['player2']
        self.quiz_screen.setStyleSheet(f"background-color: {color};")
        
        # Önceki sorunun UI'sini temizle
        self.answer_btn.setVisible(True)
        self.next_btn.setVisible(False)
        self.explanation_text.setVisible(False)
        
        for btn in self.option_buttons.values():
            btn.setChecked(False)
            btn.setStyleSheet("")
        
        # Soru yükleme göster
        self.question_label.setText("Soru üretiliyor...")
        self.answer_btn.setEnabled(False)
        
        # Soru üret (thread'de)
        self.question_thread = QuestionGeneratorThread(self.selected_topic, self.selected_level)
        self.question_thread.question_ready.connect(self.display_question)
        self.question_thread.error_occurred.connect(self.handle_question_error)
        self.question_thread.start()
    
    def display_question(self, question_data):
        """Üretilen soruyu ekranda göster"""
        self.current_question = question_data
        
        # Soru metnini göster
        self.question_label.setText(question_data['question'])
        
        # Seçenekleri göster
        for option, btn in self.option_buttons.items():
            btn.setText(f"{option}) {question_data['options'][option]}")
        
        self.answer_btn.setEnabled(True)
    
    def handle_question_error(self, error_message):
        """Soru üretme hatasını handle et"""
        QMessageBox.warning(self, "Hata", f"Soru üretme hatası: {error_message}")
        # Yedek soru kullan
        fallback_questions = manual_together_ai._create_fallback_question(self.selected_topic, self.selected_level)
        self.current_question = fallback_questions[0] if fallback_questions else None
        self.display_question(self.current_question)
    
    def check_answer(self):
        """Cevabı kontrol et"""
        if not self.current_question:
            QMessageBox.warning(self, "Hata", "Geçerli soru bulunamadı!")
            return
            
        selected_option = None
        for option, btn in self.option_buttons.items():
            if btn.isChecked():
                selected_option = option
                break
        
        if not selected_option:
            QMessageBox.warning(self, "Hata", "Lütfen bir seçenek seçin!")
            return
        
        correct_answer = self.current_question['correct_answer']
        is_correct = selected_option == correct_answer
        
        # Cevabı renklendír
        for option, btn in self.option_buttons.items():
            if option == correct_answer:
                btn.setStyleSheet(f"background-color: {COLORS['correct']};")
            elif option == selected_option and not is_correct:
                btn.setStyleSheet(f"background-color: {COLORS['incorrect']};")
        
        # Skoru güncelle
        if is_correct:
            if self.current_player == 1:
                self.player1_score += 1
            else:
                self.player2_score += 1
        
        # Skorları göster
        self.player1_info.setText(f"{self.player1_name}: {self.player1_score} puan")
        self.player2_info.setText(f"{self.player2_name}: {self.player2_score} puan")
        
        # Açıklamayı göster
        if self.current_question and 'explanation' in self.current_question:
            self.explanation_text.setText(self.current_question['explanation'])
        else:
            self.explanation_text.setText("Açıklama bulunamadı.")
        self.explanation_text.setVisible(True)
        
        # UI'yi güncelle
        self.answer_btn.setVisible(False)
        self.next_btn.setVisible(True)
    
    def next_question(self):
        """Sonraki soruya geç"""
        # Oyuncuları değiştir
        self.current_player = 2 if self.current_player == 1 else 1
        self.load_next_question()
    
    def show_results(self):
        """Sonuçları göster"""
        # Kazananı belirle
        if self.player1_score > self.player2_score:
            winner = f"{self.player1_name} Kazandı!"
            winner_color = COLORS['player1']
        elif self.player2_score > self.player1_score:
            winner = f"{self.player2_name} Kazandı!"
            winner_color = COLORS['player2']
        else:
            winner = "Berabere!"
            winner_color = COLORS['default']
        
        self.result_label.setText(winner)
        self.result_label.setStyleSheet(f"background-color: {winner_color}; padding: 20px;")
        
        self.score_label.setText(f"{self.player1_name}: {self.player1_score} puan\n{self.player2_name}: {self.player2_score} puan")
        
        # Sonucu veritabanına kaydet
        try:
            user1 = get_user_by_nickname(self.player1_name)
            user2 = get_user_by_nickname(self.player2_name)
            if user1 and user2:
                save_match_result(user1[0], user2[0], self.player1_score, self.player2_score, 
                                self.selected_topic, self.selected_level)
        except Exception as e:
            print(f"Sonuç kaydetme hatası: {e}")
        
        self.central_widget.setCurrentWidget(self.result_screen)
    
    def new_game(self):
        """Yeni oyun başlat"""
        self.quiz_screen.setStyleSheet("")  # Rengi sıfırla
        self.central_widget.setCurrentWidget(self.user_screen)
        
        # Inputları temizle
        self.user1_input.clear()
        self.user2_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizApp()
    window.show()
    sys.exit(app.exec_())
