from dataclasses import dataclass
import inspect
from .events import InitEvent
from .utils import LaunchError
from .screen import Screen
from time import sleep
from blessed import Terminal

loop = None  # TODO: replace global variable to other stuff


@dataclass
class EngineConfig:
    fps: float


class Engine:
    def __init__(self) -> None:
        ...

    def start(self) -> None:
        term = Terminal()
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            self.scr = Screen(term)
            self._launch()

    @InitEvent.trigger
    def _launch(self) -> LaunchError:
        def internal_loop():
            self.scr.clear()
        try:
            loop._loop(internal_loop)
        except Exception:
            raise LaunchError


class Loop:
    def __init__(self, func: callable) -> None:
        global loop
        args = {}
        func_params = inspect.signature(func).parameters
        for i in func_params.values():
            i: inspect.Parameter
            args[i.name] = True if i.default is i.empty else i.default
        self.user_loop = func  # main loop function placeholder
        self.config = EngineConfig(**args)
        loop = self

    def _loop(self, internal_loop: callable) -> None:
        while True:
            if self.config.fps > 0:
                sleep(1 / self.config.fps)
            internal_loop()
            self.user_loop()
