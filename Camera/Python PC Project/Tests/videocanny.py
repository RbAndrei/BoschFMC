import cv2 as cv

camera = cv.VideoCapture("road.mkv")

while(True):

	ret, image = camera.read()

	# set delay only for videos (DELETE when transfering to raspberry)

	cv.waitKey(33)

	# ^^^^^^^^ DELETE ^^^^^^^^^^

	imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

	#blur = cv.GaussianBlur(imgray, (5, 5), 0)
	canny = cv.Canny(imgray, 100, 170)


	cv.imshow("Canny", canny)

	if cv.waitKey(1) & 0xFF == ord('q'):
		break

cv.destroyAllWindows()

