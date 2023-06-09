import cv2
import numpy as np


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
    img = cv2.imread("C://Users//nepal//OneDrive//Desktop//car.jpg")
    imgg = cv2.imread("C://Users//nepal//OneDrive//Desktop//car2.jpg")
    imggg = cv2.imread("C://Users//nepal//OneDrive//Desktop//car4.webp")
    img1 = cv2.resize(img, (200, 200))
    hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    img2 = cv2.resize(imgg, (200, 200))
    hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    img3 = cv2.resize(imggg, (200, 200))
    hsv3 = cv2.cvtColor(img3, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("Hue Min", "Trackbars")
    h_max = cv2.getTrackbarPos("Hue Max", "Trackbars")
    s_min = cv2.getTrackbarPos("Saturation Min", "Trackbars")
    s_max = cv2.getTrackbarPos("Saturation Max", "Trackbars")
    v_min = cv2.getTrackbarPos("Value Min", "Trackbars")
    v_max = cv2.getTrackbarPos("Value Max", "Trackbars")
    print(h_min, h_max, s_min, s_max, v_min, v_max)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    Mask1 = cv2.inRange(hsv1, lower, upper)
    Mask2 = cv2.inRange(hsv2, lower, upper)
    Mask3 = cv2.inRange(hsv3, lower, upper)

    Result1 = cv2.bitwise_and(img1, img1, mask=Mask1)
    Result2 = cv2.bitwise_and(img2, img2, mask=Mask2)
    Result3 = cv2.bitwise_and(img3, img3, mask=Mask3)

    Stack1 = stackImages(1, ([img1, hsv1], [Mask1, Result1]))
    Stack2 = stackImages(1, ([img2, hsv2], [Mask2, Result2]))
    Stack3 = stackImages(1, ([img3, hsv3], [Mask3, Result3]))

    cv2.imshow("CAR1", Stack1)
    cv2.imshow("CAR2", Stack2)
    cv2.imshow("CAR3", Stack3)
    # cv2.imshow("Original1", img1)
    # cv2.imshow("Original2", img2)
    # cv2.imshow("Original3", img3)
    # cv2.imshow("rr",Result1)
    # cv2.imshow("Hsv1", hsv1)
    # cv2.imshow("Hsv2", hsv2)
    # cv2.imshow("Hsv3", hsv3)
    # cv2.imshow("Mask1", Mask1)
    # cv2.imshow("Mask2", Mask2)
    # cv2.imshow("Mask3", Mask3)
    cv2.waitKey(1)
