from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import ImageTk, Image
from emotion import *

obj = emotion()

def displayOnImgLabel(myImg):
	imgLabel.configure(image=myImg)
	imgLabel.image = myImg

	textLabel.configure(text="Image changed")
	textLabel.text = "Image changed"


def openImage(urDir):
	myImg = Image.open(urDir)
	resizeImg = myImg.resize((300,150), Image.Resampling.LANCZOS)
	convertedImg = ImageTk.PhotoImage(resizeImg)
	displayOnImgLabel(convertedImg)


def chooseImg():
	root.filedir = filedialog.askopenfilename(
		initialdir="../images/", 
		title="Select Image", 
		filetypes=(("Select Image","*.*"),("JPG","*.jpg"),("JPEG","*.jpeg"),("PNG","*png")))
	if root.filedir != "":
		obj.setSrcImg(root.filedir)
		openImage(root.filedir)

def displayOnTextLabel(message):
	textLabel.configure(text= f"Emotion: {message}")
	textLabel.text = f"Emotion: {message}"\

def displayErrOnTextLabel(message):
	textLabel.configure(text= message)
	textLabel.text = message

def detectEmontion():

	if (obj.haveImgSrc() is False):
		displayErrOnTextLabel("Select Image, pls.")
		return

	if(obj.haveFace()):
		message = obj.emotionReg()
	else:
		message = " cannot be guessed, because face not found."
	displayOnTextLabel(message)

root = Tk()
root.title("Emotion")
# root.iconbitmap()
root.geometry("350x350")

frame = Frame(root)
frame.pack(side=BOTTOM, padx=15, pady=15)

img1 = Image.open("../images/default.png")
resizeImg = img1.resize((300,150), Image.Resampling.LANCZOS)
convertedImg = ImageTk.PhotoImage(resizeImg)

imgLabel = Label(root, image=convertedImg, width=300, height=150)
textLabel = Label(root, text="Select Image")

chooseImgBtn = Button(frame, text="Select Image", command=chooseImg)
exitBtn = Button(frame, text="Exit", command=root.quit)
detectBtn = Button(frame, text="Detect", command=detectEmontion)


imgLabel.pack(side=TOP, ipadx=5, ipady= 5)
textLabel.pack(side=TOP, ipadx=5, ipady= 5)

chooseImgBtn.pack(side=tk.LEFT, padx= 10)
detectBtn.pack(side=tk.LEFT, padx= 10)
exitBtn.pack(side=tk.LEFT, padx= 10)

root.mainloop()