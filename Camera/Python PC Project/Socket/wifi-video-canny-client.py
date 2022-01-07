import cv2 as cv
import socket
import sys
import pickle
import struct

camera = cv.VideoCapture(0)

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('192.168.50.24', 8089))

while True:

	ret, image = camera.read()

	imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

	canny = cv.Canny(imgray, 150, 250)
	#canny = cv.GaussianBlur(gray, (5, 5), 0)

	data = pickle.dumps(canny)
	clientsocket.sendall(struct.pack("L", len(data)) + data)

	if cv.waitKey(1) & 0xFF == ord('q'):
		break

cv.destroyAllWindows()

