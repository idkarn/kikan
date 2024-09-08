from __future__ import annotations

import time
from enum import Enum
from typing import Generic, List, Tuple, TypeVar
from .main import engine
from .math import Vector
from .states import StateManager


RGBType = Tuple[int, int, int]
PositionType = TypeVar("PositionType", None, Vector, None | Vector)


class StepSides(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class Entity:
    # noinspection PyTypeChecker
    def __init__(self, position: Vector, texture: Texture | str) -> None:
        self.mass = 1
        self.position = position
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)

        if isinstance(texture, str):
            self.texture: Texture = Texture([[Pixel(texture)]])
        else:
            self.texture: Texture = texture
        self.prev_pos: Vector | None = None
        self._is_hidden: bool = False
        self.__id: int = id(self)
        self._is_destroyed = False
        engine.game_world.record_entity(self)

        self.__prev_timestamp: float = time.time()

        for attr_name in dir(self):
            attrs = dir(attr_value := getattr(self, attr_name))
            if "_subscribed_on" in attrs:
                attr_value._subscribed_on.subscribe(attr_value)
            if "_affected_by" in attrs:
                StateManager.subscribe(attr_value._affected_by, attr_value)

    def _update(self):
        self.prev_pos = Vector(self.position.x, self.position.y)

        dt = time.time() - self.__prev_timestamp
        self.velocity += self.acceleration * dt
        self.acceleration = Vector(0, 0)
        self.position += self.velocity * dt

        self.__prev_timestamp = time.time()

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
        self._is_destroyed = True

    def hide(self):
        self._is_hidden = True

    def show(self):
        self._is_hidden = False


class MetaEntity:
    """A class for game objects that have no instances of their own. These subclasses can handle events like the
    other entities."""

    def __init_subclass__(cls) -> None:
        cls._is_destroyed = False
        engine.game_world.meta_entities[id(cls)] = cls

    @classmethod
    def destroy(cls):
        cls._is_destroyed = True


# alias for MetaEntity
EmptyObject = MetaEntity


class Texture:
    tiles: List[Pixel[Vector]]

    def __init__(self, pixels: List[List[Pixel[None | Vector]]] | List[Pixel[Vector]]):
        if isinstance(pixels[0], list):
            self.tiles = []
            for y in range(len(pixels)):
                pixel: Pixel[None | Vector]
                for x in range(len(pixels[y])):
                    if (pixel := pixels[y][x]) == None:
                        continue
                    pixel.position = Vector(x, y)
                    self.tiles.append(pixel)
        else:
            self.tiles = pixels

    def add_tile(self, pixel: Pixel[Vector]):
        self.tiles.append(pixel)


class Pixel(Generic[PositionType]):
    def __init__(
        self, symbol: str, color: RGBType | None = None, position: PositionType = None
    ):
        if len(symbol) > 1:
            raise Exception("Only one character is allowed for pixel's symbol")
        self.symbol: str = symbol
        self.color: RGBType = color or (255, 255, 255)
        self.position: PositionType = position

    def __repr__(self) -> str:
        return f'<Pixel for "{self.symbol}" of {self.color} at {self.position}>'
