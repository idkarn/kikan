from kikan import engine, Entity, Vector
from kikan.entity import StepSides
from kikan.utils import Logger


class Player(Entity):
    def on_input(self, key):
        match key:
            case "a":
                self.step(StepSides.LEFT)
            case "d":
                self.step(StepSides.RIGHT)
            case "s":
                self.step(StepSides.DOWN)
            case "w":
                self.step(StepSides.UP)


class NPC(Entity):
    is_right_direction = True

    def on_update(self):
        if self.position.x == 4:
            self.is_right_direction = False
        elif self.position.x == -4:
            self.is_right_direction = True
        self.step(StepSides.RIGHT if self.is_right_direction else StepSides.LEFT)

    def on_collision(self, other):
        if other is player:
            self.destroy()


npc = NPC(Vector(0, 0), "NPC")
player = Player(Vector(0, 3), "P")

engine.start()
