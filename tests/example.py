from kikan import engine, Entity, Vector
from kikan.utils import Logger


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


npc = NPC(Vector(0, 0), "NPC")
player = Player(Vector(0, 3), "P")

engine.start()
