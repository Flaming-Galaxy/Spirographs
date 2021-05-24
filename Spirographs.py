import turtle
import fractions
import math


class Spirograph:

    # Constructor
    def __init__(self, xc, yc, col, R, r, l):
        self.t = turtle.Turtle()
        self.step = 5  # Set step angle in degrees
        self.drawingComplete = False  # Set drawing complete flag
        self.setparams(xc, yc, col, R, r, l)
        self.restart()  # Initialise drawing

    # Initialise Spirograph object
    def setparams(self, xc, yc, col, R, r, l):
        self.xc = xc
        self.yc = yc
        self.col = col
        self.R = int(R)
        self.r = int(r)
        self.l = l

        # Reduce r/R to simplest form to determine periodicity
        gcdVal = fractions.gcd(self.r, self.R)
        self.period = self.r//gcdVal  # Integer division

        # Ratio of radii r/R
        self.k = r/float(R)

        # Set colour
        self.t.color(*col)

        # Current angle
        self.a = 0

    # Restart drawing
    def restart(self):
        self.drawingComplete = False  # Set flag
        self.t.showturtle()

        # Go to first point
        self.t.up()
        R, k, l = self.R, self.k, self.l
        a = 0.0
        x = R * ((1-k) * math.cos(a) + l*k*math.cos(a/k - a))
        y = R * ((1-k) * math.sin(a) + l*k*math.sin(a/k - a))
        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()

    # Draw spirograph
    def draw(self):
        R, k, l = self.R, self.k, self.l
        for i in range(0, 360*self.period + 1, self.step):
            a = math.radians(i)
            x = R * ((1-k) * math.cos(a) + l*k*math.cos(a/k - a))
            y = R * ((1-k) * math.sin(a) + l*k*math.sin(a/k - a))
        self.t.hideturtle()
