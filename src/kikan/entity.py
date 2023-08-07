from abc import abstractmethod
from inspect import getmembers, isfunction
import time
from .math import Vector
from enum import Enum


class STEP_SIDE(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class Entity:
    def __init__(self, position: Vector, texture: str) -> None:
        methods = getmembers(self.__class__, predicate=isfunction)
        for name, method in methods:
            method._self = self
        entities.append(self)
        self.pos = position
        self.speed = Vector(0, 0)

        self.texture = texture
        self.prev_pos: Vector = None
        self.__is_hidden: bool = False
        self.__id: int = len(entities)

        self.__prev_timestamp: float = 0
        """The value updates only at the end of `_update` code, including user-defined `update` function"""

    def pre_update(self):
        """The method can be implemented by the user"""
        ...

    def _update(self):
        self.pre_update()

        self.prev_pos = Vector(self.pos.x, self.pos.y)

        dt = time.time() - self.__prev_timestamp
        self.pos += self.speed * dt

        self.update()

        self.__prev_timestamp = time.time()

    def apply_force(self):
        ...

    def update(self, *args, **kwargs) -> None:
        """The method can be implemented by the user"""
        ...

    def step(self, side: STEP_SIDE):
        match side:
            case STEP_SIDE.LEFT.value:
                self.pos.x -= 1
            case STEP_SIDE.RIGHT.value:
                self.pos.x += 1
            case STEP_SIDE.DOWN.value:
                self.pos.y -= 1
            case STEP_SIDE.UP.value:
                self.pos.y += 1

    def destroy(self):
        entities.pop(self.__id)
        del self

    def hide(self):
        self.__is_hidden = True

    def show(self):
        self.__is_hidden = False


entities: list[Entity] = []
