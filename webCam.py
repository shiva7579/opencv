import cv2
webcam=cv2.VideoCapture(0)
webcam.set(3,640)
webcam.set(4,480)
webcam.set(10,1000000000)
while True:
    success,img=webcam.read()
    cv2.imshow("show",img)
    if cv2.waitKey(1) & 0xff==ord(' '):
        break
