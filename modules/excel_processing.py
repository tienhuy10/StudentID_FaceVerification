import sqlite3
import pandas as pd
from unidecode import unidecode

def process_excel_and_save_to_db(filepath):
    # Đọc dữ liệu từ file Excel
    df = pd.read_excel(filepath)
    selected_data = df.iloc[5:, 1:5]
    selected_data.columns = ['Họ', 'Tên', 'Mã sinh viên', 'Ngày sinh']
    selected_data['Họ và Tên'] = selected_data['Họ'] + ' ' + selected_data['Tên']
    
    # Loại bỏ các hàng có giá trị thiếu
    selected_data = selected_data.dropna(subset=['Họ', 'Tên', 'Mã sinh viên', 'Ngày sinh'])
    
    # Chuyển thông tin thành không dấu và in hoa
    selected_data['Họ và Tên'] = selected_data['Họ và Tên'].apply(lambda x: unidecode(x).upper())
    selected_data['Mã sinh viên'] = selected_data['Mã sinh viên'].apply(lambda x: unidecode(str(x)).upper())
    
    # Kết nối tới cơ sở dữ liệu và chèn dữ liệu
    conn = sqlite3.connect('db/students.db')
    cursor = conn.cursor()
    for _, row in selected_data.iterrows():
        cursor.execute(''' 
            INSERT INTO students (full_name, student_id, birthdate)
            VALUES (?, ?, ?)
        ''', (row['Họ và Tên'], row['Mã sinh viên'], row['Ngày sinh']))
    
    conn.commit()
    conn.close()
