import cv2
import numpy as np

low = np.array([35, 100, 100])
high = np.array([55, 255, 255])
img = cv2.imread("screenshots/1.png")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, low, high)
print(cv2.countNonZero(mask))
