import os
import sqlite3
import pandas as pd
from flask import Flask, request, redirect, url_for, render_template, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Tạo cơ sở dữ liệu SQLite và bảng nếu chưa tồn tại
def init_db():
    conn = sqlite3.connect('students.db')
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

init_db()

# Trang chủ để chọn file Excel
@app.route('/')
def index():
    return render_template('upload.html')

# Xử lý file tải lên và thêm dữ liệu vào cơ sở dữ liệu
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Đọc dữ liệu từ file Excel
        df = pd.read_excel(filepath)
        selected_data = df.iloc[5:, 1:5]
        selected_data.columns = ['Họ', 'Tên', 'Mã sinh viên', 'Ngày sinh']
        selected_data['Họ và Tên'] = selected_data['Họ'] + ' ' + selected_data['Tên']
        
        # Loại bỏ các hàng có giá trị thiếu trong các cột 'Họ', 'Tên', 'Mã sinh viên', và 'Ngày sinh'
        selected_data = selected_data.dropna(subset=['Họ', 'Tên', 'Mã sinh viên', 'Ngày sinh'])
        
        # Kết nối tới cơ sở dữ liệu và chèn dữ liệu
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        for _, row in selected_data.iterrows():
            cursor.execute('''
                INSERT INTO students (full_name, student_id, birthdate)
                VALUES (?, ?, ?)
            ''', (row['Họ và Tên'], row['Mã sinh viên'], row['Ngày sinh']))
        
        conn.commit()
        conn.close()
        
        flash('Dữ liệu đã được thêm vào cơ sở dữ liệu thành công!')
        return redirect(url_for('index'))


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
