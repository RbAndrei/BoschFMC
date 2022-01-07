class LineEquation(object):

    def __init__(eq):
        eq.x1 = None
        eq.y1 = None
        eq.x2 = None
        eq.y2 = None

        eq.line = None

        eq.slope = 0.0
        eq.p = 0.0

    def calcequation(eq, line):

        # We calculate the line equation in the form of y = mx + p
        # and store the coefficient of x and the free variable (m and p)

        eq.x1 = line[0]
        eq.y1 = line[1]
        eq.x2 = line[2]
        eq.y2 = line[3]

        if line[1] > 10:
            eq.line = line

        eq.slope = (eq.y2 - eq.y1) / (eq.x2 - eq.x1)
        eq.p = ((-1) * eq.slope * eq.x1 + eq.y1)

        return [eq.slope, eq.p]

    def negate(eq):
        eq.slope *= -1
        eq.p *= -1

    def calcintersection(eq1, eq2, prev, maxheight):

        # To calculate the intersection of the lines we solve the system
        # formed by the lines' eqations

        eq2.negate()

        # After negation the system is of the form:
        # m1 * x1 + p1 = 0
        # -(m2 * x2) - p2 = 0

        eq2.slope += eq1.slope
        eq2.p += eq1.p

        x = ((-1.0) * eq2.p) / float(eq2.slope + 0.0001)
        y = (eq1.p + eq1.slope * x)

        if int(x) < 10 or int(x) > maxheight - 10:
            x = prev[0]
        if int(y) < 10 or int(y) > maxheight - 10:
            y = prev[1]

        return x, y
