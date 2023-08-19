from dataclasses import dataclass
from time import sleep
from typing import Callable

from .entity import entities
from .math import Vector
from .utils import Logger
from .errors import LaunchError
from .events import InitEvent, EventBase, Input, CollisionEvent, _tracking_events
from .screen import Screen
from .world import World


@dataclass
class EngineConfig:
    fps: float


class Engine:
    # noinspection PyTypeChecker
    def __init__(self):  # start engine init phase to create all necessary objects
        self.screen: Screen = None
        self.game_world: World = None
        self.loop: Loop = None
        self._init_hooks: list[Callable[[], None]] = []
        self._terminate_hooks: list[Callable[[], None]] = []

    def init(self, world: World) -> None:
        self.game_world = world

    def start(self) -> None:
        get_key_delay = 1 / self.loop.config.fps
        self.screen = Screen(get_key_delay)
        self._launch()

    def _terminate(self):
        # TODO: dispatch Terminate event
        Logger.terminate()

    def _check_input(self):
        key = self.screen.get_key()
        for listener in _tracking_events:
            listener: tuple[EventBase, callable]
            event = listener[0]
            if isinstance(event, Input):
                if event.args["key"] == key:
                    listener[1]()

    def _check_collision(self):
        for listener in _tracking_events:
            listener: tuple[EventBase, callable]
            event, fn = listener
            if isinstance(event, CollisionEvent):
                for entity in list(entities.values()):
                    if (fn._self.position - entity.position).length() <= 1 and entity is not fn._self:
                        fn(fn._self)

    def _check_world_map_collision(self):
        for world_obj in self.game_world.map.config:
            for entity in entities.values():
                if (world_obj.position - entity.position).length() <= 1:
                    entity.position = entity.prev_pos
                    entity.velocity = Vector(0, 0)

    def _draw_world(self):
        for world_obj in self.game_world.map.config:
            x, y = world_obj.position.x, world_obj.position.y
            self.screen.display_symbol(x, y, world_obj.texture)

    def _update_entities(self):
        for entity in list(entities.values()):
            # noinspection PyProtectedMember
            entity._update()

    @InitEvent.trigger
    def _launch(self):
        def internal_tick(user_tick: callable):
            self._update_entities()
            self._check_input()  # check if any key is down
            self._check_collision()  # check for all collisions
            self._draw_world()
            self._check_world_map_collision()
            user_tick()  # run user's callback function
            self.screen.update()  # draw screen
        try:
            self.loop.run(internal_tick)
        except Exception as e:
            Logger.print(repr(e))
            self.screen.terminate_terminal()
            self._terminate()
            raise LaunchError() from e


class Loop:
    def __init__(self, **kwargs: any) -> None:
        self.config = EngineConfig(**kwargs)
        engine.loop = self

    def __call__(self, func: callable) -> any:
        self.user_tick = func

    def run(self, internal_tick: callable) -> None:
        while True:
            if self.config.fps > 0:
                sleep(1 / self.config.fps)
            internal_tick(self.user_tick)


engine = Engine()
