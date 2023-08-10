from dataclasses import dataclass
import sys
from typing import Callable

from .math import Vector
from .world import World
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
    def __init__(self, world: World) -> None:
        self.game_world = world
        self._init_hooks: list[Callable[[], None]] = []
        self._deinit_hooks: list[Callable[[], None]] = []

    def init(self) -> None:  # start engine init phase to create all necessary objects
        ...

    def start(self) -> None:
        get_key_delay = 1 / loop.config.fps
        self.scr = Screen(get_key_delay)
        self._launch()

    def _deinit(self):
        # TODO: dispatch DeInit event
        pass

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
                for entity in list(entities.values()):
                    if fn._self.pos == entity.pos and entity is not fn._self:
                        fn(fn._self)

    def _check_world_map_collision(self):
        for world_obj in self.game_world.map.config:
            for entity in entities.values():
                if world_obj.position == entity.pos:
                    entity.pos = entity.prev_pos

    def _draw_world(self):
        for world_obj in self.game_world.map.config:
            x, y = world_obj.position.x, world_obj.position.y
            self.scr.display_symbol(x, y, world_obj.texture)

    def _update_entities(self):
        for entity in list(entities.values()):
            entity._update()

    @InitEvent.trigger
    def _launch(self) -> LaunchError:
        def internal_loop(user_loop: callable):
            self._update_entities()
            self._check_input()  # check if any key is down
            self._check_collision()  # check for all collisions
            self._draw_world()
            self._check_world_map_collision()
            user_loop()  # run user's callback function
            self.scr.update()  # draw screen
        try:
            loop._loop(internal_loop)
        except Exception as ex:
            self.scr.terminate_terminal()
            self._deinit()
            raise LaunchError() from ex


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
