from pprint import pprint
from enum import Enum

WIDTH, HEIGHT = 8, 4

type coord = tuple[int, int]

class Cell(Enum):
    PASSABLE   = " "
    IMPASSABLE = "#"
    START      = "S"
    FINISH     = "F"

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

    def a_star(self) -> list[coord]:
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
                    return path
                else:
                    open_list.append(cell)

if __name__ == "__main__":
    maze = Maze()
    
    maze.set_cell((0, 0), Cell.START)
    maze.set_cell((7, 3), Cell.FINISH)
    for i in range(4): maze.set_cell((4+i, 0), Cell.IMPASSABLE)
    for i in range(3): maze.set_cell((5+i, 1), Cell.IMPASSABLE)
    for i in range(2): maze.set_cell((0+i, 2), Cell.IMPASSABLE)
    for i in range(2): maze.set_cell((3+i, 2), Cell.IMPASSABLE)
    maze.set_cell((0, 3), Cell.IMPASSABLE)

    path = maze.a_star()
    print(maze.render(path))
