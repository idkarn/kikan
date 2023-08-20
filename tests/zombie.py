from random import randint

from kikan import World, Entity, Loop, InitEvent, Input, WorldMap, WorldObject, CollisionEvent, engine
from kikan.entity import StepSides
from kikan.math import Vector

world = World(WorldMap([
    WorldObject(Vector(2, 2), "#"),
    WorldObject(Vector(2, 3), "#"),
    WorldObject(Vector(3, 2), "#"),
    WorldObject(Vector(-2, 2), "#"),
    WorldObject(Vector(-2, 3), "#"),
    WorldObject(Vector(-3, 2), "#"),
]), {})

engine.init(world)


class Player(Entity):
    def __init__(self, pos: Vector, texture: str, direction: StepSides):
        super().__init__(pos, texture)
        self.direction = direction
        self.score = 0

    @CollisionEvent
    def collide(self):
        self.score = -1


class Zombie(Entity):
    def respawn(self):
        self.position = Vector(randint(-10, 10), randint(-10, 10))

    @CollisionEvent
    def collide(self):
        bullet.destroy()
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


# noinspection PyTypeChecker
player: Player = None
# noinspection PyTypeChecker
zombie: Zombie = None
# noinspection PyTypeChecker
bullet: Bullet = None


def print_score():
    size = engine.screen.size
    coords = (-(size["width"] // 2 - 1), size["height"] // 2 - 1)
    engine.screen.display_string(*coords, f"Score: {player.score}", (0, 255, 0))


@InitEvent
def init():
    global player, zombie, bullet
    # player = Player(Vector(0, 0), "@>", StepSides.RIGHT)
    # BUG: screen moves if a texture contains more than one symbol
    player = Player(Vector(0, 0), "@", StepSides.RIGHT)
    zombie = Zombie(Vector(-10, 10), "Z")


@Loop(fps=5)
def loop():
    if randint(0, 2) == 2:
        zombie.move()
    engine.screen.draw(player)
    engine.screen.draw(zombie)
    if bullet:
        bullet.move()
        engine.screen.draw(bullet)
    print_score()


@Input(key=" ")
def shoot():
    global bullet
    dx = 2 if player.direction == StepSides.RIGHT else -2
    bullet = Bullet(Vector(player.position.x + dx, player.position.y), "-", player.direction)


@Input(key="right")
def right():
    player.texture = "@>"
    player.direction = StepSides.RIGHT
    player.step(StepSides.RIGHT)


@Input(key="left")
def left():
    player.texture = "<@"
    player.direction = StepSides.LEFT
    player.step(StepSides.LEFT)


@Input(key="down")
def down():
    player.step(StepSides.DOWN)


@Input(key="up")
def up():
    player.step(StepSides.UP)


@Input(key="q")
def quit_():
    exit()


engine.start()
