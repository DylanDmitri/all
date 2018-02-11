import turtle
import math
import time

# user inputs
area = 1000
color = "red"
shape = "circle"

# settup turtle
alex = turtle.Turtle('turtle')
alex.color(color)

def draw_polygon(*sides):
    alex.begin_fill()

    for length, angle in sides:
        alex.forward(length)
        alex.left(angle)

    alex.end_fill()
    alex.hideturtle()
    time.sleep(1.5)
    alex.reset()

def draw_regular_polygon(sides):
    angle = 180 - (180*(sides-2) / sides)
    R = (1/2) * a csc(π/n) = r sec(π/n)

    side_length = area * 4*math.tan(math.pi/sides) / (sides)
    draw_polygon(*[(side_length, angle)]*sides)

# -- DRAW THE SHAPE --
sides = dict(triangle=3, square=4, pentagon=5,
             hexagon=6, heptagon=7, octagon=8,
             nonagon=9, decagon=10, circle=100,
           ).get(shape, 0)

for s in range(3, 12):
    draw_regular_polygon(s)

if sides != 0:
    draw_regular_polygon(sides)

elif shape == "trapezoid":
    dim = ((64*area) / (7 * 3**.5)) ** .5
    draw_polygon((dim, 120), (dim/4, -120), (-dim*(3/4), -120), (dim/4, 120))

elif shape == "rhombus":
    dim = ((2 * area) / (3 ** .5)) ** .5
    alex.left(60)
    draw_polygon((dim, 60), (dim, 120), (dim, 60), (dim, 60))

else:
    print("unknown shape ")
