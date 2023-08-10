from kikan import Engine, Loop, InitEvent, Input, CollisionEvent, Entity, Vector, World, WorldMap, WorldObject
from random import randint


world_map = WorldMap([
    WorldObject(Vector(2, 2), "#"),
    WorldObject(Vector(2, 3), "#"),
    WorldObject(Vector(3, 3), "#")
])
world = World(world_map, [])


eng = Engine(world)

player = None
gem = None
enemy = None
score = 0


class Enemy(Entity):
    def update(self):
        if randint(0, 100) == 100:
            if self.pos.x > player.pos.x:
                self.step("left")
            if self.pos.x < player.pos.x:
                self.step("right")
            if self.pos.y > player.pos.y:
                self.step("down")
            if self.pos.y < player.pos.y:
                self.step("up")


class Player(Entity):
    def __init__(self, *args) -> None:
        super().__init__(*args)

    @CollisionEvent
    def collide(self):
        global score, gem
        score += 1
        gem.respawn()


class Gem(Entity):
    def respawn(self):
        self.pos = Vector(randint(-10, 10), randint(-10, 10))


def print_score():
    size = eng.scr.size
    coords = (-(size["width"] // 2 - 1), size["height"] // 2 - 1)
    eng.scr.display_string(*coords, f"Score: {score}", (0, 255, 0))


@InitEvent
def init():  # start point of the game
    global player, gem, enemy
    player = Player(Vector(0, 0), "@")
    gem = Gem(Vector(10, 10), "*")
    enemy = Enemy(Vector(-2, 0), "E")
    print("[INIT] Success")


@Loop(fps=10)
def loop():  # main game loop
    eng.scr.draw(gem)
    eng.scr.draw(player)
    eng.scr.draw(enemy)
    print_score()

# *** keyboard inputs ***


@Input(key="d")
def inputD():
    player.pos.x += 1


@Input(key="a")
def inputA():
    player.pos.x -= 1


@Input(key="w")
def inputW():
    player.pos.y += 1


@Input(key="s")
def inputS():
    player.pos.y -= 1


@Input(key="q")
def quit():
    exit()


eng.start()


"""

from kikan.engine import Engine, Loop
from kikan.events import InitEvent, Input, CollisionEvent
from kikan.entity import Entity
from kikan.math import Vertex
from random import randint

eng = Engine()

player = None
zomb = None
score = 0
bullet = None


class Player(Entity):
    def __init__(self, pos, texture, dir):
        super().__init__(pos, texture)
        self.dir = dir

    @CollisionEvent
    def collide(self):
        global score
        score = -1


class Zombie(Entity):
    def respawn(self):
        self.pos = Vertex(randint(-10, 10), randint(-10, 10))

    @CollisionEvent
    def collide(self):
        global score, bullet
        score += 1
        self.respawn()
        bullet = None

    def move(self):
        dx = 1 if player.pos.x > self.pos.x else -1 if player.pos.x != self.pos.x else 0
        dy = 1 if player.pos.y > self.pos.y else -1 if player.pos.y != self.pos.y else 0
        self.pos.x += dx
        self.pos.y += dy

class Bullet(Entity):
    def __init__(self, pos, texture, dir):
        super().__init__(pos, texture)
        self.dir = dir

    def move(self):
        dx = 1 if self.dir == "right" else -1
        self.pos = Vertex(self.pos.x + dx, self.pos.y)


def print_score():
    size = eng.scr.size
    coords = (-(size["width"] // 2 - 1), size["height"] // 2 - 1)
    eng.scr.display_symbol(*coords, f"Score: {score}", (0, 255, 0))


@InitEvent
def init():  # start point of the game
    global player, zomb
    player = Player(Vertex(0, 0), "@>", "right")
    zomb = Zombie(Vertex(2, 2), "Z")
    print("[INIT] Success")


@Loop
def loop(fps=5):  # main game loop
    if bullet:
        eng.scr.draw(bullet)
        bullet.move()
    if randint(0,2) == 2:
        zomb.move()
    eng.scr.draw(zomb)
    eng.scr.draw(player)
    print_score()

# *** keyboard input ***

@Input
def shoot(key=" "):
    global bullet
    dx = 2 if player.dir == "right" else -2
    bullet = Bullet(Vertex(player.pos.x + dx, player.pos.y), "-", player.dir)

@Input
def right(key="d"):
    player.texture = "@>"
    player.dir = "right"
    player.pos.x += 1


@Input
def left(key="a"):
    player.texture = "<@"
    player.dir = "left"
    player.pos.x -= 1


@Input
def up(key="w"):
    player.pos.y += 1


@Input
def down(key="s"):
    player.pos.y -= 1


eng.start()

"""
