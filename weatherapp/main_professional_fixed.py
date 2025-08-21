import sys
import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(60)
        self.init_animation()
        self.setup_style()
    
    def init_animation(self):
        self.animation = QPropertyAnimation(self, b"size")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
    
    def setup_style(self):
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 12px;
                font-weight: bold;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2980b9, stop:1 #3498db);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1f4e79, stop:1 #2c6aa0);
            }
        """)
    
    def enterEvent(self, event):
        original_size = self.size()
        new_size = QSize(original_size.width() + 5, original_size.height() + 2)
        self.animation.setStartValue(original_size)
        self.animation.setEndValue(new_size)
        self.animation.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        current_size = self.size()
        original_size = QSize(current_size.width() - 5, current_size.height() - 2)
        self.animation.setStartValue(current_size)
        self.animation.setEndValue(original_size)
        self.animation.start()
        super().leaveEvent(event)

class ModernWeatherCard(QFrame):
    def __init__(self, city, data, parent=None):
        super().__init__(parent)
        self.city = city
        self.data = data
        self.setup_ui()
        self.setup_style()
        self.setup_shadow()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Şehir başlığı
        city_label = QLabel(f"{self.city}")
        city_label.setFont(QFont("Arial", 14, QFont.Bold))
        city_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(city_label)
        
        # Sıcaklık
        if self.data:
            temp = self.data[0][4]  # temperature
            temp_label = QLabel(f"{temp:.0f}°C")
            temp_label.setFont(QFont("Arial", 28, QFont.Bold))
            temp_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(temp_label)
            
            # Hava durumu bilgileri - Daha kompakt
            info_layout = QGridLayout()
            info_layout.setSpacing(3)
            info_layout.setContentsMargins(5, 5, 5, 5)
            
            labels_data = [
                ("Nem", f"{self.data[0][7]}%"),
                ("Ruzgar", f"{self.data[0][6]:.0f} km/h"),
                ("Bulut", f"{self.data[0][5]}%"),
                ("Hissedilen", f"{self.data[0][10]:.0f}°C")
            ]
            
            for i, (label_text, value) in enumerate(labels_data):
                label = QLabel(label_text)
                label.setFont(QFont("Arial", 8))
                label.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
                
                value_label = QLabel(value)
                value_label.setFont(QFont("Arial", 9, QFont.Bold))
                value_label.setAlignment(Qt.AlignRight)
                value_label.setStyleSheet("color: white;")
                
                row = i // 2
                col = (i % 2) * 2
                info_layout.addWidget(label, row, col)
                info_layout.addWidget(value_label, row, col + 1)
            
            info_widget = QWidget()
            info_widget.setLayout(info_layout)
            layout.addWidget(info_widget)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def setup_style(self):
        city_colors = {
            'Diyarbakır': ('rgba(231, 76, 60, 0.9)', 'rgba(192, 57, 43, 0.9)'),
            'Mardin': ('rgba(52, 152, 219, 0.9)', 'rgba(41, 128, 185, 0.9)'),
            'Siirt': ('rgba(241, 196, 15, 0.9)', 'rgba(243, 156, 18, 0.9)'),
            'Şırnak': ('rgba(26, 188, 156, 0.9)', 'rgba(22, 160, 133, 0.9)'),
            'Şanlıurfa': ('rgba(155, 89, 182, 0.9)', 'rgba(142, 68, 173, 0.9)'),
            'Batman': ('rgba(230, 126, 34, 0.9)', 'rgba(211, 84, 0, 0.9)')
        }
        
        color1, color2 = city_colors.get(self.city, ('rgba(149, 165, 166, 0.9)', 'rgba(127, 140, 141, 0.9)'))
        
        self.setStyleSheet(f"""
            ModernWeatherCard {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color1}, stop:1 {color2});
                border-radius: 15px;
                color: white;
                border: 2px solid rgba(0, 0, 0, 0.2);
            }}
            QLabel {{
                color: white;
                background: transparent;
            }}
        """)
    
    def setup_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)

class WeatherStatsWidget(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(30, 20, 30, 20)
        
        title = QLabel("Anlik Istatistikler")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: white; 
            margin-bottom: 8px;
            background: rgba(0, 0, 0, 0.3);
            padding: 8px;
            border-radius: 8px;
        """)
        layout.addWidget(title)
        
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(25)
        
        # İstatistikleri hesapla
        all_data = self.db.get_all_data()
        if all_data:
            df = pd.DataFrame(all_data, columns=[
                'id', 'city', 'date', 'hour', 'temperature', 'cloudiness',
                'wind_speed', 'humidity', 'pressure', 'weather_condition',
                'feels_like', 'uv_index', 'visibility', 'created_at'
            ])
            
            avg_temp = df['temperature'].mean()
            max_temp = df['temperature'].max()
            min_temp = df['temperature'].min()
            avg_humidity = df['humidity'].mean()
            avg_wind = df['wind_speed'].mean()
            
            stats_data = [
                ("Ort. Sicaklik", f"{avg_temp:.1f}°C", "#e74c3c"),
                ("En Yuksek", f"{max_temp:.1f}°C", "#c0392b"),
                ("En Dusuk", f"{min_temp:.1f}°C", "#3498db"),
                ("Ort. Nem", f"{avg_humidity:.1f}%", "#1abc9c"),
                ("Ort. Ruzgar", f"{avg_wind:.1f} km/h", "#9b59b6")
            ]
            
            for label_text, value, color in stats_data:
                stat_widget = QWidget()
                stat_layout = QVBoxLayout()
                stat_layout.setSpacing(4)
                stat_layout.setContentsMargins(15, 10, 15, 10)
                
                label = QLabel(label_text)
                label.setFont(QFont("Arial", 10, QFont.Bold))
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
                
                value_label = QLabel(value)
                value_label.setFont(QFont("Arial", 14, QFont.Bold))
                value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                value_label.setStyleSheet(f"color: {color}; background: rgba(255, 255, 255, 0.1); padding: 5px; border-radius: 5px;")
                
                stat_layout.addWidget(label)
                stat_layout.addWidget(value_label)
                stat_widget.setLayout(stat_layout)
                
                # Widget stili
                stat_widget.setStyleSheet(f"""
                    QWidget {{
                        background: rgba(255, 255, 255, 0.05);
                        border: 1px solid {color};
                        border-radius: 10px;
                        margin: 2px;
                    }}
                """)
                
                stats_layout.addWidget(stat_widget)
        
        layout.addLayout(stats_layout)
        self.setLayout(layout)

