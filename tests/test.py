"""
Example code of using game engine

from kikan.engine import Loop
from kikan.events import InitEvent

@InitEvent
def init(once, name="test"): # event takes args from function params
  print("Successfully init")

entity = ...

@Loop
def loop(fps=30):
  entity.upd()
"""

from kikan.engine import Loop, Engine
from kikan.events import InitEvent

counter = 0


@InitEvent
def init():
    print("Successfully init")


def update():
    global counter
    counter += 1
    print("log", counter)


@Loop
def loop(fps=1):
    update()


Engine.start()
