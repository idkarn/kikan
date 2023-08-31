from random import randint

from kikan import Entity, engine
from kikan.entity import EmptyObject, Pixel, StepSides, Texture
from kikan.math import Vector
from kikan.world import WorldMap, WorldObject

world_map = WorldMap([
    WorldObject(Vector(2, 2), "#"),
    WorldObject(Vector(2, 3), "#"),
    WorldObject(Vector(3, 2), "#"),
    WorldObject(Vector(-2, 2), "#"),
    WorldObject(Vector(-2, 3), "#"),
    WorldObject(Vector(-3, 2), "#"),
])


class Player(Entity):
    def __init__(self, pos: Vector, texture: str, direction: StepSides):
        super().__init__(pos, texture)
        self.direction = direction
        self.score = 0

    def on_collision(self, other):
        self.score = -1

    def on_input(self, key):
        match key:
            case "right":
                self.texture = Texture([[Pixel("@"), Pixel(">")]])
                self.direction = StepSides.RIGHT
            case "left":
                self.texture = Texture([[Pixel("<"), Pixel("@")]])
                self.direction = StepSides.LEFT
            case "up":
                self.direction = StepSides.UP
            case "down":
                self.direction = StepSides.DOWN
            case "q":
                exit()
            case _:
                return
        self.step(self.direction)


class Zombie(Entity):
    def respawn(self):
        self.position = Vector(randint(-10, 10), randint(-10, 10))

    def on_collision(self, other):
        self.respawn()
        player.score += 1

    def move(self):
        if player.position.x > self.position.x:
            self.step(StepSides.RIGHT)
        elif player.position.x < self.position.x:
            self.step(StepSides.LEFT)
        if player.position.y > self.position.y:
            self.step(StepSides.UP)
        elif player.position.y < self.position.y:
            self.step(StepSides.DOWN)


class Bullet(Entity):
    def __init__(self, position: Vector, texture: str, direction: StepSides) -> None:
        super().__init__(position, texture)
        self.direction = direction

    def move(self):
        self.step(self.direction)

    def on_collision(self, other):
        self.destroy()


player = Player(Vector(0, 0), Texture(
    [[Pixel("@"), Pixel(">")]]), StepSides.RIGHT)
zombie = Zombie(Vector(-10, 10), "Z")
# noinspection PyTypeChecker
bullet: Bullet = None


class Score(EmptyObject):
    def on_update():
        if randint(0, 2) == 2:
            zombie.move()
        if bullet:
            bullet.move()
        print_score()

    def on_input(key):
        if key != " ":
            return
        global bullet
        dx = 2 if player.direction == StepSides.RIGHT else -2
        if bullet:
            bullet.destroy()
        bullet = Bullet(Vector(player.position.x + dx,
                               player.position.y), "-", player.direction)


def print_score():
    size = engine.screen.size
    coords = (-(size["width"] // 2 - 1), size["height"] // 2 - 1)
    engine.screen.display_string(
        *coords, f"Score: {player.score}", (0, 255, 0))


engine.load_world_map(world_map)
engine.start()
