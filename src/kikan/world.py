# typing setting up
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from .math import Vector
    from .entity import Entity
# typing setting up

from sortedcontainers import SortedDict


class WorldObject:
    def __init__(self, position: Vector, texture: str):
        self.texture = texture
        self.position = position


class WorldMap:
    def __init__(self, config: list[WorldObject]):
        # TODO: replace config list with dictionary of position and WorldObject
        self.config = config


class World:
    def __init__(self, map: WorldMap, entities: list[Entity] = None):
        self.map = map
        self.entities = entities or []  # TODO: replace list with SortedDict
        self.meta_entities = []

    def record_entity(self, entity: Entity):
        if entity not in self.entities:
            self.entities.append(entity)

    def place(self, position: Vector, texture: str):
        self.map.config.append(WorldObject(position, texture))
