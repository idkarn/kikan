from dataclasses import dataclass
import inspect

from .events import InitEvent
from .utils import LaunchError
from .screen import Screen
from time import sleep
from blessed import Terminal
from .events import _tracking_events, EventBase, Input

loop = None  # TODO: replace global variable to other stuff
entities = []

@dataclass
class EngineConfig:
    fps: float

class Engine:
    def __init__(self) -> None:
        ...

    def start(self) -> None:
        term = Terminal()
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            get_key_delay = 1 / loop.config.fps
            self.scr = Screen(term, get_key_delay)
            self._launch()

    def _check_input(self):
        key = self.scr.get_key()
        for listener in _tracking_events:
            listener: tuple[EventBase, callable]
            event = listener[0]
            if isinstance(event, Input):
                if event.args["key"] == key:
                    listener[1]()

    @InitEvent.trigger
    def _launch(self) -> LaunchError:
        def internal_loop():
            self.scr.clear() # clear screen
            self._check_input() # check if any key is down
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
