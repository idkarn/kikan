from dataclasses import dataclass
import inspect

from .errors import LaunchError
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
    def __init__(self, world) -> None:
        ...

    def init(self) -> None:  # start engine init phase to create all necessary objects
        ...

    def start(self) -> None:
        get_key_delay = 1 / loop.config.fps
        self.scr = Screen(get_key_delay)
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
        def internal_loop(user_loop: callable):
            self._check_input()  # check if any key is down
            self._check_collision()  # check for all collisions
            user_loop()  # run user's callback function
            self.scr.update()  # draw screen
        try:
            loop._loop(internal_loop)
        except Exception:
            self.scr.terminate_terminal()
            raise LaunchError


class Loop:
    def __init__(self, **kwargs: any) -> None:
        global loop
        self.config = EngineConfig(**kwargs)
        loop = self

    def __call__(self, fn: callable) -> any:
        self.user_loop = fn

    def _loop(self, internal_loop: callable) -> None:
        while True:
            if self.config.fps > 0:
                sleep(1 / self.config.fps)
            internal_loop(self.user_loop)
