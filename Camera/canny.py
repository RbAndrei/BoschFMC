import cv2 as cv

camera = cv.VideoCapture(0)

#ret, image = camera.read()

image = cv.imread("road.jpg")

imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

cv.imshow("Gray", imgray)

cv.waitKey(0)
cv.destroyAllWindows()

gray = cv.Canny(imgray, 240, 250)
canny = cv.GaussianBlur(gray, (5,5), 0)

cv.imshow("Canny", canny)

cv.waitKey(0)
cv.destroyAllWindows()

