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
    def __init__(self, world_map: WorldMap, entities: list[Entity] = None):
        if entities is None:
            entities = []
        self.map = world_map
        self.entities: SortedDict[int, Entity] = SortedDict()
        for e in entities:
            self.entities[id(e)] = e
        self.meta_entities: SortedDict[int, Entity] = SortedDict()

    def record_entity(self, entity: Entity):
        self.entities[id(entity)] = entity

    def place(self, position: Vector, texture: str):
        self.map.config.append(WorldObject(position, texture))
