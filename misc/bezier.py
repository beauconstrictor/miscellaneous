import math
import turtle
from typing import TypeAlias

GRAB_RADIUS  = 100     # grabbable size of handles
HANDLE_SIZE  = 15      # visible size of handles
CURVE_DETAIL = (2, 50) # range allowed

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
        r0 = lerp(a1, a2, t)
        r1 = lerp(a2, b1, t)
        r2 = lerp(b1, b2, t)

        p0 = lerp(r0, r1, t)
        p1 = lerp(r1, r2, t)

        return lerp(p0, p1, t)
    
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
            self.shapesize(HANDLE_SIZE/20/1.4)
            self.color("black")
            self.stamp()
            self.shapesize(HANDLE_SIZE/20)
            self.color("white")
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

        self.dragging = None
        self.detail   = CURVE_DETAIL[1]

        self.bezier = Bezier((-200,-100), (-100,100), (100,100), (200,-100))
        self.draw()

    def draw(self) -> None:
        self.bezier.clear()
        self.bezier.draw(self.detail)
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

    
    def scroll_up(self, event) -> None:
        self.detail += 1
        self.detail = min(self.detail, CURVE_DETAIL[1])
        self.draw()

    def scroll_down(self, event) -> None:
        self.detail -= 1
        self.detail = max(self.detail, CURVE_DETAIL[0])
        self.draw()

    def scroll(self, event) -> None:
        print(event.delta)

        if event.delta > 0:
            self.scroll_up(event)
        elif event.delta < 0:
            self.scroll_down(event)

    def start(self) -> None:
        self.canvas.bind("<MouseWheel>", self.scroll)
        self.canvas.bind("<Button-4>", self.scroll_up)
        self.canvas.bind("<Button-5>", self.scroll_down)
        self.canvas.bind("<Button-1>", self.begin_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)
        turtle.mainloop()

if __name__ == "__main__":
    App().start()
