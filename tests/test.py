from kikan.engine import Engine, Loop
from kikan.events import InitEvent, Input, CreationEvent, CollisionEvent
from kikan.entity import Entity
from kikan.math import Vertex
from random import randint

eng = Engine()

player = None
gem = None
score = 0


class Player(Entity):
    @CreationEvent.trigger
    def __init__(self, *args) -> None:
        super().__init__(*args)

    @CollisionEvent
    def collide(self):
        global score, gem
        score += 1
        gem.respawn()


class Gem(Entity):
    def respawn(self):
        self.pos = Vertex(randint(-10, 10), randint(-10, 10))


def print_score():
    size = eng.scr.size
    coords = (-(size["width"] // 2 - 1), size["height"] // 2 - 1)
    eng.scr.display_symbol(*coords, f"Score: {score}", (0, 255, 0))


@CreationEvent
def player_create():
    print("player created!")


@InitEvent
def init():
    global player, gem
    player = Player(Vertex(0, 0), "@")
    gem = Gem(Vertex(2, 2), "*")
    print("[INIT] Success")


@Loop
def loop(fps=10):
    eng.scr.draw(gem)
    eng.scr.draw(player)
    print_score()


@Input
def inputD(key="d"):
    player.pos.x += 1


@Input
def inputA(key="a"):
    player.pos.x -= 1


@Input
def inputW(key="w"):
    player.pos.y += 1


@Input
def inputS(key="s"):
    player.pos.y -= 1


eng.start()
