from kikan import engine, Entity, Vector
from kikan.utils import Logger
from kikan.entity import Texture, Pixel

NPCTexture = Texture([
    Pixel("N", (255, 0, 0), Vector(0, 0)),
    Pixel("P", (0, 255, 0), Vector(0, 1)),
    Pixel("C", (0, 0, 255), Vector(0, 2))
])


class Player(Entity):
    def on_input(self, key):
        match key:
            case "a":
                self.step("left")
            case "d":
                self.step("right")
            case "s":
                self.step("down")
            case "w":
                self.step("up")


class NPC(Entity):
    is_right_direction = True

    def on_update(self):
        if self.pos.x == 4:
            self.is_right_direction = False
        elif self.pos.x == -4:
            self.is_right_direction = True
        self.step("right" if self.is_right_direction else "left")

    def on_collision(self, other):
        if other is player:
            self.destroy()


npc = NPC(Vector(0, 0), NPCTexture)
player = Player(Vector(0, 3), "P")

engine.start()
