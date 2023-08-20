import time
from enum import Enum
from .main import engine
from .math import Vector


class StepSides(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class Entity:
    # noinspection PyTypeChecker
    def __init__(self, position: Vector, texture: str) -> None:
        self.mass = 1
        self.position = position
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)

        self.texture = texture
        self.prev_pos: Vector = None
        self.__is_hidden: bool = False
        self.__id: int = id(self)
        engine.game_world.record_entity(self)

        self.__prev_timestamp: float = time.time()

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
