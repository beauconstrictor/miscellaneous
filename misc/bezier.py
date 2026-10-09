import math
import turtle
from typing import TypeAlias

GRAB_RADIUS = 100 # grabbable size of handles
HANDLE_SIZE = 10  # visible size of handles

coord: TypeAlias = tuple[float, float]

def lerp(a: coord, b: coord, t: float) -> coord:
    return (a[0] + (b[0]-a[0]) * t,
            a[1] + (b[1]-a[1]) * t)

def dist(a: coord, b: coord) -> float:
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return math.sqrt(dx**2 + dy**2)

class Bezier(turtle.Turtle):
    def __init__(self, a1: coord, a2: coord, b1: coord, b2: coord) -> None:
        super().__init__()

        self.color("white")
        self.hideturtle()
        self.shapesize(HANDLE_SIZE/20)

        self.a1 = a1
        self.a2 = a2
        self.b1 = b1
        self.b2 = b2

    def sample(self, t: float) -> coord:
        a1, a2, b1, b2 = self.a1, self.a2, self.b1, self.b2
        a = lerp(a1, a2, t)
        b = lerp(b1, b2, t)
        c = lerp(a2, b1, t)
        d = lerp(a, c, t)
        e = lerp(c, b, t)
        f = lerp(d, e, t)
        return f
    
    def draw(self, n: int) -> None:
        self.penup()
        self.pensize(2)
        for t in (i / (n-1) for i in range(n)):
            self.goto(self.sample(t))
            self.pendown()

    def draw_handles(self) -> None:
        self.pensize(1)

        for i in [("a1", "a2"), ("b2", "b1")]:

            self.penup()
            self.goto(getattr(self, i[0]))
            self.shape("circle")
            self.stamp()
            self.setheading(self.towards(getattr(self, i[1])))
            self.pendown()
            self.goto(getattr(self, i[1]))
            self.shape("classic")
            self.stamp()

class App:
    def __init__(self) -> None:
        turtle.tracer(False)
        turtle.bgcolor("black")

        self.screen = turtle.Screen()
        self.canvas = self.screen.getcanvas()

        self.bezier = Bezier((-200,-100), (-100,100), (100,100), (200,-100))
        self.draw()

        self.dragging = None

    def draw(self) -> None:
        self.bezier.clear()
        self.bezier.draw(GRAB_RADIUS)
        self.bezier.draw_handles()
        turtle.update()

    def begin_drag(self, event) -> None:
        x = event.x - self.screen.window_width() / 2
        y = self.screen.window_height() / 2 - event.y
        pos: coord = (x, y)

        draggables = ["a1", "a2", "b1", "b2"]
        for i in draggables:
            if dist(pos, getattr(self.bezier, i)) < GRAB_RADIUS:
                self.dragging = i
                break

    def drag(self, event) -> None:
        if self.dragging is None: return

        x = event.x - self.screen.window_width() / 2
        y = self.screen.window_height() / 2 - event.y
        pos: coord = (x, y)

        setattr(self.bezier, self.dragging, pos)

        self.draw()

    def end_drag(self, event) -> None:
        self.dragging = None

    def start(self) -> None:
        self.canvas.bind("<Button-1>", self.begin_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)
        turtle.mainloop()

if __name__ == "__main__":
    App().start()
