from dataclasses import dataclass
from typing import Iterator, Tuple
from math import copysign


@dataclass
class Vertex:  # find out why int instead of float
    x: int
    y: int
    z: int

    def __init__(self, x: float, y: float, z: float = 0) -> None:
        self.x, self.y, self.z = int(x), int(y), int(z)

    def get_projection(self, scale: int):
        x_proj = (scale * self.x) // (self.z + scale + 50)
        y_proj = (scale * self.y) // (self.z + scale + 50)
        return Vertex(x_proj, y_proj)

    def to_matrix(self):
        return [
            [self.x],
            [self.y],
            [self.z]
        ]


class Edge:
    def __init__(self, start: Vertex, end: Vertex) -> None:
        self.start, self.end = start, end


class Matrix:
    @staticmethod
    def multiply(a: list[list], b: list[list]) -> list[list]:
        return [[sum(a * b for a, b in zip(A_row, B_col))
                 for B_col in zip(*b)] for A_row in a]


def sign(n: int) -> -1 or 0 or 1:
    return int(copysign(1, n)) if n != 0 else 0


# algorithm from https://www.uobabylon.edu.iq/eprints/publication_2_22893_6215.pdf
def get_line_coords(x1: int, y1: int, x2: int, y2: int) -> Iterator[Tuple[int, int]]:
    x, y = x1, y1
    dx, dy = abs(x2 - x1), abs(y2 - y1)
    sx, sy = sign(x2 - x1), sign(y2 - y1)
    ichg = False

    if dy > dx:
        dx, dy = dy, dx
        ichg = True

    e = 2*dy - dx
    a = 2*dy
    b = 2*dy - 2*dx

    # in the original loop starts with 1, this causes an bug when y=0 is not returned
    for i in range(1, dx):
        if e < 0:
            if ichg:
                y += sy
            else:
                x += sx
            e += a
        else:
            y += sy
            x += sx
            e += b
        yield x, y
