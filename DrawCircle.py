import math
import turtle

# Draw circle
def draw_circle(x, y, r):
    # Move to start of circle
    turtle.up()
    turtle.setpos(x + r, y)
    turtle.down()

    # Draw circle
    for i in range(0, 365, 5):
        a = math.radians(i)
        turtle.setpos(x + r*math.cos(a), y + r*math.sin(a))

draw_circle(100, 100, 50)
turtle.mainloop()