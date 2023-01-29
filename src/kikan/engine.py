from dataclasses import dataclass
import inspect
from .events import InitEvent
from .utils import LaunchError
from time import sleep

loop = None  # TODO: replace global variable to other stuff


@dataclass
class EngineConfig:
    fps: float


class Engine:
    def __init__(self) -> None:
        # self.scr = Screen()
        ...

    @classmethod
    def start(cls) -> None:
        global eng
        eng = cls()
        eng._launch()

    @InitEvent.trigger
    def _launch(self) -> LaunchError:
        try:
            print(loop.config)
            loop._loop()
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

    def _loop(self):
        while True:
            if self.config.fps > 0:
                sleep(1 / self.config.fps)
            self.user_loop()
