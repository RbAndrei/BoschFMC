import cv2
import numpy


class ImageProcessing(object):

    def __init__(self, image):
        self.image = image
        self.maskcoords = None

        self.mask = None
        self.canny = None

        self.masked_image = None

    def createmask(self):

        # We put a mask over the parts of the image we do not want
        # our line detection program to take into account

        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        imgray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        blur = cv2.GaussianBlur(imgray, (5, 5), 0)
        canny = cv2.Canny(blur, 100, 170)

        mask = numpy.zeros(canny.shape[:2], dtype="uint8")

        self.mask = mask
        self.canny = canny

        return mask, canny

    def drawmask(self, maskcoords):

        mask = self.mask
        canny = self.canny
        image = self.image

        self.maskcoords = maskcoords

        cv2.fillPoly(mask, numpy.array([maskcoords], numpy.int32), (255, 255, 255))
        cv2.polylines(image, numpy.array([maskcoords], numpy.int32), True, (0, 0, 255))
        masked_image = cv2.bitwise_and(canny, mask)

        self.masked_image = masked_image

        return masked_image

    def lanedetection(self, center, min_line_height):

        # To detect the lane this function takes the center point of the lane and
        # selects the line to the left of the center that is closest to the center
        # and the line to the right of the center that is closest to the center
        # The coordinates of these lines are memorised into minleft and minright, respectively

        masked_image = self.masked_image

        lines = cv2.HoughLinesP(masked_image, 1, numpy.pi / 180, 50, None, 40, 20)

        minleft = [3000, 0, 0, 0]
        minright = [3000, 0, 0, 0]

        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:

                    # Checks that the line isn't horizontal
                    if abs(y1 - y2) < min_line_height:
                        break

                    if x1 > center and x1 - center < minright[0]:
                        minright = [x1, y1, x2, y2]
                    if x2 > center and x2 - center < minright[0]:
                        minright = [x1, y1, x2, y2]
                    if x1 < center and center - x1 < minleft[0]:
                            minleft = [x1, y1, x2, y2]
                    if x2 < center and center - x2 < minleft[0]:
                            minleft = [x1, y1, x2, y2]

        return minleft, minright
