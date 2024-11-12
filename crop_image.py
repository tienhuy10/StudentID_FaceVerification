# crop_image.py

import cv2
import numpy as np

def crop_image(input_path, output_path):
    # Load image
    img = cv2.imread(input_path)
    if img is None:
        print(f"Lỗi: Không thể đọc ảnh từ đường dẫn '{input_path}'")
        return None  # Trả về None nếu không đọc được ảnh

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

    # Apply Otsu's threshold
    _, thresh_gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(thresh_gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Find object with the biggest bounding box
    mx = (0, 0, 0, 0)  # Biggest bounding box so far
    mx_area = 0
    for cont in contours:
        x, y, w, h = cv2.boundingRect(cont)
        area = w * h
        if area > mx_area:
            mx = x, y, w, h
            mx_area = area
    x, y, w, h = mx

    # Crop and save
    roi = img[y:y+h, x:x+w]
    cv2.imwrite(output_path, roi)
    return output_path if cv2.imread(output_path) is not None else None
