import curses
from math import cos, sin
from .math import Matrix, Vertex, get_line_coords
from os import get_terminal_size


class Screen:
    def __init__(self) -> None:
        self.scr = curses.initscr()
        term_size = get_terminal_size()
        self.size = {
            "height": term_size.lines,
            "width": term_size.columns
        }
        curses.noecho()
        curses.start_color()
        self.scr.erase()

    def display_symbol(self, x: int, y: int, symbol: str, color: int = 0):
        if abs(x) < self.size["width"] // 2 and abs(y) < self.size["height"] // 2:
            # print(x, y)
            # translate x, y from a center to the curses coords system
            x, y = self.size["width"] // 2 + x, self.size["height"] // 2 - y
            self.scr.addch(y, x, symbol, curses.color_pair(color))
            self.scr.refresh()

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, symb: str = "*", color: int = 0) -> None:
        for x, y in get_line_coords(x1, y1, x2, y2):
            self.display_symbol(x, y, symb, color)

    def get_key(self) -> str:
        return self.scr.getkey()

    def draw_wireframe(self, vertexes: list[Vertex], edges: list, angle: float, scale: int = 1, color: int = 0) -> None:
        rotation = [
            [cos(angle), 0, sin(angle)],
            [0, 1, 0],
            [-sin(angle), 0, cos(angle)]
        ]

        projected_verts: list[Vertex] = []
        for vert in vertexes:
            rotated_matrix = Matrix.multiply(rotation, vert.to_matrix())
            rotated_vert = Vertex(
                rotated_matrix[0][0],
                rotated_matrix[1][0],
                rotated_matrix[2][0],
            )

            vert_proj: Vertex = rotated_vert.get_projection(scale)
            projected_verts.append(vert_proj)
            self.display_symbol(vert_proj.x, vert_proj.y, "*", color)

        for s, e in edges:
            s_vert = projected_verts[s]
            e_vert = projected_verts[e]
            self.draw_line(s_vert.x, s_vert.y, e_vert.x, e_vert.y, "*", color)
