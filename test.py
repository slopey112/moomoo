import cv2
import numpy as np
import time

img = cv2.imread("/home/slopey/Documents/code/moomoo/screenshots/1.png")
template = cv2.imread("/home/slopey/Documents/code/moomoo/training/tree_res/tree1.png")
res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.5
locs = np.where(res >= threshold)
pivot = (-1000, -1000)
error = 50
for pt in zip(*locs[::-1]):
	if (pt[0] - error < pivot[0] and pt[0] + error > pivot[0]) and (pt[1] - error < pivot[1] and pt[1] + error > pivot[1]):
		continue
	pivot = pt
	cv2.rectangle(img, pt, (pt[0] + 150, pt[1] + 150), (0, 0, 255), 2)
cv2.imshow("img", img)
cv2.waitKey(0)
time.sleep(30)
cv2.destroyAllWindows()
