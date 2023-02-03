from inspect import getmembers
import inspect
from .math import Vertex


entities = []


class Entity:
    def __init__(self, position: Vertex, texture: str) -> None:
        methods = getmembers(self.__class__, predicate=inspect.isfunction)
        for name, method in methods:
            method._self = self
        entities.append(self)
        self.pos = position
        self.texture = texture
