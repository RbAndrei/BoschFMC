import math

import cv2 as cv
import numpy as np

camera = cv.VideoCapture("../Working/Camera/Videos/road.mkv")

minleft = [3000, 0, 0, 0]
minright = [3000, 0, 0, 0]

past_dist_left = [3000, 0, 0, 0]
past_dist_right = [3000, 0, 0, 0]

while True:

    ret, image = camera.read()

    if (ret == None):
        break

    # set delay only for videos (DELETE when transfering to raspberry)

    cv.waitKey(33)

    # ^^^^^^^^ DELETE ^^^^^^^^^^

    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    blur = cv.GaussianBlur(imgray, (5, 5), 0)
    canny = cv.Canny(blur, 100, 170)

    height = image.shape[0]

    width = image.shape[1]

    triangle_coords = [(0, int(height)),
                       (int(width / 2), int(height / 2)),
                       (int(width), int(height))]
    trapeze_coords = [(width / 4.3, height / 1.2),
                      (width / 3, height / 1.4),
                      (width / 1.5, height / 1.4),
                      (width / 1.3, height / 1.2)]

    mask = np.zeros(canny.shape[:2], dtype="uint8")

    # cv.fillPoly(mask, pts=mask_coords, color=(255, 255, 255))
    # cv.rectangle(mask, (int(0), int(height/2)), (int(width), int(height)), 255, -1)

    cv.fillPoly(mask, np.array([trapeze_coords], np.int32), (255, 255, 255))
    masked_image = cv.bitwise_and(canny, mask)

    lines = cv.HoughLinesP(masked_image,
                           1,
                           np.pi / 180,
                           50,
                           None,
                           40, 20)

    left_line = [(0, 0), (0, 0)]
    right_line = [(0, 0), (0, 0)]
    centerL = [int(width / 1.85), int(height / 1.31)]

    min_line_height = (height / 1.2 - height / 1.4) / 2


    def intersection_coords(line1, line2):

        X1 = line1[0]
        Y1 = line1[1]
        X2 = line1[2]
        Y2 = line1[3]

        m = (Y1 - Y2) / (X1 - X2)

        v1 = [m, -m * X1 + Y1]

        X1 = line2[0]
        Y1 = line2[1]
        X2 = line2[2]
        Y2 = line2[3]

        m = (Y1 - Y2) / (X1 - X2)

        v2 = [-m, m * X1 - Y1]

        v3 = [v1[0], v1[1]]

        v3[0] += v2[0]
        v3[1] += v2[1]

        x = ((-1) * v3[1]) / v3[0]
        y = ((-1) * v1[1] - v1[0] * x)

        return x, (-1) * y


    # line_diff_coefficient = 1.34

    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:

                if abs(y1 - y2) < min_line_height:
                    break
                # print(centerL[0] - x1, " ", centerL[0] - x2)

                # print(x1 < centerL[0], " ", centerL[0] - x1 < minleft[0])
                # print(x1 < centerL[0] & centerL[0] - x1 < minleft[0])

                if x1 > centerL[0] & x1 - centerL[0] < minright[0]:
                    minright = [x1, y1, x2, y2]
                if x2 > centerL[0] & x2 - centerL[0] < minright[0]:
                    minright = [x1, y1, x2, y2]
                if x1 < centerL[0]:
                    if centerL[0] - x1 < minleft[0]:
                        minleft = [x1, y1, x2, y2]
                if x2 < centerL[0]:
                    if centerL[0] - x2 < minleft[0]:
                        minleft = [x1, y1, x2, y2]

                # if past_dist_left[0] != 3000 & past_dist_right[0] != 3000: if int(past_dist_left[0] *
                # line_diff_coefficient) < centerL[0] - minleft[0] or int(past_dist_left[2] * line_diff_coefficient)
                # < centerL[0] - minleft[2]: minleft = past_dist_left elif int(past_dist_right[0] *
                # line_diff_coefficient) < minright[0] - centerL[0] or int(past_dist_right[2] *
                # line_diff_coefficient) < minright[2] - centerL[0]: minright = past_dist_right

    intersection_x, intersection_y = intersection_coords(minleft, minright)

    print(minleft, minright)
    print(intersection_x, intersection_y)

    if not (math.isnan(intersection_x) or math.isnan(intersection_y)):
        cv.circle(image, (int(intersection_x), int(intersection_y)), 10, (0, 200, 255), -1)

    past_dist_left = minleft
    past_dist_right = minright

    cv.line(image,
            (minleft[0], minleft[1]),
            (minleft[2], minleft[3]),
            (0, 255, 0),
            3)

    cv.line(image,
            (minright[0], minright[1]),
            (minright[2], minright[3]),
            (0, 255, 0),
            3)

    #cv.circle(image, (minleft[2], minleft[3]), 5, (0, 0, 255), -1)
    #cv.circle(image, (minright[0], minright[1]), 5, (0, 0, 255), -1)

    cv.polylines(image, np.array([trapeze_coords], np.int32), True, (0, 0, 255))
    cv.line(image, (100, centerL[1]), (int(width - 100), centerL[1]), (0, 0, 0), 1)
    cv.circle(image, (centerL[0], centerL[1]), 20, (0, 0, 0), 1)

    cv.imshow('Lines', image)

    if cv.waitKey(1) & 0xff == ord('q'):
        break

cv.destroyAllWindows()
