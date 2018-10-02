import numpy as np
import cv2

import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.pyplot as plt

img1 = cv2.imread('Leftfinal.jpg',0)
img2 = cv2.imread('testnear2.jpg',0)
edges1 = cv2.Canny(img2,100,200)
#edges1 = cv2.Canny(img1,100,200)
#edges2 = cv2.Canny(img2,100,200)
#img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
ret, img2b = cv2.threshold(img2,185,255,cv2.THRESH_BINARY)
blur = cv2.GaussianBlur(img2b,(21,21),0)

edges2 = cv2.Canny(blur,100,200)

orb = cv2.ORB_create()

#cv2.imshow('e1',edges1)
#cv2.imshow('e2',edges2)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(edges1,None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

matches = bf.match(des1,des2)
matches = sorted(matches, key = lambda x:x.distance)

img3 = cv2.drawMatches(img1,kp1,edges1,kp2,matches[:10],None, flags=2)
plt.imshow(img3)
plt.show()
