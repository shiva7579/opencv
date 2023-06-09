import cv2
import numpy as np

kernel=np.ones((5,5),np.uint8)
# print(kernel)
img=cv2.imread("C:/Users/nepal/OneDrive/Desktop/cutie.jpg")
resizeimg=cv2.resize(img,(300,300))
# print(img.shape)
grayimg=cv2.cvtColor(resizeimg,cv2.COLOR_BGR2GRAY)
blurimg=cv2.GaussianBlur(grayimg,(11,11),0)
cannyimg=cv2.Canny(resizeimg,150,150)
imgdilation=cv2.dilate(cannyimg,kernel,iterations=1)
imgerosion=cv2.erode(imgdilation,kernel,iterations=1)
imgcropped=resizeimg[0:150,0:150]
cv2.imshow("Real",resizeimg)
cv2.imshow("Gray",grayimg)
cv2.imshow("blur",blurimg)
cv2.imshow("canny",cannyimg)
cv2.imshow("dilate",imgdilation)
cv2.imshow("erode",imgerosion)
cv2.imshow("cropped",imgcropped)
cv2.waitKey(0)

