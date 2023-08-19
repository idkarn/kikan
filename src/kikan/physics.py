from dataclasses import dataclass
from kikan.entity import Entity


@dataclass
class PhysicsWorldConfig:
    FREE_FALL_FORCE: float = 9.81


class PhysicsEnvironment:
    def __init__(self, entity):
        self.config = PhysicsWorldConfig()

    def tick(self, entity: Entity):
        entity.position += entity.velocity
