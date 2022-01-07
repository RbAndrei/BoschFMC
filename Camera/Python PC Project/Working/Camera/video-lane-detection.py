import Working.Libraries.CameraDetection.linecalc as leq
import Working.Libraries.CameraDetection.imageprocessing as imgP

import math

import cv2 as cv


def drawLane(line1, line2):
    cv.line(image,
            (line1[0], line1[1]),
            (line1[2], line1[3]),
            (0, 255, 0),
            3)

    cv.line(image,
            (line2[0], line2[1]),
            (line2[2], line2[3]),
            (0, 255, 0),
            3)


# Sets camera object to receive input from video file
camera = cv.VideoCapture("Videos/road.mkv")

prevcoords = [0, 0]

equation1 = leq.LineEquation()
equation2 = leq.LineEquation()

while True:

    # Read frame by frame from camera object
    ret, image = camera.read()

    # If no frame is read from the camera, exit while loop
    if ret is None:
        break

    height = image.shape[0]
    width = image.shape[1]

    # Coordinates for the trapeze-shaped mask
    mask_coords = [(width / 4.3, height / 1.2),
                   (width / 3, height / 1.4),
                   (width / 1.5, height / 1.4),
                   (width / 1.3, height / 1.2)]

    # Coordinates for center of the lane on camera
    centerL = [int(width / 1.85), int(height / 1.31)]

    imageP = imgP.ImageProcessing(image)

    # set delay only for videos (DELETE when transferring to raspberry)

    cv.waitKey(33)

    # ^^^^^^^^ DELETE ^^^^^^^^^^

    imageP.createmask()

    masked_image = imageP.drawmask(mask_coords)

    # Minimum line height for a line to be taken into consideration as a lane delimiter line
    min_line_height = (height / 1.2 - height / 1.4) / 2

    # minleft and minright are lists of 4 elements
    # containing the x and y coordinates of each of the lines' ends: x1, y1, x2, y2
    minleft, minright = imageP.lanedetection(centerL[0], min_line_height)

    equation1.calcequation(minleft)
    equation2.calcequation(minright)

    intersection_x, intersection_y = equation1.calcintersection(equation2, prevcoords, height)

    # The previous coordinates are remembered in the case that one of the 2
    # lines disappears. In that case the robot will still remember its heading
    # and not go off course
    prevcoords[0] = intersection_x
    prevcoords[1] = intersection_y

    print(prevcoords)
    print(intersection_x, intersection_y)

    if not (math.isnan(intersection_x) or math.isnan(intersection_y)):
        cv.circle(image, (int(intersection_x), int(intersection_y)), 10, (0, 200, 255), -1)

    minleft = equation1.line
    minright = equation2.line

    drawLane(minleft, minright)

    cv.line(image,
            (100, centerL[1]),
            (int(width - 100), centerL[1]),
            (0, 0, 0),
            1)

    cv.circle(image, (centerL[0], centerL[1]), 20, (0, 0, 0), 1)

    cv.imshow('Lines', image)

    if cv.waitKey(1) & 0xff == ord('q'):
        break

cv.destroyAllWindows()
