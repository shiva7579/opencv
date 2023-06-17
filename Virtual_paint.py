import cv2
import numpy as np

webcam=cv2.VideoCapture(0)
webcam=cv2.VideoCapture(0)
webcam.set(3,640)
webcam.set(4,480)
webcam.set(10,100)

#yellow_color
colors = [[0, 81, 100, 26, 186, 255]]
#displaying circle of same color
yellow=[[0,255,255]]

mypoints=[]
def findcolors(img,colors,yellow):
    HSVimage=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    newpoints=[]
    lower = np.array(colors[0][0:3])
    upper = np.array(colors[0][3:6])
    mask = cv2.inRange(HSVimage, lower, upper)
    cv2.imshow("mask",mask)
    x,y=getcontours(mask)
    cv2.circle(imgn, (x, y), 10, yellow[0], cv2.FILLED)
    if x!=0 and y!=0:
        newpoints.append([x,y])
    return newpoints

def getcontours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area > 500:
            cv2.drawContours(imgn, cnt, -1, (255, 255, 0), 3)
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            # objcor=len(approx)
            x,y,w,h=cv2.boundingRect(approx)
    return x+w//2,y


def drawpoints(mypoints,yellow):
    for points in mypoints:
        cv2.circle(imgn, (points[0], points[1]), 10, yellow[0], cv2.FILLED)



while True:
    success, img=webcam.read()
    imgn=img.copy()
    newpoints=findcolors(img,colors,yellow)
    if len(newpoints)!=0:
        for newp in newpoints:
            mypoints.append(newp)
    if len(newpoints)!=0:
        drawpoints(mypoints, yellow)
    cv2.imshow("Image",imgn)
    if cv2.waitKey(1) & 0xff == ord(' '):
        break

webcam.release()
cv2.destroyAllWindows()