class AdvancedWeatherChart(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Chart türü seçimi
        chart_type_layout = QHBoxLayout()
        chart_type_label = QLabel("📈 Grafik Türü:")
        chart_type_label.setFont(QFont("Arial", 12, QFont.Bold))
        chart_type_layout.addWidget(chart_type_label)
        
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems([
            "Sıcaklık Karşılaştırması",
            "Nem Oranları",
            "Rüzgar Hızları", 
            "Günlük Trend"
        ])
        chart_type_layout.addWidget(self.chart_type_combo)
        
        update_btn = AnimatedButton("🔄 Güncelle")
        update_btn.clicked.connect(self.update_chart)
        chart_type_layout.addWidget(update_btn)
        
        chart_type_layout.addStretch()
        layout.addLayout(chart_type_layout)
        
        # Matplotlib figure
        self.figure = Figure(figsize=(12, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
        self.update_chart()
    
    def update_chart(self):
        self.figure.clear()
        
        data = self.db.get_all_data()
        if not data:
            return
        
        df = pd.DataFrame(data, columns=[
            'id', 'city', 'date', 'hour', 'temperature', 'cloudiness',
            'wind_speed', 'humidity', 'pressure', 'weather_condition',
            'feels_like', 'uv_index', 'visibility', 'created_at'
        ])
        
        chart_type = self.chart_type_combo.currentText()
        
        if chart_type == "Sıcaklık Karşılaştırması":
            self.plot_temperature_comparison(df)
        elif chart_type == "Nem Oranları":
            self.plot_humidity_chart(df)
        elif chart_type == "Rüzgar Hızları":
            self.plot_wind_speed_chart(df)
        elif chart_type == "Günlük Trend":
            self.plot_daily_trend(df)
        
        self.canvas.draw()
    
    def plot_temperature_comparison(self, df):
        ax = self.figure.add_subplot(111)
        ax.clear()
        
        cities = df['city'].unique()
        # Daha belirgin renkler
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3']
        
        for i, city in enumerate(cities):
            city_data = df[df['city'] == city].sort_values('hour')
            color = colors[i % len(colors)]
            
            # Çizgi kalınlığı ve stil
            ax.plot(city_data['hour'], city_data['temperature'], 
                   marker='o', label=city, color=color, linewidth=3,
                   markersize=6, markerfacecolor='white', markeredgecolor=color,
                   markeredgewidth=2)
        
        ax.set_xlabel('Saat', fontsize=12, fontweight='bold')
        ax.set_ylabel('Sicaklik (°C)', fontsize=12, fontweight='bold')
        ax.set_title('Saatlik Sicaklik Karsilastirmasi', fontsize=16, fontweight='bold', pad=20)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_facecolor('#f8f9fa')
        
        # X ekseni saatleri
        ax.set_xticks(range(0, 24, 3))
        ax.set_xticklabels([f'{h:02d}:00' for h in range(0, 24, 3)])
        
        plt.tight_layout()
    
    def plot_humidity_chart(self, df):
        ax = self.figure.add_subplot(111)
        ax.clear()
        
        city_humidity = df.groupby('city')['humidity'].mean().sort_values(ascending=False)
        
        # Gradient renkler
        colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
        
        bars = ax.bar(city_humidity.index, city_humidity.values, 
                     color=colors[:len(city_humidity)], alpha=0.8, width=0.6)
        
        # Değerleri bar üzerinde göster
        for bar, value in zip(bars, city_humidity.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                   f'{value:.1f}%', ha='center', va='bottom', 
                   fontweight='bold', fontsize=11)
        
        ax.set_ylabel('Nem Orani (%)', fontsize=12, fontweight='bold')
        ax.set_title('Sehirlere Gore Ortalama Nem Orani', fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.set_facecolor('#f8f9fa')
        
        # Y ekseni limitleri
        ax.set_ylim(0, max(city_humidity.values) * 1.15)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
    
    def plot_wind_speed_chart(self, df):
        ax = self.figure.add_subplot(111)
        ax.clear()
        
        city_wind = df.groupby('city')['wind_speed'].mean().sort_values(ascending=False)
        
        # Rüzgar için uygun renkler
        colors = ['#74b9ff', '#0984e3', '#00b894', '#00cec9', '#fdcb6e', '#e17055']
        
        bars = ax.bar(city_wind.index, city_wind.values, 
                     color=colors[:len(city_wind)], alpha=0.8, width=0.6)
        
        # Değerleri bar üzerinde göster
        for bar, value in zip(bars, city_wind.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                   f'{value:.1f}', ha='center', va='bottom', 
                   fontweight='bold', fontsize=11)
        
        ax.set_ylabel('Ruzgar Hizi (km/h)', fontsize=12, fontweight='bold')
        ax.set_title('Sehirlere Gore Ortalama Ruzgar Hizi', fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.set_facecolor('#f8f9fa')
        
        # Y ekseni limitleri
        ax.set_ylim(0, max(city_wind.values) * 1.15)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
    
    def plot_daily_trend(self, df):
        ax = self.figure.add_subplot(111)
        ax.clear()
        
        hourly_temp = df.groupby('hour')['temperature'].mean()
        hourly_humidity = df.groupby('hour')['humidity'].mean()
        
        ax2 = ax.twinx()
        
        # Sıcaklık çizgisi
        line1 = ax.plot(hourly_temp.index, hourly_temp.values, 
                       'o-', color='#e74c3c', label='Sicaklik', linewidth=3,
                       markersize=6, markerfacecolor='white', markeredgecolor='#e74c3c',
                       markeredgewidth=2)
        
        # Nem çizgisi
        line2 = ax2.plot(hourly_humidity.index, hourly_humidity.values, 
                        's-', color='#3498db', label='Nem', linewidth=3,
                        markersize=6, markerfacecolor='white', markeredgecolor='#3498db',
                        markeredgewidth=2)
        
        ax.set_xlabel('Saat', fontsize=12, fontweight='bold')
        ax.set_ylabel('Sicaklik (°C)', color='#e74c3c', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Nem (%)', color='#3498db', fontsize=12, fontweight='bold')
        
        ax.set_title('Gunluk Sicaklik ve Nem Trendi', fontsize=16, fontweight='bold', pad=20)
        
        # Grid ve stil
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_facecolor('#f8f9fa')
        
        # X ekseni saatleri
        ax.set_xticks(range(0, 24, 3))
        ax.set_xticklabels([f'{h:02d}:00' for h in range(0, 24, 3)])
        
        # Legend
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax.legend(lines, labels, loc='upper left', framealpha=0.8)
        
        plt.tight_layout()

class WeatherDataThread(QThread):
    data_updated = pyqtSignal(dict)
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.running = True
    
    def run(self):
        while self.running:
            try:
                cities_data = {}
                cities = ['Diyarbakır', 'Mardin', 'Siirt', 'Şırnak', 'Şanlıurfa', 'Batman']
                
                for city in cities:
                    data = self.db.get_city_data(city)
                    if data:
                        cities_data[city] = data
                
                self.data_updated.emit(cities_data)
                self.msleep(30000)  # 30 saniye bekle
                
            except Exception as e:
                print(f"Thread hatası: {e}")
                break
    
    def stop(self):
        self.running = False

class EnhancedWeatherDatabase:
    def __init__(self, db_name='weather_professional.db'):
        self.db_name = db_name
        self.init_database()
        self.load_sample_data()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            date TEXT NOT NULL,
            hour INTEGER NOT NULL,
            temperature REAL NOT NULL,
            cloudiness INTEGER NOT NULL,
            wind_speed REAL NOT NULL,
            humidity INTEGER NOT NULL,
            pressure REAL NOT NULL,
            weather_condition TEXT NOT NULL,
            feels_like REAL NOT NULL,
            uv_index INTEGER NOT NULL,
            visibility INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
        conn.close()
    
    def load_sample_data(self):
        cities = ['Diyarbakır', 'Mardin', 'Siirt', 'Şırnak', 'Şanlıurfa', 'Batman']
        weather_conditions = ['Güneşli', 'Bulutlu', 'Parçalı Bulutlu', 'Yağmurlu', 'Fırtınalı']
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('DELETE FROM weather')
        
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        for city in cities:
            base_temp = random.randint(20, 40)
            for hour in range(24):
                temp_variation = 5 * (1 + 0.5 * random.random()) * (1 if 6 <= hour <= 18 else 0.7)
                temperature = base_temp + temp_variation
                
                cloudiness = random.randint(0, 100)
                wind_speed = random.uniform(0, 30)
                humidity = random.randint(20, 90)
                pressure = random.uniform(995, 1025)
                weather_condition = random.choice(weather_conditions)
                feels_like = temperature + random.uniform(-3, 3)
                uv_index = random.randint(0, 11)
                visibility = random.randint(5, 25)
                
                c.execute('''INSERT INTO weather 
                    (city, date, hour, temperature, cloudiness, wind_speed, humidity, 
                     pressure, weather_condition, feels_like, uv_index, visibility)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (city, current_date, hour, temperature, cloudiness, wind_speed,
                     humidity, pressure, weather_condition, feels_like, uv_index, visibility))
        
        conn.commit()
        conn.close()
    
    def get_city_data(self, city):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''SELECT * FROM weather WHERE city = ? ORDER BY hour''', (city,))
        data = c.fetchall()
        conn.close()
        return data
    
    def get_all_data(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT * FROM weather ORDER BY city, hour')
        data = c.fetchall()
        conn.close()
        return data
    
    def get_weather_stats(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''SELECT city, 
                     AVG(temperature) as avg_temp,
                     MIN(temperature) as min_temp,
                     MAX(temperature) as max_temp,
                     AVG(humidity) as avg_humidity,
                     AVG(wind_speed) as avg_wind
                     FROM weather GROUP BY city''')
        data = c.fetchall()
        conn.close()
        return data

class ProfessionalWeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cities = ['Diyarbakır', 'Mardin', 'Siirt', 'Şırnak', 'Şanlıurfa', 'Batman']
        self.db = EnhancedWeatherDatabase()
        self.city_cards = {}
        self.setup_ui()
        self.setup_data_thread()
        self.setWindowTitle("Professional Weather Tracker Pro")
        self.setGeometry(100, 100, 1400, 900)
        self.setup_main_style()
    
    def setup_main_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2c3e50, stop:0.5 #34495e, stop:1 #2c3e50);
            }
            QTabWidget::pane {
                border: 2px solid #34495e;
                border-radius: 10px;
                background: rgba(44, 62, 80, 0.8);
            }
            QTabBar::tab {
                background: #34495e;
                color: white;
                padding: 12px 25px;
                margin: 2px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
                border: 1px solid #2c3e50;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
                border: 1px solid #2980b9;
            }
            QTabBar::tab:hover {
                background: #4a6741;
                color: white;
            }
        """)
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Başlık
        title_label = QLabel("Professional Weather Tracker Pro")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                background: rgba(0, 0, 0, 0.3);
                padding: 15px;
                border-radius: 10px;
                margin: 10px;
            }
        """)
        layout.addWidget(title_label)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Status bar
        status_widget = QWidget()
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel("Sistem hazır")
        self.status_label.setStyleSheet("""
            QLabel {
                color: white;
                background: rgba(0, 0, 0, 0.3);
                padding: 8px 15px;
                border-radius: 15px;
                font-weight: bold;
            }
        """)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        
        time_label = QLabel(datetime.now().strftime("Tarih: %d.%m.%Y | Saat: %H:%M"))
        time_label.setStyleSheet("""
            QLabel {
                color: white;
                background: rgba(0, 0, 0, 0.3);
                padding: 8px 15px;
                border-radius: 15px;
                font-weight: bold;
            }
        """)
        status_layout.addWidget(time_label)
        
        status_widget.setLayout(status_layout)
        layout.addWidget(status_widget)
        
        central_widget.setLayout(layout)
        
        # Tabları oluştur
        self.create_dashboard_tab()
        self.create_advanced_charts_tab()
        self.create_detailed_tab()
        self.create_historical_tab()
        self.create_analytics_tab()
        self.create_settings_tab()
    
    def create_dashboard_tab(self):
        dashboard_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Üst panel - İstatistikler (sabit yükseklik)
        stats_widget = WeatherStatsWidget(self.db)
        stats_widget.setFixedHeight(120)
        stats_widget.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                margin: 5px;
            }
        """)
        main_layout.addWidget(stats_widget)
        
        # Şehir kartları için grid layout (scroll olmadan)
        cards_widget = QWidget()
        cards_layout = QGridLayout()
        cards_layout.setSpacing(15)
        cards_layout.setContentsMargins(10, 10, 10, 10)
        
        # Kartları 2x3 düzeninde yerleştir
        for i, city in enumerate(self.cities):
            city_data = self.db.get_city_data(city)
            card = ModernWeatherCard(city, city_data)
            card.setFixedSize(280, 200)  # Sabit boyut
            self.city_cards[city] = card
            
            row = i // 3
            col = i % 3
            cards_layout.addWidget(card, row, col)
        
        cards_widget.setLayout(cards_layout)
        main_layout.addWidget(cards_widget, 1)  # Esnek alan
        
        # Alt panel - Hızlı işlemler
        actions_widget = QWidget()
        actions_widget.setFixedHeight(60)
        actions_layout = QHBoxLayout()
        actions_layout.setContentsMargins(20, 10, 20, 10)
        
        refresh_btn = AnimatedButton("Verileri Yenile")
        refresh_btn.setFixedSize(150, 40)
        refresh_btn.clicked.connect(self.refresh_all_data)
        actions_layout.addWidget(refresh_btn)
        
        export_btn = AnimatedButton("Excel'e Aktar")
        export_btn.setFixedSize(150, 40)
        export_btn.clicked.connect(self.export_to_excel)
        actions_layout.addWidget(export_btn)
        
        actions_layout.addStretch()
        actions_widget.setLayout(actions_layout)
        main_layout.addWidget(actions_widget)
        
        dashboard_widget.setLayout(main_layout)
        self.tab_widget.addTab(dashboard_widget, "Ana Panel")
    
    def create_advanced_charts_tab(self):
        charts_widget = AdvancedWeatherChart(self.db)
        self.tab_widget.addTab(charts_widget, "Gelismis Grafikler")
    
    def create_settings_tab(self):
        settings_widget = QWidget()
        layout = QVBoxLayout()
        
        settings_group = QGroupBox("⚙️ Uygulama Ayarları")
        settings_layout = QVBoxLayout()
        
        # Gerçek zamanlı güncelleme
        self.realtime_checkbox = QCheckBox("🔄 Gerçek zamanlı veri güncellemesi (30 saniye)")
        self.realtime_checkbox.setChecked(True)
        self.realtime_checkbox.stateChanged.connect(self.setup_data_thread)
        settings_layout.addWidget(self.realtime_checkbox)
        
        # Tema seçimi
        theme_layout = QHBoxLayout()
        theme_label = QLabel("🎨 Tema:")
        theme_layout.addWidget(theme_label)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Profesyonel Gradyan", "Klasik Mavi", "Gece Teması"])
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        
        settings_layout.addLayout(theme_layout)
        
        # Bildirim ayarları
        notification_group = QGroupBox("🔔 Bildirim Ayarları")
        notification_layout = QVBoxLayout()
        
        self.temp_alert_checkbox = QCheckBox("🌡️ Aşırı sıcaklık uyarısı (35°C üstü)")
        notification_layout.addWidget(self.temp_alert_checkbox)
        
        self.wind_alert_checkbox = QCheckBox("💨 Yüksek rüzgar uyarısı (20 km/h üstü)")
        notification_layout.addWidget(self.wind_alert_checkbox)
        
        notification_group.setLayout(notification_layout)
        settings_layout.addWidget(notification_group)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        layout.addStretch()
        
        settings_widget.setLayout(layout)
        self.tab_widget.addTab(settings_widget, "Ayarlar")
    
    def setup_data_thread(self):
        if hasattr(self, 'data_thread'):
            self.data_thread.stop()
            self.data_thread.wait()
        
        self.data_thread = WeatherDataThread(self.db)
        self.data_thread.data_updated.connect(self.update_dashboard)
        
        if self.realtime_checkbox.isChecked():
            self.data_thread.start()
    
    def update_dashboard(self, cities_data):
        for city, card in self.city_cards.items():
            if city in cities_data:
                new_card = ModernWeatherCard(city, cities_data[city])
        
        # Sıcaklık uyarıları kontrol et
        self.check_temperature_alerts(cities_data)
        
        self.status_label.setText(f"Veriler guncellendi - {datetime.now().strftime('%H:%M:%S')}")
    
    def check_temperature_alerts(self, cities_data):
        """Aşırı sıcaklık uyarılarını kontrol et"""
        if hasattr(self, 'temp_alert_checkbox') and self.temp_alert_checkbox.isChecked():
            for city, data in cities_data.items():
                if data and len(data) > 0:
                    temp = data[0][4]  # temperature
                    if temp > 35:
                        self.show_temperature_alert(city, temp)
    
    def show_temperature_alert(self, city, temperature):
        """Sıcaklık uyarısı göster"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Asiri Sicaklik Uyarisi")
        msg.setText(f"{city} sehrinde asiri sicaklik!")
        msg.setInformativeText(f"Mevcut sicaklik: {temperature:.1f}°C\nDikkatli olun!")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2c3e50;
                color: white;
            }
            QMessageBox QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        msg.exec()
    
    def refresh_all_data(self):
        self.db.load_sample_data()
        current_tab = self.tab_widget.currentIndex()
        self.tab_widget.clear()
        
        self.create_dashboard_tab()
        self.create_advanced_charts_tab()
        self.create_detailed_tab()
        self.create_historical_tab()
        self.create_analytics_tab()
        self.create_settings_tab()
        
        self.tab_widget.setCurrentIndex(current_tab)
        self.status_label.setText("Tum veriler yenilendi")
    
    def export_to_excel(self):
        try:
            path, _ = QFileDialog.getSaveFileName(
                self, 'Excel olarak kaydet', 
                f'weatherpro_export_{datetime.now().strftime("%Y%m%d_%H%M")}.xlsx', 
                'Excel Files (*.xlsx)'
            )
            if path:
                all_data = self.db.get_all_data()
                df = pd.DataFrame(all_data, columns=[
                    'ID', 'Şehir', 'Tarih', 'Saat', 'Sıcaklık', 'Bulutlanma', 
                    'Rüzgar Hızı', 'Nem', 'Basınç', 'Hava Durumu', 'Hissedilen',
                    'UV İndeksi', 'Görüş Mesafesi', 'Oluşturma Zamanı'
                ])
                
                with pd.ExcelWriter(path, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Tüm Veriler', index=False)
                    
                    for city in self.cities:
                        city_df = df[df['Şehir'] == city]
                        city_df.to_excel(writer, sheet_name=city, index=False)
                
                self.status_label.setText(f"Veriler basariyla aktarildi: {path}")
        except Exception as e:
            self.status_label.setText(f"Hata: {str(e)}")
    
    def create_detailed_tab(self):
        detailed_widget = QWidget()
        layout = QVBoxLayout()
        
        # Şehir seçimi
        city_layout = QHBoxLayout()
        city_select_label = QLabel("Sehir Secin:")
        city_select_label.setFont(QFont("Arial", 12, QFont.Bold))
        city_select_label.setStyleSheet("color: white;")
        city_layout.addWidget(city_select_label)
        
        self.city_combo = QComboBox()
        self.city_combo.addItems(self.cities)
        self.city_combo.setFont(QFont("Arial", 11))
        self.city_combo.setStyleSheet("""
            QComboBox {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                padding: 5px;
                min-width: 150px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
        """)
        self.city_combo.currentTextChanged.connect(self.load_detailed_data)
        city_layout.addWidget(self.city_combo)
        city_layout.addStretch()
        
        layout.addLayout(city_layout)
        
        # Detaylı tablo
        self.detailed_table = QTableWidget()
        self.detailed_table.setStyleSheet("""
            QTableWidget {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                gridline-color: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 5px;
            }
            QHeaderView::section {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                font-weight: bold;
                border: none;
                padding: 8px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        layout.addWidget(self.detailed_table)
        
        detailed_widget.setLayout(layout)
        self.tab_widget.addTab(detailed_widget, "Detayli Gorunum")
        
        # İlk yükleme
        self.load_detailed_data()
    
    def load_detailed_data(self):
        """Seçilen şehir için detaylı verileri yükle"""
        try:
            selected_city = self.city_combo.currentText()
            city_data = self.db.get_city_data(selected_city)
            
            if city_data:
                # Tablo başlıklarını ayarla
                headers = ['Saat', 'Sicaklik', 'Hissedilen', 'Nem', 'Ruzgar', 'Bulut', 'Basinc', 'UV', 'Gorunurluk', 'Hava Durumu']
                self.detailed_table.setColumnCount(len(headers))
                self.detailed_table.setHorizontalHeaderLabels(headers)
                
                # Verileri formatla
                formatted_data = []
                for row in city_data:
                    formatted_data.append([
                        f"{row[3]:02d}:00",  # hour
                        f"{row[4]:.1f}°C",  # temperature
                        f"{row[10]:.1f}°C",  # feels_like
                        f"{row[7]}%",  # humidity
                        f"{row[6]:.1f} km/h",  # wind_speed
                        f"{row[5]}%",  # cloudiness
                        f"{row[8]:.1f} hPa",  # pressure
                        f"{row[11]}",  # uv_index
                        f"{row[12]} km",  # visibility
                        row[9]  # weather_condition
                    ])
                
                # Tabloyu doldur
                self.detailed_table.setRowCount(len(formatted_data))
                
                for row_idx, row_data in enumerate(formatted_data):
                    for col_idx, value in enumerate(row_data):
                        item = QTableWidgetItem(str(value))
                        item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                        self.detailed_table.setItem(row_idx, col_idx, item)
                
                # Sütun genişliklerini ayarla
                self.detailed_table.resizeColumnsToContents()
                
        except Exception as e:
            print(f"Detaylı veri yükleme hatası: {e}")
    
    def create_historical_tab(self):
        historical_widget = QWidget()
        layout = QVBoxLayout()
        
        # Tarih arama paneli
        date_panel = QGroupBox("Tarihsel Veri Arama")
        date_layout = QHBoxLayout()
        
        start_date_label = QLabel("Baslangic:")
        start_date_label.setStyleSheet("color: white; font-weight: bold;")
        date_layout.addWidget(start_date_label)
        
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate().addDays(-7))
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setStyleSheet("""
            QDateEdit {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                padding: 5px;
            }
        """)
        date_layout.addWidget(self.start_date_edit)
        
        end_date_label = QLabel("Bitis:")
        end_date_label.setStyleSheet("color: white; font-weight: bold;")
        date_layout.addWidget(end_date_label)
        
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDate(QDate.currentDate())
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setStyleSheet("""
            QDateEdit {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                padding: 5px;
            }
        """)
        date_layout.addWidget(self.end_date_edit)
        
        search_btn = AnimatedButton("Ara")
        search_btn.clicked.connect(self.load_historical_data)
        date_layout.addWidget(search_btn)
        
        date_layout.addStretch()
        date_panel.setLayout(date_layout)
        date_panel.setStyleSheet("""
            QGroupBox {
                color: white;
                font-weight: bold;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        layout.addWidget(date_panel)
        
        # Tarihsel veriler tablosu
        self.historical_table = QTableWidget()
        self.historical_table.setStyleSheet("""
            QTableWidget {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                gridline-color: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 5px;
            }
            QHeaderView::section {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                font-weight: bold;
                border: none;
                padding: 8px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        layout.addWidget(self.historical_table)
        
        historical_widget.setLayout(layout)
        self.tab_widget.addTab(historical_widget, "Tarihsel Veriler")
        
        # İlk yükleme
        self.load_historical_data()
    
    def load_historical_data(self):
        """Tarihsel verileri yükle"""
        try:
            all_data = self.db.get_all_data()
            
            if all_data:
                # Tablo başlıklarını ayarla
                headers = ['Sehir', 'Tarih', 'Saat', 'Sicaklik', 'Nem', 'Ruzgar', 'Bulut', 'Hava Durumu']
                self.historical_table.setColumnCount(len(headers))
                self.historical_table.setHorizontalHeaderLabels(headers)
                
                # Verileri filtrele ve sırala
                filtered_data = []
                for row in all_data:
                    filtered_data.append([
                        row[1],  # city
                        row[2],  # date
                        f"{row[3]:02d}:00",  # hour
                        f"{row[4]:.1f}°C",  # temperature
                        f"{row[7]}%",  # humidity
                        f"{row[6]:.1f} km/h",  # wind_speed
                        f"{row[5]}%",  # cloudiness
                        row[9]  # weather_condition
                    ])
                
                # Tabloyu doldur
                self.historical_table.setRowCount(len(filtered_data))
                
                for row_idx, row_data in enumerate(filtered_data):
                    for col_idx, value in enumerate(row_data):
                        item = QTableWidgetItem(str(value))
                        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Salt okunur
                        self.historical_table.setItem(row_idx, col_idx, item)
                
                # Sütun genişliklerini ayarla
                self.historical_table.resizeColumnsToContents()
                
        except Exception as e:
            print(f"Tarihsel veri yükleme hatası: {e}")
    
    def create_analytics_tab(self):
        analytics_widget = QWidget()
        layout = QVBoxLayout()
        
        stats_table = QTableWidget()
        stats_data = self.db.get_weather_stats()
        
        if stats_data:
            stats_table.setRowCount(len(stats_data))
            stats_table.setColumnCount(6)
            stats_table.setHorizontalHeaderLabels([
                '🏙️ Şehir', '🌡️ Ortalama Sıcaklık', '❄️ Min Sıcaklık', 
                '🔥 Max Sıcaklık', '💧 Ortalama Nem', '💨 Ortalama Rüzgar'
            ])
            
            for i, row in enumerate(stats_data):
                stats_table.setItem(i, 0, QTableWidgetItem(row[0]))
                stats_table.setItem(i, 1, QTableWidgetItem(f"{row[1]:.1f}°C"))
                stats_table.setItem(i, 2, QTableWidgetItem(f"{row[2]:.1f}°C"))
                stats_table.setItem(i, 3, QTableWidgetItem(f"{row[3]:.1f}°C"))
                stats_table.setItem(i, 4, QTableWidgetItem(f"{row[4]:.1f}%"))
                stats_table.setItem(i, 5, QTableWidgetItem(f"{row[5]:.1f} km/h"))
            
            stats_table.resizeColumnsToContents()
        
        layout.addWidget(stats_table)
        analytics_widget.setLayout(layout)
        self.tab_widget.addTab(analytics_widget, "Analitik")
    
    def closeEvent(self, event):
        if hasattr(self, 'data_thread'):
            self.data_thread.stop()
            self.data_thread.wait()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Uygulama ikonu ve stili
    app.setStyle('Fusion')
    
    window = ProfessionalWeatherApp()
    window.show()
    
    sys.exit(app.exec_())
