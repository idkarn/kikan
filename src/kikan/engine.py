# import curses
import inspect

from .events import CreationEvent

from .events import InitEvent
from .math import Vertex
from .utils import LaunchError
from .screen import Screen
from time import sleep

loop = None  # TODO: replace global variable to other stuff


class Engine:
    def __init__(self) -> None:
        # self.scr = Screen()
        ...

    @classmethod
    def start(cls) -> None:
        global eng
        eng = cls()
        eng._launch()

    @InitEvent._trigger
    def _launch(self) -> LaunchError:
        try:
            print(loop.args)
            loop._loop()
        except Exception:
            raise LaunchError


class Loop:
    def __init__(self, func: callable) -> None:
        global loop
        self.args = {}
        func_params = inspect.signature(func).parameters
        for i in func_params.values():
            i: inspect.Parameter
            self.args[i.name] = True if i.default is i.empty else i.default
        self.user_loop = func  # main loop function placeholder
        loop = self

    def _loop(self):
        while True:
            if self.args["fps"] > 0:
                sleep(1 / self.args["fps"])
            self.user_loop()
