from kikan.engine import Engine, Loop
from kikan.events import InitEvent, Input
from kikan.entity import Entity
from kikan.math import Vertex

eng = Engine()
player = None


class Player(Entity):
    ...


@InitEvent
def init():
    global player
    player = Player(Vertex(0, 0), "@")
    print("[INIT] Success")


@Loop
def loop(fps=10):
    eng.scr.draw(player)


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
