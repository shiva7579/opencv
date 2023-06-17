import cv2
import numpy as np

facecascade=cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
eyecascade=cv2.CascadeClassifier("Resources/haarcascade_eye.xml")
profilecascade=cv2.CascadeClassifier("Resources/haarcascade_profileface.xml")
# img=cv2.imread("images/cutie.jpg")
# grayimg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# for video
def faces(img):
    grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = facecascade.detectMultiScale(grayimg, 1.1, 4)
    eyes = eyecascade.detectMultiScale(grayimg, 1.1, 4)
    prof = profilecascade.detectMultiScale(grayimg, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
    for (x, y, w, h) in eyes:
        cv2.rectangle(img, (x, y), (x + w, y + h), (180, 255, 0), 2)
    for (x, y, w, h) in prof:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
    cv2.imshow("Result", img)




vid=cv2.VideoCapture(0)
while True:
    success, img = vid.read()
    faces(img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()