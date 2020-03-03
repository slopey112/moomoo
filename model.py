import cv2
import numpy as np
import subprocess
import time

class Model:
	directory = "" 

	def __init__(self, obj, directory):
		self.obj = obj
		Model.directory = directory
		data = subprocess.check_output(["ls", "{}/training/{}/".format(directory, obj)]).decode().split()
		self.templates = [cv2.imread("{}/training/{}/{}".format(directory, obj, image)) for image in data]
		
		# h + w subject ochange, td
		height, width, channels = self.templates[0].shape
		self.h = height
		self.w = width


	def scan(self, img_path):
		img = cv2.imread("{}/screenshots/{}.png".format(Model.directory, img_path))
		res = [cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) for template in self.templates]
		threshold = 0.7
		locs = [np.where(res[i] >= threshold) for i in range(len(res))]
		points = []
		error = 50
		for loc in locs:
			pivot = (-1000, -1000)
			for pt in zip(*loc[::-1]):
				if (pt[0] - error < pivot[0] and pt[0] + error > pivot[0]) and (pt[1] - error < pivot[1] and pt[1] + error > pivot[1]):
					continue
				else:
					cv2.rectangle(img, pt, (pt[0] + self.w, pt[1] + self.h), (0, 0, 255), 2)
					pivot = pt
					points.append(pt)
		cv2.imshow("img", img)
		cv2.waitKey(0)
		time.sleep(5)
		cv2.destroyAllWindows()
		return points

