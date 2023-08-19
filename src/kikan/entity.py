import time
from enum import Enum
from inspect import getmembers, isfunction

from .math import Vector


class StepSides(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class Entity:
    # noinspection PyTypeChecker
    def __init__(self, position: Vector, texture: str) -> None:
        methods = getmembers(self.__class__, predicate=isfunction)
        for name, method in methods:
            method._self = self

        self.mass = 1
        self.position = position
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)

        self.texture = texture
        self.prev_pos: Vector = None
        self.__is_hidden: bool = False
        self.__id: int = id(self)
        entities[self.__id] = self

        self.__prev_timestamp = time.time()
        """The value updates only at the end of `_update` code, including user-defined `update` function"""

    def pre_update(self):
        """The method can be implemented by the user"""
        ...

    def _update(self):
        self.pre_update()

        self.prev_pos = Vector(self.position.x, self.position.y)

        dt = time.time() - self.__prev_timestamp
        self.velocity += self.acceleration * dt
        self.acceleration = Vector(0, 0)
        self.position += self.velocity * dt

        self.update()

        self.__prev_timestamp = time.time()

    def update(self) -> None:
        """The method can be implemented by the user"""
        ...

    def apply_force(self, force: Vector):
        self.acceleration += force / self.mass

    def step(self, side: StepSides):
        match side:
            case StepSides.LEFT:
                self.position.x -= 1
            case StepSides.RIGHT:
                self.position.x += 1
            case StepSides.DOWN:
                self.position.y -= 1
            case StepSides.UP:
                self.position.y += 1

    def destroy(self):
        del entities[self.__id]
        del self

    def hide(self):
        self.__is_hidden = True

    def show(self):
        self.__is_hidden = False


entities: dict[int, Entity] = {}
