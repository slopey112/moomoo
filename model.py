import cv2
import numpy as np
import subprocess

class Model:

    def __init__(self, obj):
        self.obj = obj
        data = subprocess.check_output(["ls", "/home/howardp/Documents/Code/moomoo/training/{}/".format(obj)]).decode().split()
        self.templates = [cv2.imread("/home/howardp/Documents/Code/moomoo/training/{}/{}".format(obj, image)) for image in data]
        
        # h + w subject ochange, td
        self.h = 500
        self.w = 500


    def scan(self, img_path):
        img = cv2.imread("/home/howardp/Documents/Code/moomoo/screenshots/{}.png".format(img_path))
        res = [cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) for template in self.templates]
        threshold = 0.5
        locs = [np.where(res[i] >= threshold) for i in range(len(res))]
        points = []
        error = 10
        for loc in locs:
            pivot = (-1000, -1000)
            for pt in zip(*loc[::-1]):
                if (pt[0] - 10 < pivot[0] and pt[0] + 10 > pivot[0]) and (pt[1] - 10 < pivot[1] and pt[1] + 10 > pivot[1]):
                    continue
                else:
                    pivot = pt
                    points.append(pt)
        return points

