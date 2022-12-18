import cv2
import face_detection
import tensorflow as tf
import numpy as np
from PIL import Image
from numpy.ma.core import reshape

class emotion:

	def __init__(self):
		self.src_img = ""
		self.model = tf.keras.models.load_model('../Model/EmotionRecogntion_v16.h5')
		self.detector = face_detection.build_detector("DSFDDetector", confidence_threshold=.5, nms_iou_threshold=.3)
		self.points = None
		self.setFace = None

	def setSrcImg(self,src_img):
		self.src_img = src_img
		self.face_detection()

	def haveFace(self):
		if(self.points.shape[0] == 0):
			return False
		else:
			return True

	def haveImgSrc(self):
		if self.src_img != "":
			return True
		else:
			return False

	def readImg(self, src_img):
		img = cv2.imread(src_img)
		return img

	def face_detection(self):
		img = self.readImg(self.src_img)
		detections = self.detector.detect(img)
		self.points = detections.copy()

	def convertImg(self):
		setFace = np.arange(self.points.shape[0]*48*48, dtype=float).reshape(self.points.shape[0],48,48,1)
		rootImg = Image.open(self.src_img).convert('L')
		for i in range(self.points.shape[0]):
	  		cropImg = rootImg.crop(self.points[i][:4])
	  		resizeCropImg = cropImg.resize((48,48), Image.Resampling.LANCZOS)
	  		testImg = np.reshape(resizeCropImg,(48,48,1))
	  		setFace[i] = testImg.copy()
		return setFace

	def emotionReg(self):
		setFace = self.convertImg()
		label_dict = {0:'Angry',1:'Disgust',2:'Fear',3:'Happy',4:'Sad',5:'Surprise',6:'Neutral'}

		setResult = self.model.predict(setFace)
		Listemotion = list()
		for i in range(setResult.shape[0]):
			result = list(setResult[i])
			imgIndex = result.index(max(result))
			Listemotion.append(label_dict[imgIndex])
		return ",".join(Listemotion)


