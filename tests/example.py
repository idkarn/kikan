from kikan import engine, Entity, Vector
from kikan.entity import EmptyObject


class NPC(Entity):
    def __init__(self, pos, tex):
        super().__init__(pos, tex)
        self.phase = 0

    def on_update(self):
        match self.phase:
            case 0:
                self.step("right")
            case 1:
                self.step("up")
            case 2:
                self.step("left")
            case 3:
                self.step("down")
        self.phase += 1
        if self.phase == 4:
            self.phase = 0


class DisplayManager(EmptyObject):
    ticks = 0

    @classmethod
    def on_update(cls):
        display.texture = str(cls.ticks)
        cls.ticks += 1


class Display(Entity):
    def __init__(self):
        super().__init__(Vector(-30, 10), "")


npc = NPC(Vector(0, 0), "NPC")
display = Display()

engine.start()
