# db_utils.py
import sqlite3

def init_db(db_name='conversation_history.db'):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_input TEXT,
                    ai_response TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                 )''')
    conn.commit()
    conn.close()

def save_conversation_to_db(user_input, ai_response):
    conn = sqlite3.connect('conversation_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO history (user_input, ai_response) VALUES (?, ?)", 
              (user_input, ai_response))
    conn.commit()
    conn.close()
