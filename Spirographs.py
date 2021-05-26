import turtle
import math
import random
from datetime import datetime
from PIL import Image
import argparse


class Spirograph:

    # Constructor
    def __init__(self, xc, yc, col, R, r, l):
        self.t = turtle.Turtle()
        self.t.shape("turtle")
        self.step = 5  # Set step angle in degrees
        self.drawingComplete = False  # Set drawing complete flag
        self.setparams(xc, yc, col, R, r, l)
        self.restart()  # Initialise drawing

    # Initialise Spirograph object
    def setparams(self, xc, yc, col, R, r, l):
        self.xc = xc  # Centre x coordinate of spirograph
        self.yc = yc  # Centre y coordinate of spirograph
        self.col = col  # Colour in RGB
        self.R = int(R)  # Large circle radius
        self.r = int(r)  # Small circle radius
        self.l = l  # ratio of r to where the "pen" will draw

        # Reduce r/R to simplest form to determine periodicity
        gcdVal = math.gcd(self.r, self.R)
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
            self.t.setpos(self.xc + x, self.yc + y)
        self.t.hideturtle()

    # Draw spirographs in steps
    def update(self):

        # Exit if drawing complete
        if self.drawingComplete:
            return

        # Draw a step
        R, k, l = self.R, self.k, self.l
        self.a += self.step
        a = math.radians(self.a)
        x = R * ((1-k) * math.cos(a) + l*k*math.cos(a/k - a))
        y = R * ((1-k) * math.sin(a) + l*k*math.sin(a/k - a))
        self.t.setpos(self.xc + x, self.yc + y)

        # Check if drawing is complete and set flag
        if self.a >= 360*self.period:
            self.drawingComplete = True
            self.t.hideturtle()

    # Clear spirograph
    def clear(self):
        self.t.clear()


# Class to draw random spiros simultaneously
class SpiroAnimator:

    # Constructor
    def __init__(self, N):
        self.deltaT = 10  # Timer value in ms

        # Window dimensions
        self.width = turtle.window_width()
        self.height = turtle.window_height()

        # Generate random spiros
        self.spiros = []
        for i in range(N):
            randomParams = self.generate_random_params()
            spiro = Spirograph(*randomParams)
            self.spiros.append(spiro)
            # Call update after timer is up
            turtle.ontimer(self.update, self.deltaT)

    # Generate random parameters for spirographs
    def generate_random_params(self):
        width, height = self.width, self.height
        R = random.randint(50, min(width, height)//2)
        r = random.randint(10, 9*R//10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width//4, width//4)
        yc = random.randint(-height//4, height//4)
        col = (random.random(),
               random.random(),
               random.random())
        return (xc, yc, col, R, r, l)

    # Restart animator
    def restart(self):
        for spiro in self.spiros:
            spiro.clear()

            # Generate new spirographs
            randomParams = self.generate_random_params()
            spiro.setparams(*randomParams)

            # Get ready to restart drawing
            spiro.restart()

    # Draw all spirographs in steps
    def update(self):
        numComplete = 0
        for spiro in self.spiros:
            spiro.update()
            if spiro.drawingComplete:
                numComplete += 1

        # Restart drawing when all spirographs are complete
        if numComplete == len(self.spiros):
            self.restart()

        # Call update again after timer is up
        turtle.ontimer(self.update, self.deltaT)

    # Show or hide cursor
    def toggle_cursor(self):
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()


# Save drawings as PNGs
def save_drawing():
    turtle.hideturtle()

    # Generate unique file names
    dateString = datetime.now().strftime("%d%b%Y-%H%M%S")
    fileName = "Spirograph - " + dateString
    print("Saving to " + fileName + ".eps/png")

    # Save as PNG
    canvas = turtle.getcanvas()
    canvas.postscript(file=fileName + ".eps")
    img = Image.open(fileName + ".eps")
    img.save(fileName + '.png', 'png')

    turtle.showturtle()

# main() function


def main():
    print('Generating spirograph...')

    # Create parser
    descStr = """This program draws spirographs using the Turtle module. 
    When run with no arguments, this program draws a random spirograph.
    
    Terminology:
    R: radius of outer circle.
    r: radius of inner circle.
    l: ratio of hole distance to r.
    """
    parser = argparse.ArgumentParser(description=descStr)

    # Add expected arguments
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False,
                        help="The three arguments in sparams: R, r, l.")

    # Parse arguments
    args = parser.parse_args()

    # Set up window
    turtle.setup(width=0.8)
    turtle.title("Spirographs!")

    # Add key handler for saving images
    turtle.onkey(save_drawing, key="s")
    turtle.listen()
    turtle.hideturtle()

    # Check arguments and draw spirograph(s)
    if args.sparams:
        params = [float(x) for x in args.sparams]
        col = (0.0, 0.0, 0.0)  # Default colour is black
        spiro = Spirograph(0, 0, col, *params)
        spiro.draw()
    else:
        spiroAnim = SpiroAnimator(1)
        # Key handler to toggle turtle cursor
        turtle.onkey(spiroAnim.toggle_cursor, "t")
        # Key handler to restart animation
        turtle.onkey(spiroAnim.restart, "space")

    # Start turtle main loop
    turtle.mainloop()


# Call main() function when file is run
if __name__ == '__main__':
    main()
