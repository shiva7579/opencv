import cv2
import numpy as np

img=cv2.imread("C:\\Users\\nepal\\OneDrive\\Desktop\\carads.jpg")
print(img.shape)
cv2.imshow("Cards",img)
cv2.waitKey(0)