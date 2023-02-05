
class WorldObject:
    def __init__(self):
        self.texture = ""


class Map:
    def __init__(self):
        self.config: list[WorldObject] = []


class World:
    def __init__(self):
        self.entities = []
        self.map = Map()
