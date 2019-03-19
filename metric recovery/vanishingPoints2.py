# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 10:51:55 2019

Metric and affine rectification of images using parallel lines (in 2D)

@author: Gopiraj
"""

#loading the necessary libraries
import numpy as np
import cv2

#Reading the image
img = cv2.imread('floor.png')

#making the first line
p1 = [171, 244, 1]
p2 = [422, 123, 1]

l1 = np.cross(p1, p2)
l1 = l1/l1[-1]


#making the second line
p3 = [143, 117, 1]
p4 = [338, 247, 1]

l2 = np.cross(p3, p4)
l2 = l2/l2[-1]

#line parallel to l1
p5 = [108, 191, 1]
p6 = [356, 88, 1]

l3 = np.cross(p5, p6)
l3 = l3/l3[-1]


#line parallel to l2
p7 = [226, 87, 1]
p8 = [424, 200, 1]

l4 = np.cross(p7, p8)
l4 = l4/l4[-1]


#calculating the vanishing points
x1 = np.cross(l1, l3)
x1 = x1/x1[-1]

x2 = np.cross(l2, l4)
x2 = x2/x2[-1]

#calculating the vanishing line
vLine = np.cross(x1, x2)
vLine = vLine/vLine[-1]

#Transformation to make vanishing line to infinity
H = np.eye(3)
H[2, 0] = vLine[0]
H[2, 1] = vLine[1]

#removing the projective distortion
res = cv2.warpPerspective(img, H, (img.shape[1], img.shape[0]))

cv2.imwrite('floor_affineRect.png', res)

#detecting pairs of lines in the affine rectified image
p1 = [107, 151, 1]
p2 = [330, 98, 1]

l1_m = np.cross(p1, p2)
l1_m = l1_m/l1_m[-1]

p3 = [113, 91, 1]
p4 = [212, 156, 1]

l2_m = np.cross(p3, p4)
l2_m = l2_m/l2_m[-1]

p5 = [73, 129, 1]
p6 = [295, 75, 1]

l3_m = np.cross(p5, p6)
l3_m = l3_m/l3_m[-1]

p7 = [185, 71, 1]
p8 = [289, 136, 1]

l4_m = np.cross(p7, p8)
l4_m = l4_m/l4_m[-1]

#2 pairs of parallel lines in affine rectified image
lines = [[], []]
lines[0].append(l1_m)
lines[0].append(l3_m)
lines[1].append(l2_m)
lines[1].append(l4_m)

#transforming the parallel lines
nlines = 2
RHS = np.zeros((nlines,1))
A = np.zeros((nlines, 2))
for k in range(0,nlines):
    RHS[k] = -lines[0][k][1]*lines[1][k][1]
for k in range(0,nlines):
    A[k,0] = lines[0][k][0]*lines[1][k][0]
    A[k,1] = lines[0][k][0]*lines[1][k][1] + lines[0][k][1]*lines[1][k][0]
s = np.linalg.lstsq(A,RHS)[0]
S = np.array([[s[0][0], s[1][0]],[s[1][0],1]])

#lines transform as l' = H^-T * l
u,s,vh = np.linalg.svd(S,full_matrices=1,compute_uv=1)

A = np.linalg.cholesky(S)

H1 = np.zeros((3,3))
H1[0:2,0:2] = A
H1[2,2] = 1

res = cv2.warpPerspective(res, np.linalg.inv(H1).T, (img.shape[1], img.shape[0]))

cv2.imwrite('floor_metricRect.png', res)

#combined transformation
Hc = np.linalg.inv(H1).T #affine rectification
Hc[2, :2] = vLine[:2] #projective rectification

#performing rectification on the original image 
res = cv2.warpPerspective(img, Hc, (img.shape[1], img.shape[0]))

cv2.imwrite('combined_rect.png', res)

#cv2.namedWindow("res", cv2.WINDOW_FREERATIO)
cv2.imshow("res", res)
cv2.imshow("orig", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

