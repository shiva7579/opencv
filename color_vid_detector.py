import cv2
import numpy as np

webcam=cv2.VideoCapture(0)
webcam.set(3,640)
webcam.set(4,480)
webcam.set(10,1000000000)

def x(a):
    pass

cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 640, 240)

cv2.createTrackbar("Hue Min", "Trackbars", 30, 179, x)
cv2.createTrackbar("Hue Max", "Trackbars", 107, 179, x)
cv2.createTrackbar("Saturation Min", "Trackbars", 39, 255, x)
cv2.createTrackbar("Saturation Max", "Trackbars", 255, 255, x)
cv2.createTrackbar("Value Min", "Trackbars", 42, 255, x)
cv2.createTrackbar("Value Max", "Trackbars", 255, 255, x)

#STACKING_IMAGES
def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


while True:
    success,img=webcam.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue Min", "Trackbars")
    h_max = cv2.getTrackbarPos("Hue Max", "Trackbars")
    s_min = cv2.getTrackbarPos("Saturation Min", "Trackbars")
    s_max = cv2.getTrackbarPos("Saturation Max", "Trackbars")
    v_min = cv2.getTrackbarPos("Value Min", "Trackbars")
    v_max = cv2.getTrackbarPos("Value Max", "Trackbars")
    print(h_min, h_max, s_min, s_max, v_min, v_max)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    Mask = cv2.inRange(hsv, lower, upper)
    Result = cv2.bitwise_and(img, img, mask=Mask)
    Stack = stackImages(0.5, ([img, hsv], [Mask, Result]))
    cv2.imshow("stacking",Stack)
    if cv2.waitKey(1) & 0xff==ord(' '):
        break

webcam.release()
cv2.destroyAllWindows()


