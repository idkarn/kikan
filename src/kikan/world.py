from .entity import Entity
from .math import Vector


class WorldObject:
    def __init__(self, position: Vector, texture: str):
        self.texture = texture
        self.position = position


class WorldMap:
    def __init__(self, config: list[WorldObject]):
        self.config = config


class World:
    def __init__(self, world_map: WorldMap, entities: dict[int, Entity]):
        self.entities = entities
        self.map = world_map
