from flask import Flask, render_template, request, redirect, url_for, flash
import os
from modules.crop_image import crop_image
from modules.extract_info import extract_student_info
from modules.excel_processing import process_excel_and_save_to_db
from db.init_db import init_db
import sqlite3
from unidecode import unidecode

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Khởi tạo cơ sở dữ liệu
init_db()

def normalize_string(s):
    """Chuẩn hóa chuỗi: chuyển về chữ hoa và bỏ dấu"""
    return unidecode(s.strip().upper())  # Chuyển thành chữ hoa và loại bỏ dấu

def check_student_in_db(name, msv):
    conn = sqlite3.connect('db/students.db')  # Thay 'path_to_your_database.db' bằng đường dẫn chính xác
    cursor = conn.cursor()
    
    # Truy vấn để kiểm tra thông tin sinh viên trong database
    cursor.execute("SELECT * FROM students WHERE full_name = ? AND student_id = ?", (name, msv))
    result = cursor.fetchone()
    
    conn.close()
    return result is not None

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

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('upload'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('upload'))
        
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            process_excel_and_save_to_db(filepath)
            flash('Dữ liệu đã được thêm vào cơ sở dữ liệu thành công!')
            return redirect(url_for('upload'))
    
    return render_template('upload.html')

# Bổ sung route save để lưu thông tin sinh viên
@app.route('/save', methods=['POST'])
def save():
    student_info = {key: request.form[key] for key in request.form}
    name = student_info.get("Tên")
    msv = student_info.get("MSV")
    
    # Kiểm tra xem sinh viên có tồn tại trong database không
    if check_student_in_db(name, msv):
        flash("Thông tin sinh viên trùng khớp với dữ liệu trong cơ sở dữ liệu!")
    else:
        flash("Thông tin sinh viên KHÔNG trùng khớp trong cơ sở dữ liệu!")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
