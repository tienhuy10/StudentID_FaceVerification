from deepface import DeepFace
import matplotlib.pyplot as plt

# Phát hiện khuôn mặt đầu tiên và loại bỏ chiều batch
detected_face_1 = DeepFace.detectFace(img_path="D:\\DoAnTN\\Project\\test\\NgocAnh_face.jpg")[0]
plt.imshow(detected_face_1)
plt.show()

# Phát hiện khuôn mặt thứ hai và loại bỏ chiều batch
detected_face_2 = DeepFace.detectFace(img_path="D:\\DoAnTN\\Project\\test\\NgocAnhIDCard.jpg")[0]
plt.imshow(detected_face_2)
plt.show()

result = DeepFace.verify(img1_path = "D:\\DoAnTN\\Project\\test\\NgocAnh_face.jpg", img2_path = "D:\\DoAnTN\\Project\\test\\NgocAnhIDCard.jpg", model_name = "Facenet")
print(result)

