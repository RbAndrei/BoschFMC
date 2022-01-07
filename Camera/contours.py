import numpy as np
import cv2 as cv

#camera = cv.VideoCapture(0)

#ret, img = camera.read()

#cv.imwrite('foo.jpg', img)

img = cv.imread('road.jpg')
imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

ret, thresh = cv.threshold(imgray, 127, 255, cv.THRESH_BINARY)
cv.imshow('Binary image', thresh)
cv.waitKey(0)
cv.imwrite('image_thresh.jpg', thresh)
cv.destroyAllWindows()

contours, hierarchy = cv.findContours(image=thresh, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)

image_copy = img.copy()
cv.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv.LINE_AA)
cv.imshow('None approximation', image_copy)
cv.waitKey(0)
cv.imwrite('contours_none_image.jpg', image_copy)
cv.destroyAllWindows()
