import cv2 as cv

camera = cv.VideoCapture(0)

while(True):

	ret, image = camera.read()

	imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

	canny = cv.Canny(imgray, 150, 250)
	#canny = cv.GaussianBlur(gray, (5, 5), 0)

	cv.imshow("Canny", canny)

	if cv.waitKey(1) & 0xFF == ord('q'):
		break

cv.destroyAllWindows()

