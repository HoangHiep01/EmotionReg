from PIL import Image
import cv2
import face_detection
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

src_img = "../images/test2.jpg"

# khởi tạo "model"
detector = face_detection.build_detector("DSFDDetector", confidence_threshold=.5, nms_iou_threshold=.3)
# đọc ảnh với tên được điền
img = cv2.imread(src_img)
# nhận diện gương mặt trong ảnh
detections = detector.detect(img)

# giá trị tọa độ xác định được khuôn mặt và độ chính xác
# print (detections) 

x_start = round(detections[0][0])
y_start = round(detections[0][1])
x_end   = round(detections[0][2])
y_end   = round(detections[0][3])


crop_img = Image.open(src_img).convert('L')
crop_img = crop_img.crop((x_start, y_start, x_end, y_end))
plt.imshow(crop_img)

basewidth = 48
resize_img = crop_img
hsize = 48
resize_img = resize_img.resize((basewidth,hsize), Image.ANTIALIAS)
plt.imshow(resize_img)


new_model = tf.keras.models.load_model('../Model/EmotionRecogntion_v16.h5')

test_img = resize_img
test_img = np.reshape(test_img,(48,48))


label_dict = {0:'Angry',1:'Disgust',2:'Fear',3:'Happy',4:'Sad',5:'Surprise',6:'Neutral'}

test_img = np.expand_dims(test_img,axis = 0)
test_img = test_img.reshape(1,48,48,1)
# test_img = cv2.resize(test_img,(48,48),3)
result = new_model.predict(test_img)
# print (result)
result = list(result[0])

img_index = result.index(max(result))

plt.imshow(Image.open(src_img))
print("Emotion: ", label_dict[img_index])
