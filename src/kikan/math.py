from dataclasses import dataclass
from typing import Iterator, Tuple
import math


# arithmetic operations from https://github.com/philiprbrenan/Vector2/blob/master/Vector2.py
@dataclass
class Vector:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float = 0) -> None:
        self.x, self.y, self.z = x, y, z

    def get_projection(self, scale: int):
        x_proj = (scale * self.x) // (self.z + scale + 50)
        y_proj = (scale * self.y) // (self.z + scale + 50)
        return Vector(x_proj, y_proj)

    def to_matrix(self):
        return [
            [self.x],
            [self.y],
            [self.z]
        ]

    def length(self):
        """Length of a vector"""
        return (self.x**2 + self.y**2) ** 0.5

    def normalize(self):
        """Normalize a vector"""
        l = self.length()
        return self / l if l else self

    def dot(self, other):
        """Dot product of two vectors"""
        products = [s * o for s,
                    o in zip(self._get_coords(), other._get_coords())]
        dot_sum = sum(products)
        return dot_sum

    def _get_coords(self):
        return (self.x, self.y, self.z)

    def __add__(self, other):
        """Add the second vector to a copy of the first vector"""
        coords = [s + o for s, o in zip(
            self._get_coords(), other._get_coords())]
        new_vertex = Vector(*coords)
        return new_vertex

    def __sub__(self, other):
        """Subtract the second vector from a copy of the first vector"""
        coords = [s - o for s, o in zip(
            self._get_coords(), other._get_coords())]
        new_vertex = Vector(*coords)
        return new_vertex

    def __mul__(self, n: float):
        """Multiply a copy of vector by a scalar"""
        coords = [i * n for i in self._get_coords()]
        new_vertex = Vector(*coords)
        return new_vertex

    def __truediv__(self, n: float):
        """Divide a copy of a vector by a scalar"""
        coords = [i / n for i in self._get_coords()]
        new_vertex = Vector(*coords)
        return new_vertex

    def __floordiv__(self, n: float):
        """Same as a true div"""
        return self / n

    def __abs__(self):
        """Length of a vector"""
        return self.length()

    def __len__(self):
        """Length of a vector"""
        return self.length()

    def __neg__(self):
        """Rotate a copy of a vector by 180 degrees"""
        coords = [-i for i in self._get_coords()]
        new_vertex = Vector(*coords)
        return new_vertex


class Matrix:
    @staticmethod
    def multiply(a: list[list], b: list[list]) -> list[list]:
        return [[sum(a * b for a, b in zip(A_row, B_col))
                 for B_col in zip(*b)] for A_row in a]


# algorithm from https://www.uobabylon.edu.iq/eprints/publication_2_22893_6215.pdf
def get_line_coords(x1: float, y1: float, x2: float, y2: float) -> Iterator[Tuple[int, int]]:
    def sign(n: int) -> -1 or 0 or 1:
        return int(math.copysign(1, n)) if n != 0 else 0

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
    i = 1
    while i < dx:
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
        i += 1
