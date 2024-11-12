import os
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from crop_image import crop_image
from extract_info import extract_student_info

app = Flask(__name__)
app.secret_key = 'some_secret_key'
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Khởi tạo cơ sở dữ liệu
def init_db():
    conn = sqlite3.connect('student_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            major TEXT,
            school TEXT,
            course TEXT,
            student_id TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Hàm lưu dữ liệu vào cơ sở dữ liệu
def save_to_db(student_info):
    conn = sqlite3.connect('student_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (name, major, school, course, student_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        student_info.get("Tên", ""),
        student_info.get("Ngành", ""),
        student_info.get("Trường", ""),
        student_info.get("Khóa", ""),
        student_info.get("MSV", "")
    ))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Không có tệp nào được tải lên", 400

        file = request.files['file']
        if file.filename == '':
            return "Không có tệp nào được chọn", 400

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            cropped_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'cropped_' + file.filename)
            crop_image(file_path, cropped_image_path)
            student_info = extract_student_info(cropped_image_path)
            return render_template('index.html', original_image=file_path, cropped_image=cropped_image_path, student_info=student_info)
    
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    student_info = request.form.to_dict()
    save_to_db(student_info)
    flash("Thông tin sinh viên đã được lưu vào cơ sở dữ liệu.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
