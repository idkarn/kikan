from blessed import Terminal
from math import cos, sin
from .math import Matrix, Vector, get_line_coords
from os import get_terminal_size
from .entity import Entity


class Screen:
    def __init__(self, delay) -> None:
        self.scr = Terminal()
        self.delay = delay
        term_size = get_terminal_size()
        self.size = {
            "height": term_size.lines,
            "width": term_size.columns
        }
        self.terminal_contexts = (self.scr.fullscreen(
        ), self.scr.cbreak(), self.scr.hidden_cursor())
        for option in self.terminal_contexts:
            option.__enter__()
        self.clear()

    def terminate_terminal(self) -> None:
        for option in self.terminal_contexts:
            option.__exit__(None, None, None)

    # probably must be private for internal usage only
    def render(self, data: str):
        print(data, end='', flush=True)

    def draw(self, entity: Entity):
        self.display_symbol(entity.pos.x, entity.pos.y, entity.texture)

    def display_symbol(self, x: int, y: int, symbol: str, color: tuple[int, int, int] = (255, 255, 255)):
        if abs(x) < self.size["width"] // 2 and abs(y) < self.size["height"] // 2:
            # translate x, y from a center to the curses coords system
            x, y = self.size["width"] // 2 + x, self.size["height"] // 2 - y
            self.frame[y][x] = self.scr.color_rgb(*color) + symbol

    def display_string(self, x: int, y: int, s: str, color: tuple[int, int, int] = (255, 255, 255)):
        for shift in range(len(s)):
            self.display_symbol(x + shift, y, s[shift], color)

    # TODO: make color args more convenient (make it optional)

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, symb: str = "*", color: tuple[int, int, int] = (255, 255, 255)) -> None:
        for x, y in get_line_coords(x1, y1, x2, y2):
            self.display_symbol(x, y, symb, color)

    def get_key(self) -> str:
        return self.scr.inkey(self.delay).lower()

    def clear(self) -> None:
        self.frame = [[" " for _ in range(self.size["width"])]
                      for _ in range(self.size["height"])]

    def update(self) -> None:
        for row in self.frame:
            for symb in row:
                self.render(symb)
        self.clear()

    def draw_wireframe(self, vertexes: list[Vector], edges: list, angle: float, scale: int = 1, color: tuple[int, int, int] = (255, 255, 255)) -> None:
        rotation = [
            [cos(angle), 0, sin(angle)],
            [0, 1, 0],
            [-sin(angle), 0, cos(angle)]
        ]

        projected_verts: list[Vector] = []
        for vert in vertexes:
            rotated_matrix = Matrix.multiply(rotation, vert.to_matrix())
            rotated_vert = Vector(
                rotated_matrix[0][0],
                rotated_matrix[1][0],
                rotated_matrix[2][0],
            )

            vert_proj: Vector = rotated_vert.get_projection(scale)
            projected_verts.append(vert_proj)
            self.display_symbol(vert_proj.x, vert_proj.y, "*", color)

        for s, e in edges:
            s_vert = projected_verts[s]
            e_vert = projected_verts[e]
            self.draw_line(s_vert.x, s_vert.y, e_vert.x, e_vert.y, "*", color)
