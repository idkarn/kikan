from __future__ import annotations

import time
from .math import Vector
from .main import engine
from enum import Enum
from typing import Generic, List, Tuple, TypeVar


RGBType = Tuple[int, int, int]
PositionType = TypeVar("PositionType", None, Vector, None | Vector)


class STEP_SIDE(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class Entity:
    def __init__(self, position: Vector, texture: Texture | str) -> None:
        self.mass = 1
        self.pos = position
        self.velocity = Vector(0, 0)
        self.accel = Vector(0, 0)

        if isinstance(texture, str):
            self.texture: Texture = Texture([[Pixel(texture)]])
        else:
            self.texture: Texture = texture
        self.prev_pos: Vector | None = None
        self._is_hidden: bool = False
        self.__id: int = id(self)
        engine.game_world.record_entity(self)

        self.__prev_timestamp: float = time.time()

    def _update(self):
        self.prev_pos = Vector(self.pos.x, self.pos.y)

        dt = time.time() - self.__prev_timestamp
        self.velocity += self.accel * dt
        self.accel = Vector(0, 0)
        self.pos += self.velocity * dt

        self.__prev_timestamp = time.time()

    def apply_force(self, force: Vector):
        self.accel += force / self.mass

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
        engine.game_world.entities.remove(self)
        del self

    def hide(self):
        self._is_hidden = True

    def show(self):
        self._is_hidden = False


class MetaEntity:
    """A class for game objects that have no instances of their own. These subclasses can handle events like the other entities."""

    def __init_subclass__(cls) -> None:
        engine.game_world.meta_entities.append(cls)

    def destroy(self):
        engine.game_world.meta_entities.remove(self)
        del self


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
    def __init__(self, symbol: str, color: RGBType | None = None, position: PositionType = None):
        if len(symbol) > 1:
            raise Exception("Only one character is allowed for pixel's symbol")
        self.symbol: str = symbol
        self.color: RGBType = color or (255, 255, 255)
        self.position: PositionType = position

    def __repr__(self) -> str:
        return f'<Pixel for "{self.symbol}" of {self.color} at {self.position}>'
