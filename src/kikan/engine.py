from dataclasses import dataclass
import inspect

from .utils import LaunchError
from .screen import Screen
from time import sleep
from blessed import Terminal
from .events import InitEvent, EventBase, Input, CollisionEvent, _tracking_events
from .entity import Entity, entities

loop = None  # TODO: replace global variable to other stuff


@dataclass
class EngineConfig:
    fps: float


class Engine:
    def __init__(self) -> None:
        ...

    def init(self) -> None:  # start engine init phase to create all necessary objects
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
                if event._args["key"] == key:
                    listener[1]()

    def _check_collision(self):
        for listener in _tracking_events:
            listener: tuple[EventBase, callable]
            event, fn = listener
            if isinstance(event, CollisionEvent):
                for entity in entities:
                    entity: Entity
                    if fn._self.pos == entity.pos and entity is not fn._self:
                        fn(fn._self)

    @InitEvent.trigger
    def _launch(self) -> LaunchError:
        def internal_loop():
            self.scr.clear()  # clear screen
            self._check_input()  # check if any key is down
            self._check_collision()  # check for all collisions
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
