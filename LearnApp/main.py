import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QLabel, QLineEdit, QComboBox,
                             QSpinBox, QTextEdit, QMessageBox, QFrame, QButtonGroup,
                             QRadioButton, QDialog, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPalette
import sqlite3
from db.database import Database
from question_generator import QuestionGenerator
from config import TOPICS, LEVELS, COLORS

class UserRegistrationDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Kullanıcı Kaydı")
        self.setModal(True)
        self.resize(300, 150)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Kullanıcı Adı:"))
        self.nickname_input = QLineEdit()
        layout.addWidget(self.nickname_input)
        
        button_layout = QHBoxLayout()
        
        register_btn = QPushButton("Kaydet")
        register_btn.clicked.connect(self.register_user)
        button_layout.addWidget(register_btn)
        
        cancel_btn = QPushButton("İptal")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def register_user(self):
        nickname = self.nickname_input.text().strip()
        if not nickname:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı boş olamaz!")
            return
        
        user_id = self.db.add_user(nickname)
        if user_id:
            QMessageBox.information(self, "Başarılı", f"{nickname} kullanıcısı kaydedildi!")
            self.accept()
        else:
            QMessageBox.warning(self, "Hata", "Bu kullanıcı adı zaten mevcut!")

class GameSetupWidget(QWidget):
    gameStarted = pyqtSignal(dict)
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.refresh_users()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Başlık
        title = QLabel("AI Destekli Soru-Cevap Yarışması")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Kullanıcı seçimi
        user_frame = QFrame()
        user_layout = QHBoxLayout()
        
        # Kullanıcı 1
        user1_layout = QVBoxLayout()
        user1_layout.addWidget(QLabel("Oyuncu 1 (Sarı):"))
        self.user1_combo = QComboBox()
        user1_layout.addWidget(self.user1_combo)
        user_frame1 = QFrame()
        user_frame1.setLayout(user1_layout)
        user_frame1.setStyleSheet(f"background-color: {COLORS['player1']}; border-radius: 10px; padding: 10px;")
        user_layout.addWidget(user_frame1)
        
        # Kullanıcı 2
        user2_layout = QVBoxLayout()
        user2_layout.addWidget(QLabel("Oyuncu 2 (Mavi):"))
        self.user2_combo = QComboBox()
        user2_layout.addWidget(self.user2_combo)
        user_frame2 = QFrame()
        user_frame2.setLayout(user2_layout)
        user_frame2.setStyleSheet(f"background-color: {COLORS['player2']}; border-radius: 10px; padding: 10px;")
        user_layout.addWidget(user_frame2)
        
        user_frame.setLayout(user_layout)
        layout.addWidget(user_frame)
        
        # Kullanıcı ekle butonu
        add_user_btn = QPushButton("Yeni Kullanıcı Ekle")
        add_user_btn.clicked.connect(self.add_user)
        layout.addWidget(add_user_btn)
        
        # Konu seçimi
        layout.addWidget(QLabel("Konu Seçimi:"))
        self.topic_combo = QComboBox()
        self.topic_combo.addItems(TOPICS)
        layout.addWidget(self.topic_combo)
        
        # Özel konu
        self.custom_topic_input = QLineEdit()
        self.custom_topic_input.setPlaceholderText("Özel konu yazın...")
        self.custom_topic_input.setEnabled(False)
        layout.addWidget(self.custom_topic_input)
        
        self.topic_combo.currentTextChanged.connect(self.on_topic_changed)
        
        # Seviye seçimi
        layout.addWidget(QLabel("Zorluk Seviyesi:"))
        self.level_combo = QComboBox()
        self.level_combo.addItems(LEVELS.keys())
        layout.addWidget(self.level_combo)
        
        # Soru sayısı
        layout.addWidget(QLabel("Soru Sayısı:"))
        self.question_count = QSpinBox()
        self.question_count.setMinimum(1)
        self.question_count.setMaximum(20)
        self.question_count.setValue(5)
        layout.addWidget(self.question_count)
        
        # Başlat butonu
        start_btn = QPushButton("Testi Başlat")
        start_btn.setFont(QFont("Arial", 12, QFont.Bold))
        start_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        start_btn.clicked.connect(self.start_game)
        layout.addWidget(start_btn)
        
        # Geçmiş sonuçlar butonu
        history_btn = QPushButton("Geçmiş Sonuçlar")
        history_btn.clicked.connect(self.show_history)
        layout.addWidget(history_btn)
        
        self.setLayout(layout)
    
    def refresh_users(self):
        users = self.db.get_all_users()
        self.user1_combo.clear()
        self.user2_combo.clear()
        
        for user in users:
            self.user1_combo.addItem(user[1], user[0])  # nickname, id
            self.user2_combo.addItem(user[1], user[0])
    
    def add_user(self):
        dialog = UserRegistrationDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            self.refresh_users()
    
    def on_topic_changed(self, topic):
        self.custom_topic_input.setEnabled(topic == "Özel Konu (Kendin Belirle)")
    
    def start_game(self):
        if self.user1_combo.currentData() == self.user2_combo.currentData():
            QMessageBox.warning(self, "Hata", "İki farklı oyuncu seçmelisiniz!")
            return
        
        topic = self.topic_combo.currentText()
        if topic == "Özel Konu (Kendin Belirle)":
            topic = self.custom_topic_input.text().strip()
            if not topic:
                QMessageBox.warning(self, "Hata", "Özel konu yazmalısınız!")
                return
        
        game_config = {
            'user1_id': self.user1_combo.currentData(),
            'user1_name': self.user1_combo.currentText(),
            'user2_id': self.user2_combo.currentData(),
            'user2_name': self.user2_combo.currentText(),
            'topic': topic,
            'level': self.level_combo.currentText(),
            'question_count': self.question_count.value()
        }
        
        self.gameStarted.emit(game_config)
    
    def show_history(self):
        dialog = HistoryDialog(self.db)
        dialog.exec_()

class HistoryDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Geçmiş Sonuçlar")
        self.resize(800, 400)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        headers = ["Tarih", "Oyuncu 1", "Skor 1", "Oyuncu 2", "Skor 2", "Konu", "Seviye"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        matches = self.db.get_match_history()
        self.table.setRowCount(len(matches))
        
        for row, match in enumerate(matches):
            self.table.setItem(row, 0, QTableWidgetItem(str(match[8])))  # created_at
            self.table.setItem(row, 1, QTableWidgetItem(match[9]))       # user1_name
            self.table.setItem(row, 2, QTableWidgetItem(str(match[3])))  # user1_score
            self.table.setItem(row, 3, QTableWidgetItem(match[10]))      # user2_name
            self.table.setItem(row, 4, QTableWidgetItem(str(match[4])))  # user2_score
            self.table.setItem(row, 5, QTableWidgetItem(match[5]))       # topic
            self.table.setItem(row, 6, QTableWidgetItem(match[6]))       # level
        
        layout.addWidget(self.table)
        
        close_btn = QPushButton("Kapat")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

class GameWidget(QWidget):
    gameFinished = pyqtSignal()
    
    def __init__(self, db, question_generator, game_config):
        super().__init__()
        self.db = db
        self.question_generator = question_generator
        self.game_config = game_config
        self.current_question = 0
        self.current_player = 1
        self.scores = [0, 0]
        self.questions = []
        self.match_id = None
        self.init_ui()
        self.start_game()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Skor paneli
        score_layout = QHBoxLayout()
        
        self.player1_score = QLabel(f"{self.game_config['user1_name']}: 0")
        self.player1_score.setFont(QFont("Arial", 14, QFont.Bold))
        self.player1_score.setStyleSheet(f"background-color: {COLORS['player1']}; padding: 10px; border-radius: 5px;")
        score_layout.addWidget(self.player1_score)
        
        self.player2_score = QLabel(f"{self.game_config['user2_name']}: 0")
        self.player2_score.setFont(QFont("Arial", 14, QFont.Bold))
        self.player2_score.setStyleSheet(f"background-color: {COLORS['player2']}; padding: 10px; border-radius: 5px;")
        score_layout.addWidget(self.player2_score)
        
        layout.addLayout(score_layout)
        
        # Sıra göstergesi
        self.turn_label = QLabel()
        self.turn_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.turn_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.turn_label)
        
        # Soru paneli
        self.question_label = QLabel()
        self.question_label.setFont(QFont("Arial", 12))
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("background-color: white; padding: 15px; border-radius: 5px; border: 2px solid #ddd;")
        layout.addWidget(self.question_label)
        
        # Seçenekler
        self.option_buttons = QButtonGroup()
        options_layout = QVBoxLayout()
        
        for i, option in enumerate(['A', 'B', 'C', 'D']):
            btn = QRadioButton()
            btn.setFont(QFont("Arial", 10))
            self.option_buttons.addButton(btn, i)
            options_layout.addWidget(btn)
        
        layout.addLayout(options_layout)
        
        # Cevapla butonu
        self.answer_btn = QPushButton("Cevapla")
        self.answer_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.answer_btn.clicked.connect(self.submit_answer)
        layout.addWidget(self.answer_btn)
        
        # Açıklama alanı
        self.explanation_text = QTextEdit()
        self.explanation_text.setMaximumHeight(100)
        self.explanation_text.setVisible(False)
        layout.addWidget(self.explanation_text)
        
        # Sonraki soru butonu
        self.next_btn = QPushButton("Sonraki Soru")
        self.next_btn.setFont(QFont("Arial", 12))
        self.next_btn.clicked.connect(self.next_question)
        self.next_btn.setVisible(False)
        layout.addWidget(self.next_btn)
        
        self.setLayout(layout)
    
    def start_game(self):
        self.match_id = self.db.create_match(
            self.game_config['user1_id'],
            self.game_config['user2_id'],
            self.game_config['topic'],
            self.game_config['level'],
            self.game_config['question_count']
        )
        self.load_next_question()
    
    def load_next_question(self):
        if self.current_question >= self.game_config['question_count']:
            self.end_game()
            return
        
        # Sırayı değiştir
        self.current_player = 1 if self.current_question % 2 == 0 else 2
        
        # Ekran rengini değiştir
        if self.current_player == 1:
            color = COLORS['player1']
            player_name = self.game_config['user1_name']
        else:
            color = COLORS['player2'] 
            player_name = self.game_config['user2_name']
        
        self.setStyleSheet(f"background-color: {color};")
        self.turn_label.setText(f"{player_name}'in Sırası - Soru {self.current_question + 1}/{self.game_config['question_count']}")
        
        # Soru üret
        question_data = self.question_generator.generate_question(
            self.game_config['topic'],
            self.game_config['level']
        )
        
        self.current_question_data = question_data
        self.questions.append(question_data)
        
        # Soruyu göster
        self.question_label.setText(question_data['question'])
        
        # Seçenekleri göster
        for i, (key, value) in enumerate(question_data['options'].items()):
            btn = self.option_buttons.button(i)
            btn.setText(f"{key}) {value}")
            btn.setChecked(False)
        
        # UI durumunu sıfırla
        self.answer_btn.setVisible(True)
        self.next_btn.setVisible(False)
        self.explanation_text.setVisible(False)
        
        # Butonları etkinleştir
        for btn in self.option_buttons.buttons():
            btn.setEnabled(True)
    
    def submit_answer(self):
        selected_id = self.option_buttons.checkedId()
        if selected_id == -1:
            QMessageBox.warning(self, "Hata", "Bir seçenek seçmelisiniz!")
            return
        
        # Seçilen cevabı al
        selected_option = ['A', 'B', 'C', 'D'][selected_id]
        correct_answer = self.current_question_data['correct_answer']
        
        # Cevabı kontrol et
        is_correct = self.question_generator.check_answer(selected_option, correct_answer)
        
        if is_correct:
            self.scores[self.current_player - 1] += 1
            self.setStyleSheet(f"background-color: {COLORS['correct']};")
        else:
            self.setStyleSheet(f"background-color: {COLORS['incorrect']};")
        
        # Skorları güncelle
        self.update_scores()
        
        # Açıklama göster
        explanation = self.question_generator.get_explanation(self.current_question_data, selected_option)
        self.explanation_text.setText(explanation)
        self.explanation_text.setVisible(True)
        
        # Butonları devre dışı bırak
        for btn in self.option_buttons.buttons():
            btn.setEnabled(False)
        
        self.answer_btn.setVisible(False)
        self.next_btn.setVisible(True)
        
        # Doğru cevabı işaretle
        correct_btn = self.option_buttons.button(['A', 'B', 'C', 'D'].index(correct_answer))
        correct_btn.setStyleSheet("background-color: green; color: white;")
        
        if not is_correct:
            selected_btn = self.option_buttons.button(selected_id)
            selected_btn.setStyleSheet("background-color: red; color: white;")
    
    def update_scores(self):
        self.player1_score.setText(f"{self.game_config['user1_name']}: {self.scores[0]}")
        self.player2_score.setText(f"{self.game_config['user2_name']}: {self.scores[1]}")
    
    def next_question(self):
        # Buton stillerini sıfırla
        for btn in self.option_buttons.buttons():
            btn.setStyleSheet("")
        
        self.current_question += 1
        self.load_next_question()
    
    def end_game(self):
        # Skorları veritabanına kaydet
        self.db.update_match_scores(self.match_id, self.scores[0], self.scores[1])
        
        # Sonuç mesajı
        if self.scores[0] > self.scores[1]:
            winner = self.game_config['user1_name']
        elif self.scores[1] > self.scores[0]:
            winner = self.game_config['user2_name']
        else:
            winner = "Berabere!"
        
        result_msg = f"""
        Oyun Bitti!
        
        {self.game_config['user1_name']}: {self.scores[0]} puan
        {self.game_config['user2_name']}: {self.scores[1]} puan
        
        Kazanan: {winner}
        """
        
        QMessageBox.information(self, "Oyun Sonucu", result_msg)
        self.gameFinished.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.question_generator = QuestionGenerator()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("AI Destekli Soru-Cevap Uygulaması")
        self.setGeometry(100, 100, 1000, 700)
        
        # Ana widget
        self.setup_widget = GameSetupWidget(self.db)
        self.setup_widget.gameStarted.connect(self.start_game)
        self.setCentralWidget(self.setup_widget)
    
    def start_game(self, game_config):
        self.game_widget = GameWidget(self.db, self.question_generator, game_config)
        self.game_widget.gameFinished.connect(self.return_to_setup)
        self.setCentralWidget(self.game_widget)
    
    def return_to_setup(self):
        self.setup_widget.refresh_users()
        self.setCentralWidget(self.setup_widget)

def main():
    app = QApplication(sys.argv)
    
    # Uygulama stilini ayarla
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
