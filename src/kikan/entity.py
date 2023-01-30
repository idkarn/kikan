from .math import Vertex

class Entity:
    def __init__(self, position: Vertex, texture: str):
        # self.id = len(entities)
        self.pos = position
        self.texture = texture