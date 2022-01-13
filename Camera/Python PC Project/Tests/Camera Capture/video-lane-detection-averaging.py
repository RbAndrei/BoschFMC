import Working.Libraries.CameraDetection.linecalc as leq
import Working.Libraries.CameraDetection.imageprocessing as imgP

import math

import cv2 as cv
import numpy as np

prev_left = None
prev_right = None


def average(image, lines):
    global prev_left, prev_right

    left = []
    right = []
    for line in lines:
        # print(line)
        x1, y1, x2, y2 = line.reshape(4)

        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        y_int = parameters[1]
        if slope < 0:
            left.append((slope, y_int))
        else:
            right.append((slope, y_int))

    right_avg = np.average(right, axis=0)
    left_avg = np.average(left, axis=0)

    try:
        left_line = make_points(image, left_avg)
    except:
        left_line = make_points(image, prev_left)
        left_avg = prev_left

    try:
        right_line = make_points(image, right_avg)
    except:
        right_line = make_points(image, prev_right)
        right_avg = prev_right

    prev_left = left_avg
    prev_right = right_avg

    return np.array([left_line, right_line])


def make_points(image, average):
    slope, y_int = average

    y1 = int(image.shape[0] / 1.2)
    y2 = int(image.shape[0] / 1.4)
    x1 = int((y1 - y_int) // slope)
    x2 = int((y2 - y_int) // slope)

    return np.array([x1, y1, x2, y2])


def display_lines(image, lines):
    lines_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line
            cv.line(lines_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return lines_image


# Sets camera object to receive input from video file
camera = cv.VideoCapture("../../Working/Camera/Videos/road.mkv")

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
    mask_coords = [(width / 2.58, height / 1.2),
                   (width / 2.08, height / 1.4),
                   (width / 1.7, height / 1.4),
                   (width / 1.3, height / 1.2)]

    # Coordinates for center of the lane on camera
    centerL = [int(width / 1.85), int(height / 1.31)]

    imageP = imgP.ImageProcessing(image)

    # set delay only for videos (DELETE when transferring to raspberry)

    cv.waitKey(33)

    # ^^^^^^^^ DELETE ^^^^^^^^^^

    imageP.createmask()

    masked_image = imageP.drawmask(mask_coords)

    copy = np.copy(image)

    lines = cv.HoughLinesP(masked_image, 2, np.pi / 180, 100, np.array([]), minLineLength=60, maxLineGap=5)

    if lines is None:
        lines = np.array([])

    averaged_lines = average(copy, lines)
    black_lines = display_lines(copy, averaged_lines)
    lanes = cv.addWeighted(copy, 0.8, black_lines, 1, 1)

    cv.circle(image, (centerL[0], centerL[1]), 20, (0, 0, 0), 1)

    minleft = averaged_lines[0]
    minright = averaged_lines[1]

    equation1.calcequation(minleft)
    equation2.calcequation(minright)

    intersection_x, intersection_y = equation1.calcintersection(equation2, prevcoords, height)

    # The previous coordinates are remembered in the case that one of the 2
    # lines disappears. In that case the robot will still remember its heading
    # and not go off course
    prevcoords[0] = intersection_x
    prevcoords[1] = intersection_y

    # print(prevcoords)
    # print(intersection_x, intersection_y)

    if not (math.isnan(intersection_x) or math.isnan(intersection_y)):

        cv.circle(lanes,
                  (int(intersection_x), int(intersection_y)),
                  10,
                  (14, 14, 201),
                  -1)
        cv.line(lanes,
                (centerL[0], centerL[1]),
                (int(intersection_x), int(intersection_y)),
                (14, 14, 201),
                6)

        line1 = abs(centerL[0] - intersection_x)
        line2 = abs(centerL[1] - intersection_y)

        if centerL[0] > intersection_x:
            angle = math.atan2(line2, line1)
        else:
            angle = math.atan2(line1, line2) + 1.5708

        angle *= 180.0 / math.pi

        # angle = 180 - angle

        # print("(", line1, line2, angle, ")")

        cv.putText(lanes,
                   str(angle),
                   (centerL[0], centerL[1] + 32),
                   cv.FONT_HERSHEY_PLAIN,
                   1,
                   (255, 255, 255),
                   1)

    minleft = equation1.line
    minright = equation2.line

    cv.line(lanes,
            (100, centerL[1]),
            (int(width - 100), centerL[1]),
            (0, 0, 0),
            1)

    cv.circle(lanes, (centerL[0], centerL[1]), 20, (0, 0, 0), 1)

    cv.imshow('Lines', lanes)

    if cv.waitKey(1) & 0xff == ord('q'):
        break

cv.destroyAllWindows()
