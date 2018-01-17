import cv2
import numpy as np
import os

def showImg(title,img):
	cv2.imshow(title,img)
	cv2.waitKey(0)

def textBox(text):
	tb_img = np.zeros((40,300,3),np.uint8)
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(tb_img,text,(0,20), font, 0.5,(255,255,255),0,cv2.LINE_AA)
	showImg("Pixel values",tb_img) 

def checkPixelColorAt(img, x,y, color):
	textBox("At:(" + str(y) + "," + str(x) + ") B: " + str(img.item(y,x,0)) +
			" G: " + str(img.item(y,x,1)) +
			" R: " + str(img.item(y,x,2)))
	if img.item(y,x,0) == color and img.item(y,x,1) == color and img.item(y,x,2) == color:
		return True
	return False
	
def fillFrom(x,y, imgCpy):
	cv2.floodFill(imgCpy, None, (x,y),(147,20,255));
	showImg("Floodfill " + str(x) + ", " + str(y),imgCpy)

def createMask(imgCpy):
	img_hsv = cv2.cvtColor(imgCpy, cv2.COLOR_BGR2HSV)
	lower_red = np.array([147,20,255])
	upper_red = np.array([255,255,255])
	mask0 = cv2.inRange(img_hsv, lower_red,upper_red)
	inv_mask0 = cv2.bitwise_not(mask0)
	showImg("inv_mask0",inv_mask0)
	return inv_mask0
	
def applyMask(mask, img):
	b,g,r = cv2.split(img)
	rgba = [b,g,r,mask]
	return rgba

srcImg = cv2.imread(r'c:\temp\1123_2.png')
showImg("original", srcImg)
img_height, img_width = srcImg.shape[:2]
img_height = img_height - 1
img_width = img_width - 1
textBox("W: " + str(img_width) + " H: " + str(img_height))

imgCpy = srcImg.copy()

if checkPixelColorAt(imgCpy, img_width,0,255):
	fillFrom(img_width,0, imgCpy)
	img_changed = True
if checkPixelColorAt(imgCpy, img_width,img_height,255):
	fillFrom(img_width,img_height, imgCpy)
	img_changed = True
if checkPixelColorAt(imgCpy, 0,img_height,255):
	fillFrom(0,img_height, imgCpy)
	img_changed = True
if checkPixelColorAt(imgCpy, 0,0,255):
	fillFrom(0,0, imgCpy)
	img_changed = True
	
mask = createMask(imgCpy)
rgba = applyMask(mask, srcImg)
dst = cv2.merge(rgba,4)

showImg("Final",dst)
cv2.imwrite(r'c:\temp\out_raster.tif',dst)
cv2.destroyAllWindows()
