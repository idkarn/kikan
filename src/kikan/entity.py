import time
from .math import Vector
from .main import engine
from enum import Enum


class STEP_SIDE(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class Entity:
    def __init__(self, position: Vector, texture: str) -> None:
        self.mass = 1
        self.pos = position
        self.velocity = Vector(0, 0)
        self.accel = Vector(0, 0)

        self.texture = texture
        self.prev_pos: Vector | None = None
        self.__is_hidden: bool = False
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
        self.__is_hidden = True

    def show(self):
        self.__is_hidden = False


class MetaEntity:
    """A class for game objects that have no instances of their own. These subclasses can handle events like the other entities."""

    def __init_subclass__(cls) -> None:
        engine.game_world.meta_entities.append(cls)

    def destroy(self):
        engine.game_world.meta_entities.remove(self)
        del self


EmptyObject = MetaEntity
