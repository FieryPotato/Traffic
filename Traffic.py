import turtle
import random
from collections import namedtuple
from math import sqrt


Aircraft: namedtuple = namedtuple("Aircraft", "acid, type, heading, altitude, speed")

CALLSIGNS: list[str] = ["ACA", "BAW", "GGN", "NCB", "NWT", "CFC", "JZA", "WJA",
                        "UAL", "CRQ", "DAL", "GLR"]

PLANE_TYPES: list[str] = ["A320", "B190", "B747", "CRJ9", "B737"]

# Lowest altitude, highest altitude - 10
ALTITUDE_RANGE: tuple[int, int] = (90, 290)

HEADING_RANGE: tuple[float, float] = (0, 179.9999)

PARITIES = [1, -1]
PPS_SIDE: int = 10
RADIUS: int = 270
MILE_LENGTH: int = 40
SMALLEST_SAME_HEADING_ANGLE = 30


class PenUp:
    """
    Context manager to automate putting pen up and down for movement.
    """
    def __enter__(self) -> "PenUp":
        turtle.penup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        turtle.pendown()


class KeepPos:
    """
    Context manager for storing pen position and returning to it at exit.
    """
    x: float
    y: float

    def __init__(self) -> None:
        self.x, self.y = turtle.position()
        self.heading: float = turtle.heading()

    def __enter__(self) -> "Keep Pos":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        with PenUp():
            turtle.goto(self.x, self.y)
            turtle.setheading(self.heading)


def random_altitudes() -> tuple[str, str]:
    """
    Return two altitudes for pps displays.
    """
    a = random.randrange(*ALTITUDE_RANGE, step=10)
    b = a + 10
    return f"{a:03d}", f"{b:03d}"


def random_acid() -> str:
    callsign: str = random.choice(CALLSIGNS)
    percentage_of_4_digit_flight_numbers = 0.1

    if random.uniform(0, 1) < percentage_of_4_digit_flight_numbers:
        number: int = random.randint(1000, 9999)
    else:
        number: int = random.randint(100, 999)

    return callsign + str(number)


def generate_aircraft(heading_0: float, heading_1: float) -> tuple[namedtuple, namedtuple]:
    alt_0, alt_1 = random_altitudes()

    craft_0 = Aircraft(acid=random_acid(), type=random.choice(PLANE_TYPES),
                       heading=heading_0, altitude=alt_0, speed=25)

    craft_1 = Aircraft(acid=random_acid(), type=random.choice(PLANE_TYPES),
                       heading=heading_1, altitude=alt_1, speed=25)

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


def place_pps(aircraft_list: tuple[Aircraft, Aircraft]) -> None:
    """
    Place a PPS on each of the lines defined by two-member tuple of
    Aircraft at the same distance from the centre.
    """
    distance = random.randint(40, 170)
    parity = random.choice(PARITIES)

    for i, aircraft in enumerate(aircraft_list):

        # Prevent PPS from being too close to each other by preventing same-
        # parity when the angles are too similar.
        heading_angle = abs(aircraft_list[0].heading - aircraft_list[1].heading)
        if i == 1:
            if heading_angle < SMALLEST_SAME_HEADING_ANGLE:
                parity = 1 if parity == -1 else -1
            else:
                parity = random.choice(PARITIES)

        with KeepPos():
            modified_distance = parity * distance
            with PenUp():
                turtle.setheading(aircraft.heading)
                turtle.forward(modified_distance)

            draw_pps()

            tag = f"{aircraft.acid}\n" \
                  f"{aircraft.type}\n" \
                  f"{aircraft.altitude}    {aircraft.speed}"

            with PenUp():
                turtle.forward(parity * (RADIUS / 4))
                turtle.write(tag)


def draw_pps() -> None:
    """
    Draw a PSR/SSR Correlated PPS at current position.
    """
    triangle_side = PPS_SIDE * sqrt(3)

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
            turtle.forward(triangle_side)


def draw_scale() -> None:
    """
    Draw a scale for 1 mile.
    """
    tick_length = 10
    scale_start = (-RADIUS, RADIUS)

    with KeepPos():
        with PenUp():
            turtle.goto(scale_start)
            turtle.setheading(360)

        # draw the bracket shape
        turtle.forward(tick_length)
        turtle.setheading(90)
        turtle.forward(MILE_LENGTH)
        turtle.setheading(180)
        turtle.forward(tick_length)

        with PenUp():
            turtle.goto(scale_start[0] + MILE_LENGTH / 2, scale_start[1] + 10)

        turtle.write("1 MILE", align="center")


def initialize() -> None:
    """
    Run initial setup for turtle.
    """
    turtle.mode('logo')
    turtle.hideturtle()
    turtle.speed(0)
    turtle.onscreenclick(draw)


def reset() -> None:
    """
    Clear the screen and put the pen back at the origin.
    """
    turtle.clear()
    turtle.setheading(360)
    turtle.home()


def draw(*args) -> None:
    """
    Draw the radar, heading lines, and PPS (with data tags).
    """
    reset()
    draw_circle()
    headings = random.uniform(*HEADING_RANGE), random.uniform(*HEADING_RANGE)
    draw_lines(*headings)
    place_pps(generate_aircraft(*headings))
    draw_scale()


def main() -> None:
    initialize()
    draw()


if __name__ == '__main__':
    main()
    turtle.mainloop()
