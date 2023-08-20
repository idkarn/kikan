from random import randint, random
from time import time
from kikan import engine, Entity, Vector
from kikan.utils import Logger
from kikan.entity import EmptyObject, Texture, Pixel, StepSides
from kikan.world import WorldMap, WorldObject

world_map = WorldMap([
    WorldObject(Vector(-30, 10), "#"),

    WorldObject(Vector(-31, 9), "#"),
    WorldObject(Vector(-30, 9), "#"),
    WorldObject(Vector(-29, 9), "#"),

    WorldObject(Vector(-32, 8), "#"),
    WorldObject(Vector(-31, 8), "#"),
    WorldObject(Vector(-29, 8), "#"),
    WorldObject(Vector(-28, 8), "#"),

    WorldObject(Vector(-33, 7), "#"),
    WorldObject(Vector(-32, 7), "#"),
    WorldObject(Vector(-31, 7), "#"),
    WorldObject(Vector(-30, 7), "#"),
    WorldObject(Vector(-29, 7), "#"),
    WorldObject(Vector(-28, 7), "#"),
    WorldObject(Vector(-27, 7), "#"),

    WorldObject(Vector(-32, 6), "#"),
    WorldObject(Vector(-31, 6), "#"),
    WorldObject(Vector(-29, 6), "#"),
    WorldObject(Vector(-28, 6), "#"),

    WorldObject(Vector(-32, 5), "#"),
    WorldObject(Vector(-31, 5), "#"),
    WorldObject(Vector(-29, 5), "#"),
    WorldObject(Vector(-28, 5), "#")
])


def find_directions_to_target(source: Entity, target: Entity):
    h, v = "", ""
    if target.position.x > source.position.x:
        h = StepSides.RIGHT
    elif target.position.x < source.position.x:
        h = StepSides.LEFT
    if target.position.y > source.position.y:
        v = StepSides.UP
    elif target.position.y < source.position.y:
        v = StepSides.DOWN
    return h, v


class Player(Entity):
    def __init__(self):
        super().__init__(Vector(0, 0), "P")
        self.damage = 1
        self.score = 10
        self.direction = "left"
        self.weapon = "sword"

    def on_input(self, key):
        match key:
            case "left":
                self.move(StepSides.LEFT)
                self.direction = "left"
            case "right":
                self.move(StepSides.RIGHT)
                self.direction = "right"
            case "down":
                self.move(StepSides.DOWN)
            case "up":
                self.move(StepSides.UP)
            case "1":
                self.weapon = "sword"
            case "2":
                self.weapon = "boomerang"
            case "q":
                exit()

    def on_collision(self, other):
        if isinstance(other, Enemy):
            player.score = 0
            player.damage = 1
            player.position = Vector(0, 0)
            for enemy in enemies:
                enemy.to_destroy = True

    def move(self, dir):
        self.step(dir)
        sword.step(dir)


class Sword(Entity):
    P1Texture = Texture([[None, None, Pixel("<", )]])
    P2Texture = Texture([[None, Pixel("-"), Pixel("<")]])
    P3Texture = Texture([[Pixel("-"), Pixel("-"), Pixel("<")]])
    P1RTexture = Texture([[Pixel(">"), None, None]])
    P2RTexture = Texture([[Pixel(">"), Pixel("-"), None]])
    P3RTexture = Texture([[Pixel(">"), Pixel("-"), Pixel("-")]])

    def __init__(self):
        super().__init__(player.position, self.P1Texture)
        self._is_hidden = True
        self.ticks = 0

    def on_input(self, key):
        if self._is_hidden and player.weapon == "sword" and key == " ":
            self.ticks = 0
            self.show()

    def on_update(self):
        if player.direction == "right":
            self.position = player.position + Vector(1, 0)
        else:
            self.position = player.position - Vector(3, 0)
        match self.ticks:
            case 2:
                self.texture = self.P2Texture if player.direction == "left" else self.P2RTexture
            case 4:
                self.texture = self.P3Texture if player.direction == "left" else self.P3RTexture
            case 6:
                self.texture = self.P2Texture if player.direction == "left" else self.P2RTexture
            case 8:
                self.texture = self.P1Texture if player.direction == "left" else self.P1RTexture
            case 10:
                self.hide()
        self.ticks += 1


class Boomerang(Entity):
    P1Texture = Texture([[Pixel("+")]])
    P2Texture = Texture([[Pixel("X")]])

    def __init__(self):
        super().__init__(player.position, "+")
        self.dir = "left"
        self._is_hidden = True
        self.ticks = 0
        self.is_at_start = True

    def on_input(self, key):
        if self._is_hidden and player.weapon == "boomerang" and key == " ":
            self.dir = player.direction
            if self.dir == "left":
                self.position = player.position - Vector(1, 0)
            else:
                self.position = player.position + Vector(1, 0)
            self.is_at_start = True
            self.show()
            self.ticks = 0

    def on_update(self):
        if self.ticks % 2 == 0:
            self.texture = self.P1Texture
        else:
            self.texture = self.P2Texture

        if self.ticks == 1:
            self.is_at_start = False
        elif self.ticks == 10:
            self.dir = "right" if self.dir == "left" else "left"
        elif self.ticks >= 20:
            self.hide()

        self.step(StepSides.RIGHT if self.dir == "right" else StepSides.LEFT)
        self.ticks += 1

    def on_collision(self, other):
        if isinstance(other, Player) and not self.is_at_start:
            self.hide()


class Enemy(Entity):
    to_destroy = False

    def __init__(self, position: Vector, lvl) -> None:
        match lvl:
            case 1:
                texture = Texture([[Pixel(f"{lvl}")]])
                self.healh = 5
            case 2:
                texture = Texture([[Pixel(f"{lvl}", (255, 51, 153))]])
                self.healh = 10
            case 3:
                texture = Texture([[Pixel(f"{lvl}", (255, 0, 0))]])
                self.healh = 20
        super().__init__(position, texture)

    def on_collision(self, other):
        if isinstance(other, (Sword, Boomerang)):
            if not other._is_hidden:
                self.healh -= player.damage

    def on_update(self):
        if self.healh <= 0:
            self.to_destroy = True
            player.score += 1
            return
        if random() >= 0.8:
            horizontal, vertical = find_directions_to_target(self, player)
            self.step(horizontal)
            self.step(vertical)


class Door(Entity):
    def __init__(self) -> None:
        super().__init__(Vector(-30, 5), Texture([[Pixel(" ")]]))

    def on_collision(self, other):
        if other is player:
            if other.score >= 10:
                other.score -= 10
                other.damage += 1
                Logger.print(f"Damage was incrased to {player.damage}")


class EnemiesManager(EmptyObject):
    def on_update():
        for enemy in list(enemies):
            if enemy.to_destroy:
                enemies.remove(enemy)
                enemy.destroy()
        if random() >= 0.98:
            if (r := random()) >= 0.9:
                lvl = 3
            elif r >= 0.6:
                lvl = 2
            else:
                lvl = 1
            enemies.append(
                Enemy(Vector(randint(-10, 10), randint(-10, 10)), lvl))


class Stats(EmptyObject):
    def on_update():
        engine.screen.display_string(30, 10, f"{player.score} pts")
        engine.screen.display_string(30, 9, f"{player.damage} dmg")


player = Player()
sword = Sword()
boomerang = Boomerang()
door = Door()
enemies: list[Enemy] = []

engine.load_world_map(world_map)
engine.start()
