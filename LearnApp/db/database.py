import sqlite3
import os

class Database:
    def __init__(self):
        db_dir = os.path.join(os.path.dirname(__file__))
        self.db_path = os.path.join(db_dir, 'quizapp.db')
        self.create_tables()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def create_tables(self):
        conn = self.get_connection()
        c = conn.cursor()
        
        # Kullanıcılar tablosu
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Karşılaşmalar tablosu
        c.execute('''CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user1_id INTEGER,
            user2_id INTEGER,
            user1_score INTEGER DEFAULT 0,
            user2_score INTEGER DEFAULT 0,
            topic TEXT,
            level TEXT,
            question_count INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user1_id) REFERENCES users(id),
            FOREIGN KEY(user2_id) REFERENCES users(id)
        )''')
        
        # Sorular tablosu (geçmiş sorular için)
        c.execute('''CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER,
            question_text TEXT,
            option_a TEXT,
            option_b TEXT,
            option_c TEXT,
            option_d TEXT,
            correct_answer TEXT,
            FOREIGN KEY(match_id) REFERENCES matches(id)
        )''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, nickname):
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (nickname) VALUES (?)", (nickname,))
            user_id = c.lastrowid
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def get_user_by_nickname(self, nickname):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE nickname = ?", (nickname,))
        user = c.fetchone()
        conn.close()
        return user
    
    def get_all_users(self):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users ORDER BY nickname")
        users = c.fetchall()
        conn.close()
        return users
    
    def create_match(self, user1_id, user2_id, topic, level, question_count):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("""INSERT INTO matches (user1_id, user2_id, topic, level, question_count) 
                     VALUES (?, ?, ?, ?, ?)""", 
                 (user1_id, user2_id, topic, level, question_count))
        match_id = c.lastrowid
        conn.commit()
        conn.close()
        return match_id
    
    def update_match_scores(self, match_id, user1_score, user2_score):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("UPDATE matches SET user1_score = ?, user2_score = ? WHERE id = ?",
                 (user1_score, user2_score, match_id))
        conn.commit()
        conn.close()
    
    def get_match_history(self):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("""SELECT m.*, u1.nickname as user1_name, u2.nickname as user2_name 
                     FROM matches m 
                     JOIN users u1 ON m.user1_id = u1.id 
                     JOIN users u2 ON m.user2_id = u2.id 
                     ORDER BY m.created_at DESC""")
        matches = c.fetchall()
        conn.close()
        return matches

if __name__ == "__main__":
    db = Database()
