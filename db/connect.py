import sqlite3

DB_NAME = "daily_log.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        tag TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )                                 
''')
    
    conn.commit()
    conn.close()