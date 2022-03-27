import turtle
import random
from collections import namedtuple
from math import sqrt

Aircraft = namedtuple("Aircraft", "acid, type, heading, altitude")

CALLSIGNS = ["ACA", "BAW", "GGN", "NCB", "NWT", "CFC", "JZA", "WJA",
             "UAL", "CRQ", "DAL", "GLR"]

PLANE_TYPES = ["A320", "B190", "B747", "CRJ9", "B737"]

PPS_SIDE = 10
RADIUS = 270


class PenUp:
    """
    Context manager for movements during which time pen should be up.
    """
    def __enter__(self):
        turtle.penup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        turtle.pendown()


class KeepPos:
    """
    Context manager for storing pen position and returning to it at exit.
    """
    def __init__(self):
        self.x, self.y = turtle.position()
        self.heading = turtle.heading()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with PenUp():
            turtle.goto(self.x, self.y)
            turtle.setheading(self.heading)


def random_altitudes() -> tuple[str, str]:
    """
    Return two altitudes for pps displays.
    """
    alt_range = (90, 290)
    a = random.randrange(*alt_range, step=10)
    b = a + 10
    return f"{a:03d}", f"{b:03d}"


def random_acid() -> str:
    callsign = random.choice(CALLSIGNS)
    number = str(random.randint(100, 999))
    return callsign + number


def line_headings() -> tuple[float, float]:
    """
    Return two random headings modulo 180.
    """
    heading_range = 0, 179.9999
    heading_0 = random.uniform(*heading_range)
    heading_1 = random.uniform(*heading_range)
    return heading_0, heading_1


def generate_aircraft(heading_0, heading_1) -> tuple[namedtuple, namedtuple]:
    alt_0, alt_1 = random_altitudes()
    craft_0 = Aircraft(acid=random_acid(), type=random.choice(PLANE_TYPES), heading=heading_0, altitude=alt_0)
    craft_1 = Aircraft(acid=random_acid(), type=random.choice(PLANE_TYPES), heading=heading_1, altitude=alt_1)
    return craft_0, craft_1


def draw_circle() -> None:
    """
    Draw a circle to enclose the exercise.
    """
    with KeepPos() as pos:
        with PenUp():
            turtle.setx(pos.x + RADIUS)
        turtle.circle(RADIUS)


def draw_lines(heading_0, heading_1) -> None:
    """
    Draw two diameters through the centre at specified headings.
    """
    for heading in heading_0, heading_1:
        with KeepPos():
            with PenUp():
                turtle.setheading(heading)
                turtle.forward(RADIUS)
            turtle.backward(2 * RADIUS)
    return heading_0, heading_1


def place_pps(aircraft: tuple) -> None:
    """
    Place a PPS on each of the lines defined by two-member tuple of
    Aircraft at the same distance from the centre.
    """
    distance = random.randint(30, 170)
    parities = [1, -1]
    parity = random.choice(parities)
    for i, craft in enumerate(aircraft):
        if i == 1:
            if abs(aircraft[0].heading - aircraft[1].heading) <= 20:
                parity = 1 if parity == -1 else -1
            else:
                parity = random.choice(parities)
        with KeepPos():
            modded_distance = parity * distance
            with PenUp():
                turtle.setheading(craft.heading)
                turtle.forward(modded_distance)
            text = f"{craft.acid}\n" \
                   f"{craft.type}\n" \
                   f"{craft.altitude}    25"
            draw_pps()
            with PenUp():
                turtle.forward(parity * (RADIUS / 4))
                turtle.write(text)


def draw_pps() -> None:
    """
    Draw a PSR/SSR Correlated PPS at current position.
    """
    with KeepPos():

        with PenUp():
            turtle.setheading(360)
            turtle.forward(PPS_SIDE)

        hexagon_angles = (120, 180, 240, 300, 360, 60)
        for angle in hexagon_angles:
            turtle.setheading(angle)
            turtle.forward(PPS_SIDE)

        triangle_angles = (150, 270, 30)
        for angle in triangle_angles:
            turtle.setheading(angle)
            turtle.forward(PPS_SIDE * sqrt(3))


def init() -> None:
    turtle.mode('logo')
    turtle.hideturtle()
    turtle.speed(0)
    turtle.onscreenclick(draw)


def reset() -> None:
    turtle.clear()
    turtle.setheading(360)
    turtle.home()


def draw(*args) -> None:
    reset()
    draw_circle()
    headings = line_headings()
    draw_lines(*headings)
    place_pps(generate_aircraft(*headings))


def main() -> None:
    init()
    draw()


if __name__ == '__main__':
    main()
    turtle.mainloop()
