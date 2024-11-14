import sqlite3

def init_db():
    conn = sqlite3.connect('db/students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            student_id TEXT,
            birthdate TEXT
        )
    ''')
    conn.commit()
    conn.close()
