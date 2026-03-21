import sqlite3
import os
import datetime

class EmotionMusicDatabase:
    def __init__(self, db_path='emotion_music.db'):
        """Initialize the database connection"""
        self.db_path = db_path
        self.conn = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Connect to the SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            print(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
    
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        try:
            cursor = self.conn.cursor()
            
            # Table to store detected emotions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS emotions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    emotion_name TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table to store song recommendations
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recommendations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    emotion_id INTEGER,
                    song_name TEXT NOT NULL,
                    artist TEXT NOT NULL,
                    spotify_url TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (emotion_id) REFERENCES emotions (id)
                )
            ''')
            
            # Table to store user sessions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_start DATETIME DEFAULT CURRENT_TIMESTAMP,
                    session_end DATETIME,
                    emotion_count INTEGER DEFAULT 0
                )
            ''')
            
            self.conn.commit()
            cursor.close()
            print("Database tables created successfully")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
    
    def log_emotion(self, emotion_name):
        """Log a detected emotion"""
        try:
            # Create a new cursor for this operation
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO emotions (emotion_name) VALUES (?)",
                (emotion_name,)
            )
            self.conn.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
        except sqlite3.Error as e:
            print(f"Error logging emotion: {e}")
            return None
    
    def log_recommendation(self, emotion_id, song_name, artist, spotify_url):
        """Log a song recommendation"""
        try:
            # Create a new cursor for this operation
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO recommendations (emotion_id, song_name, artist, spotify_url) VALUES (?, ?, ?, ?)",
                (emotion_id, song_name, artist, spotify_url)
            )
            self.conn.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
        except sqlite3.Error as e:
            print(f"Error logging recommendation: {e}")
            return None
    
    def start_session(self):
        """Start a new user session"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO sessions DEFAULT VALUES")
            self.conn.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
        except sqlite3.Error as e:
            print(f"Error starting session: {e}")
            return None
    
    def end_session(self, session_id):
        """End a user session"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE sessions SET session_end = CURRENT_TIMESTAMP WHERE id = ?",
                (session_id,)
            )
            self.conn.commit()
            cursor.close()
        except sqlite3.Error as e:
            print(f"Error ending session: {e}")
    
    def increment_emotion_count(self, session_id):
        """Increment the emotion count for a session"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE sessions SET emotion_count = emotion_count + 1 WHERE id = ?",
                (session_id,)
            )
            self.conn.commit()
            cursor.close()
        except sqlite3.Error as e:
            print(f"Error incrementing emotion count: {e}")
    
    def get_emotion_history(self, limit=10):
        """Get recent emotion history"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT emotion_name, timestamp FROM emotions ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
            result = cursor.fetchall()
            cursor.close()
            return result
        except sqlite3.Error as e:
            print(f"Error getting emotion history: {e}")
            return []
    
    def get_recommendation_history(self, limit=10):
        """Get recent recommendation history"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """SELECT e.emotion_name, r.song_name, r.artist, r.spotify_url, r.timestamp 
                   FROM recommendations r 
                   JOIN emotions e ON r.emotion_id = e.id 
                   ORDER BY r.timestamp DESC LIMIT ?""",
                (limit,)
            )
            result = cursor.fetchall()
            cursor.close()
            return result
        except sqlite3.Error as e:
            print(f"Error getting recommendation history: {e}")
            return []
    
    def get_emotion_stats(self):
        """Get statistics on emotions detected"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """SELECT emotion_name, COUNT(*) as count 
                   FROM emotions 
                   GROUP BY emotion_name 
                   ORDER BY count DESC"""
            )
            result = cursor.fetchall()
            cursor.close()
            return result
        except sqlite3.Error as e:
            print(f"Error getting emotion stats: {e}")
            return []
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")