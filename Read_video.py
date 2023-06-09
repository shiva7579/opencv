import cv2
vid=cv2.VideoCapture("D:/2nd sem/H/Raincoat/sample.mkv")
while True:
    success, img=vid.read()
    cv2.imshow("try",img)
    if cv2.waitKey(10) & 0xFF==ord('q'):
        break