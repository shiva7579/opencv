import cv2
import numpy as np


framewidth = 640
frameheight = 480
# cam = cv2.VideoCapture(0)
# cam.set(3,framewidth)
# cam.set(4,frameheight)
# cam.set(10,100000)

def preprocess(img):
    grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurimg = cv2.GaussianBlur(grayimg, (11, 11), 0)
    cannyimg = cv2.Canny(blurimg, 150, 150)
    kernel = np.ones((5,5))
    imgdilation = cv2.dilate(cannyimg,kernel,iterations=2)
    imgerosion = cv2.erode(imgdilation,kernel,iterations=1)
    return imgerosion

def getcontours(img):
    biggestarea = np.array([])
    maxarea = 0
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area=cv2.contourArea(cnt)
        print(area)
        if area > 5000:
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            if area > maxarea and len(approx) == 4:
                biggestarea = approx
                maxarea = area
    cv2.drawContours(imgn, biggestarea, -1, (255, 255, 0), 20)
    return biggestarea

def reorder(mypoints):
    mypoints = mypoints.reshape((4,2))
    mypointsnew = np.zeros((4,1,2), np.int32)
    add = mypoints.sum(1)
    mypointsnew[0] = mypoints[np.argmin(add)]
    mypointsnew[3] = mypoints[np.argmax(add)]
    diff = np.diff(mypoints, axis=1)
    mypointsnew[1] = mypoints[np.argmin(diff)]
    mypointsnew[2] = mypoints[np.argmax(diff)]
    return mypointsnew


def getWarp(img,biggestarea):
    biggest = reorder(biggestarea)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [framewidth, 0], [0, frameheight], [framewidth, frameheight]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (framewidth, frameheight))

    imgCropped = imgOutput[20:imgOutput.shape[0]-20,20:imgOutput.shape[1]-20]
    imgCropped = cv2.resize(imgCropped,(framewidth,frameheight))

    return imgCropped

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



# while True:
#     success, img = cam.read()
#     cv2.resize(img,(framewidth,frameheight))
#     imgn = img.copy()
#     imgthre = preprocess(img)
#     biggestarea = getcontours(imgthre)
#     if biggestarea.size != 0:
#         imgWarped = getWarp(img, biggestarea)
#         imageArray = ([img,imgthre],
#                   [imgn,imgWarped])
#
#         cv2.imshow("ImageWarped", imgWarped)
#     else:
#         imageArray = ([img, imgthre],
#                        [img, img])
#
#     stackedImages = stackImages(0.6, imageArray)
#     cv2.imshow("Final_output", stackedImages)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


img= cv2.imread("images/document.jpg")
cv2.resize(img,(framewidth,frameheight))
imgn = img.copy()
imgthre = preprocess(img)
biggestarea = getcontours(imgthre)
if biggestarea.size != 0:
   imgwarped = getWarp(img, biggestarea)
   imagearray = ([img,imgthre],
                  [imgn,imgwarped])

   stackedimages = stackImages(0.2, imagearray)
   cv2.imshow("Final_output", stackedimages)
else:
  imagearray = ([img, imgthre])
  stackedimages = stackImages(0.2, imagearray)
  cv2.imshow("Final_output", stackedimages)

cv2.waitKey(0)