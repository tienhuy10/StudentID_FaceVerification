import sqlite3

# Kết nối đến SQLite
conn = sqlite3.connect('students.db')
c = conn.cursor()

# Tạo bảng sinh viên
c.execute('''CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT,
                class_id INTEGER,
                subject TEXT
            )''')

# Tạo bảng lưu ca thi
c.execute('''CREATE TABLE IF NOT EXISTS exam_sessions (
                session_id INTEGER PRIMARY KEY,
                class_id INTEGER,
                exam_date DATE,
                start_time TIME,
                end_time TIME
            )''')

# Bảng chi tiết ca thi
c.execute('''CREATE TABLE IF NOT EXISTS exam_session_details (
                session_id INTEGER,
                student_id INTEGER,
                FOREIGN KEY(session_id) REFERENCES exam_sessions(session_id),
                FOREIGN KEY(student_id) REFERENCES students(student_id)
            )''')

conn.commit()
conn.close()
