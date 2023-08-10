from random import randint
from kikan import Engine, World, Entity, Loop, InitEvent, Input, WorldMap, WorldObject, Vector, CollisionEvent
from kikan.math import Vector

world = World(WorldMap([
    WorldObject(Vector(2, 2), "#"),
    WorldObject(Vector(2, 3), "#"),
    WorldObject(Vector(3, 2), "#"),
    WorldObject(Vector(-2, 2), "#"),
    WorldObject(Vector(-2, 3), "#"),
    WorldObject(Vector(-3, 2), "#"),
]), [])
e = Engine(world)

score: int = 0


class Player(Entity):
    def __init__(self, pos: Vector, texture: str, dir: str):
        super().__init__(pos, texture)
        self.dir = dir

    @CollisionEvent
    def collide(self):
        global score
        score = -1


class Zombie(Entity):
    def respawn(self):
        self.pos = Vector(randint(-10, 10), randint(-10, 10))

    @CollisionEvent
    def collide(self):
        global score
        bullet.destroy()
        self.respawn()
        score += 1

    def move(self):
        if player.pos.x > self.pos.x:
            self.step("right")
        elif player.pos.x < self.pos.x:
            self.step("left")
        if player.pos.y > self.pos.y:
            self.step("up")
        elif player.pos.y < self.pos.y:
            self.step("down")


class Bullet(Entity):
    def __init__(self, position: Vector, texture: str, dir: str) -> None:
        super().__init__(position, texture)
        self.dir = dir

    def move(self):
        self.step(self.dir)


player: Player = None
zombie: Zombie = None
bullet: Bullet = None


def print_score():
    size = e.scr.size
    coords = (-(size["width"] // 2 - 1), size["height"] // 2 - 1)
    e.scr.display_string(*coords, f"Score: {score}", (0, 255, 0))


@InitEvent
def init():
    global player, zombie, bullet
    player = Player(Vector(0, 0), "@>", "right")
    zombie = Zombie(Vector(-10, 10), "Z")


@Loop(fps=5)
def loop():
    if randint(0, 2) == 2:
        zombie.move()
    e.scr.draw(player)
    e.scr.draw(zombie)
    if bullet:
        bullet.move()
        e.scr.draw(bullet)
    print_score()


@Input(key=" ")
def shoot():
    global bullet
    dx = 2 if player.dir == "right" else -2
    bullet = Bullet(Vector(player.pos.x + dx, player.pos.y), "-", player.dir)


@Input(key="right")
def right():
    player.texture = "@>"
    player.dir = "right"
    player.step("right")


@Input(key="left")
def left():
    player.texture = "<@"
    player.dir = "left"
    player.step("left")


@Input(key="down")
def down():
    player.step("down")


@Input(key="up")
def up():
    player.step("up")


@Input(key="q")
def quit():
    exit()


e.start()
