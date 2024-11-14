# extract_info.py

from paddleocr import PaddleOCR
import re
import cv2

# Khởi tạo PaddleOCR với hỗ trợ tiếng Việt
ocr = PaddleOCR(use_angle_cls=True, ocr_version='PP-OCRv4', use_space_char=True)

def extract_student_info(cropped_image_path):
    # Đọc ảnh đã cắt
    image = cv2.imread(cropped_image_path)
    if image is None:
        print(f"Lỗi: Không thể đọc ảnh từ đường dẫn '{cropped_image_path}'")
        return None

    # Chuyển ảnh sang grayscale và làm nét để tăng độ chi tiết
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sharp_image = cv2.GaussianBlur(gray_image, (0, 0), sigmaX=3)
    sharp_image = cv2.addWeighted(gray_image, 1.5, sharp_image, -0.5, 0)

    # Sử dụng OCR để trích xuất văn bản
    result = ocr.ocr(sharp_image, cls=True)

    # Sắp xếp các box theo trục y
    sorted_result = sorted(result[0], key=lambda x: x[0][0][1])

    # Khởi tạo từ điển để lưu thông tin
    fields = {
        "Tên": "",
        "Ngành": "",
        "Trường": "",
        "Khóa": "",
        "MSV": ""
    }

    next_line_is_name = False
    next_line_is_major = False
    next_line_is_faculty = False

    for line in sorted_result:
        text = line[1][0].strip()

        # Tìm tên sau "THE SINH VIEN"
        if "THE SINH VIEN" in text.upper():
            next_line_is_name = True
            continue
        if next_line_is_name:
            fields["Tên"] = text
            next_line_is_name = False
            next_line_is_major = True
            continue

        if next_line_is_major:
            # Loại bỏ từ "Ngành" hoặc bất kỳ ký tự biến thể nào của từ này (ví dụ "Ngänh")
            text = re.sub(r"Ng[aáäàâ]nh:", "", text).strip()  # Thay thế tất cả biến thể của "Ngành"
            fields["Ngành"] = text
            next_line_is_major = False
            next_line_is_faculty = True
            continue
        if next_line_is_faculty:
            fields["Trường"] = text
            next_line_is_faculty = False
            continue

        # Tìm khóa học nếu có từ "Khóa" hoặc một chuỗi chứa năm học
        if re.search(r"\d{4}-\d{4}", text):
            fields["Khóa"] = text

        # Tìm mã sinh viên (MSV) với từ khóa "MSV" hoặc một chuỗi số dài
        if "MSV" in text.upper():
            msv_match = re.search(r"\d{9,}", text)
            if msv_match:
                fields["MSV"] = msv_match.group(0)

    return fields
