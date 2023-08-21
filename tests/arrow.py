from math import ceil
from random import randint, random
from kikan import engine, Entity, Vector
from kikan.entity import MetaEntity, Pixel, Texture
from kikan.math import Vector
from kikan.utils import Logger


class Range(Entity):
    def __init__(self, center, pattern):
        super().__init__(center, "")
        self.pattern: str = pattern
        self.green_zones = []
        self.red_zones = []
        l = len(pattern)
        for i in range(l):
            x = ceil(-l / 2 + i)
            self.texture.add_tile(
                Pixel("=", (255, 0, 0) if pattern[i] == "R" else (0, 255, 0), Vector(x, 0)))
            if pattern[i] == "G":
                self.green_zones.append(x)
            else:
                self.red_zones.append(x)
        self.borders = (ceil(-l / 2), ceil(l / 2) - 1)


class Arrow(Entity):
    def __init__(self) -> None:
        super().__init__(Vector(0, -1), Texture([[Pixel("^", (0, 0, 255))]]))
        self.score = 0
        self.velocity = Vector(5, 0)
        self.is_invincible = False
        self.ticks = 0
        self.ticks_stamp = 0
        self.factor = 1

    def on_input(self, key):
        if key != " ":
            return
        if round(self.position.x) in range_.green_zones:
            self.score += 1 * self.factor
        elif round(self.position.x) in range_.red_zones and not self.is_invincible:
            self.score = max(self.score - 1 * self.factor, 0)
        if self.factor != 1:
            self.factor = 1

    def on_update(self):
        if self.position.x <= range_.borders[0]:
            self.velocity = Vector(5 + self.score / 10, 0)
        elif self.position.x >= range_.borders[1]:
            self.velocity = Vector(-5 - self.score / 10, 0)
        if self.is_invincible and self.ticks >= self.ticks_stamp + 20:
            self.is_invincible = False
        self.ticks += 1


class Score(MetaEntity):
    score_stamp = 0
    effect = ""

    @classmethod
    def on_update(cls):
        if arrow.score % 10 == 0 and arrow.score > cls.score_stamp:
            new_pattern = range_.pattern.replace("G", "R", 1)
            Logger.print(
                f"Removed a green zone; new pattern is {new_pattern}")
            range_.destroy()
            create_range(new_pattern)
            cls.score_stamp = arrow.score

        if random() >= 0.97:
            create_star()

        engine.screen.display_string(-4, 5, f'Score: {arrow.score}')
        if cls.effect:
            engine.screen.display_string(-4, 4, f"Effect: {cls.effect}")

    @classmethod
    def on_input(cls, key):
        if key == "q":
            exit()
        elif key == "r":
            global arrow
            arrow.destroy()
            arrow = Arrow()
            create_range("RRRRRRGGGGGGGRRRRRR")
            cls.score_stamp = 0


class Star(Entity):
    def __init__(self, position) -> None:
        super().__init__(position, Texture([[Pixel("*", (102, 153, 255))]]))

    # add 1 green zone
    # invicible
    # multiply score for next hit

    def on_input(self, key):
        if key == " " and round(arrow.position.x) == self.position.x:
            match randint(0, 2):
                case 0:
                    create_range(range_.pattern.replace("R", "G", 1))
                    Score.effect = "Replaced red zone with green"
                case 1:
                    arrow.is_invincible = True
                    arrow.ticks_stamp = arrow.ticks
                    Score.effect = "Invincibility"
                case 2:
                    arrow.factor = 3
                    Score.effect = "Hit multiplier"


def create_star():
    global star
    l = round(len(range_.pattern)/2)
    if star:
        star.destroy()
    star = Star(Vector(randint(-l, l), 0))


def create_range(pattern):
    global range_
    range_ = Range(Vector(0, 0), pattern)


arrow = Arrow()
create_range("RRRRRRGGGGGGGRRRRRR")
star = None

engine.start()
