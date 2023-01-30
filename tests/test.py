from kikan.engine import Engine, Loop
from kikan.events import InitEvent, Input
from kikan.entity import Entity

eng = Engine()


class Player(Entity):
    ...


@InitEvent
def init():
    player = Player()
    print("[INIT] Success")


i = -10


@Loop
def loop(fps=1):

    eng.scr.display_symbol(i, i, eng.scr.get_key() or "0")


@Input
def input(key="a"):
    print("handled")


eng.start()
