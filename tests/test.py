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
def init():  # start point of the game
    global player, gem
    player = Player(Vertex(0, 0), "@")
    gem = Gem(Vertex(2, 2), "*")
    print("[INIT] Success")


@Loop(fps=5)
def loop():  # main game loop
    eng.scr.draw(gem)
    eng.scr.draw(player)
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


eng.start()
