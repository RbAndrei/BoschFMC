import numpy as np
import cv2 as cv

camera = cv.VideoCapture(0)

while(True):

	ret, img = camera.read()

	imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

	ret, thresh = cv.threshold(imgray, 127, 255, cv.THRESH_BINARY)

	contours, hierarchy = cv.findContours(image=thresh, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)

	image_copy = img.copy()
	cv.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv.LINE_AA)
	cv.imshow("Video Contours", image_copy) 

	if cv.waitKey(1) & 0xFF == ord('q'):
		break

cv.destroyAllWindows()
