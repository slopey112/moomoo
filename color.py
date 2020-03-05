import cv2
import numpy as np

low = np.array([40, 100, 100])
high = np.array([50, 255, 255])
# Approx # of pixels
full_hp = 1200

def get_heal(img_path):
	img = cv2.imread(img_path)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, low, high)
	pixels = cv2.countNonZero(mask)
	return pixels < full_hp
