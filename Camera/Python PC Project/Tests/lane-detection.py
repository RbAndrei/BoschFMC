import math

import cv2 as cv
import numpy as np

camera = cv.VideoCapture(0)

# ret, image = camera.read()

image = cv.imread("road.jpg")
image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

cv.imshow("Gray", imgray)

cv.waitKey(0)
cv.destroyAllWindows()

blur = cv.GaussianBlur(imgray, (5, 5), 0)
canny = cv.Canny(blur, 150, 200)

height = image.shape[0]
width = image.shape[1]

triangle_coords = [(0, int(height)),
               (int(width/2), int(height/2)),
               (int(width), int(height))]
trapeze_coords = [(width / 9.4, height / 1.2),
                 (width / 5.6, height / 1.6),#1.8),
                 (width / 1.2, height / 1.6),#1.8),
                 (width / 1.1, height / 1.2)]

mask = np.zeros(canny.shape[:2], dtype="uint8")
# cv.fillPoly(mask, pts=mask_coords, color=(255, 255, 255))
# cv.rectangle(mask, (int(0), int(height/2)), (int(width), int(height)), 255, -1)
cv.fillPoly(mask, np.array([trapeze_coords], np.int32), (255, 255, 255))
masked_image = cv.bitwise_and(canny, mask)

cv.imshow("Mask", masked_image)

cv.waitKey(0)
cv.destroyAllWindows()

lines = cv.HoughLinesP(masked_image,
                       1,
                       np.pi / 180,
                       50,
                       None,
                       30, 15)

print(lines)

if lines is not None:
    for i in range(0, len(lines)):
        line = lines[i][0]
        cv.line(image,
                (line[0], line[1]),
                (line[2], line[3]),
                (0, 0, 255),
                3)

cv.imshow('Lines',image)

cv.waitKey(0)
cv.destroyAllWindows()