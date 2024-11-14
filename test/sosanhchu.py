from unidecode import unidecode

def normalize_name(name):
    return unidecode(name.strip().upper())

# Tên trong cơ sở dữ liệu
db_name = "Phạm thùy linhj"
# Tên đã trích xuất
extracted_name = "PHAM THUY LINH"

# Chuẩn hóa và so sánh
if normalize_name(db_name) == normalize_name(extracted_name):
    print("Tên trùng khớp")
else:
    print("Tên không trùng khớp")
