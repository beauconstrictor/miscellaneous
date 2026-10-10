from pprint import pprint
from enum import Enum
import random
import turtle

type coord = tuple[int, int]

class Cell(Enum):
    PASSABLE   = " "
    IMPASSABLE = "#"
    START      = "S"
    FINISH     = "F"

CELL_SIZE = 20
COLOUR_MAP = {
        Cell.PASSABLE:   (1,   1,  1),
        Cell.IMPASSABLE: (0.5, 0.5, 0.5),
        Cell.FINISH:     (1,   0,   0),
        Cell.START:      (0,   1,   0),
}

WIDTH, HEIGHT = 20, 15

class EvaluatedCell:
    def __init__(self, c: coord, maze: Maze, parent: coord|None) -> None:
        self.c = c
        self.maze = maze
        self.parent = parent
    
    def g(self) -> int:
        return 0 if self.parent is None else self.parent.g() + 1

    def h(self) -> int:
        # manhattan distance
        dx = abs(self.c[0] - self.maze.finish[0])
        dy = abs(self.c[1] - self.maze.finish[1])
        return dx + dy

    def f(self) -> int:
        return self.h() + self.g()

class Maze:
    def __init__(self) -> None:
        self.grid = [[Cell.PASSABLE for i in range(WIDTH)] for i in range(HEIGHT)]
        self.alterations = {}
        self.start = None
        self.finish = None

    def set_cell(self, c: coord, value: Cell) -> None:
        self.alterations[c] = value
        self.grid[c[1]][c[0]] = value
        if value == Cell.START:  self.start  = c
        if value == Cell.FINISH: self.finish = c

    def at(self, c: coord) -> Cell:
        return self.grid[c[1]][c[0]]

    def render(self, path: list[coord]|None=None) -> str:
        maze = [[cell.value for cell in row] for row in self.grid]

        if path:
            for cell in path:
                maze[cell[1]][cell[0]] = "+"

        return "\n".join("".join(row) for row in maze)

    def __repr__(self) -> str:
        return self.render(None)

    def a_star(self) -> list[coord]|None:
        open_list   = [EvaluatedCell(self.start, self, None)]
        closed_list = []

        while len(open_list) > 0:
            open_list.sort(key=lambda c: c.f())

            q = open_list.pop(0)
            closed_list.append(q)

            for d in (1, 0), (0, 1), (-1, 0), (0, -1):
                c = q.c[0]+d[0], q.c[1]+d[1]

                if not (0 <= c[0] < WIDTH):       continue
                if not (0 <= c[1] < HEIGHT):      continue
                if self.at(c) == Cell.IMPASSABLE: continue

                if any(cell.c == c for cell in open_list):   continue
                if any(cell.c == c for cell in closed_list): continue

                cell = EvaluatedCell(c, self, q)

                if cell.c == self.finish:
                    path = []
                    while cell.parent is not None:
                        cell = cell.parent
                        path.append(cell.c)
                    path.pop() # remove start from path
                    return reversed(path)
                else:
                    open_list.append(cell)

        return None

def plot_square(c: coord) -> None:
    x, y = c
    turtle.goto(x*CELL_SIZE-WIDTH*CELL_SIZE/2, HEIGHT*CELL_SIZE/2-y*CELL_SIZE)
    turtle.stamp()

def main() -> None:
    maze = Maze()

    maze.set_cell((0, 0), Cell.START)
    maze.set_cell((19, 14), Cell.FINISH)

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (x, y) != maze.start and (x, y) != maze.finish:
                if random.random() < 0.25:
                    maze.set_cell((x, y), Cell.IMPASSABLE)

    turtle.color("black")
    turtle.shape("square")
    turtle.penup()
    turtle.shapesize(CELL_SIZE/20)
    turtle.hideturtle()
    turtle.tracer(False)

    for x in range(-1, WIDTH+1):
        plot_square((x, -1))
        plot_square((x, HEIGHT))
    for y in range(-1, HEIGHT+1):
        plot_square((-1, y))
        plot_square((WIDTH, y))

    for y, row in enumerate(maze.grid):
        for x, cell in enumerate(row):
            turtle.color( COLOUR_MAP[cell])
            plot_square((x, y))

    path = maze.a_star()
    if path is None:
        turtle.goto(0, 0)
        turtle.color("red")
        turtle.write("No path found!", align="center", font=("Arial", 24, "bold"))
        turtle.Screen().ontimer(main, 3000)
        return

    turtle.update()
    turtle.tracer(True)

    turtle.speed(1)

    for c in path:
        turtle.color((1, 1, 0))
        plot_square(c)
        turtle.showturtle()

    turtle.Screen().ontimer(main, 1000)

if __name__ == "__main__":
    main()
    turtle.done()
