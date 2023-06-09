import cv2
import numpy as np

img1=cv2.imread("C:/Users/nepal/OneDrive/Desktop/carads.jpg")
img2=cv2.imread("C:/Users/nepal/OneDrive/Desktop/cutie.jpg")
print(img1.shape)
print(img2.shape)

#using numpy
# img3=cv2.resize(img1,(872,490))
# grayimg=cv2.cvtColor(img3,cv2.COLOR_BGR2GRAY)
# print(img3.shape)
# horizontal_stack=np.hstack((img2,img3))
# vertical_stack=np.vstack((img2,img3))
#
# cv2.imshow("HShow",horizontal_stack)
# cv2.imshow("VShow",vertical_stack)

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

img3=cv2.resize(img1,(872,490))
print(img3.shape)
grayimg=cv2.cvtColor(img3,cv2.COLOR_BGR2GRAY)

imgstack=stackImages(0.5,([img3,img2,grayimg],[img3,grayimg,img2]))
cv2.imshow("hg",imgstack)

cv2.waitKey(0)