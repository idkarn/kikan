from dataclasses import dataclass
from typing import Callable


from .events_new import EventManager

from .world import World
from .errors import LaunchError
from .screen import Screen
from time import sleep
from .events import InitEvent, EventBase, Input, CollisionEvent, _tracking_events
from .utils import Logger


@dataclass
class EngineConfig:
    fps: float = 10


class Engine:
    def __init__(self, world: World) -> None:
        self.game_world = world
        self._init_hooks: list[Callable[[], None]] = []
        self._deinit_hooks: list[Callable[[], None]] = []
        self.event_manager = EventManager(self)
        self.config = EngineConfig()
        Logger.init()

    def init(self) -> None:  # start engine init phase to create all necessary objects
        ...

    def setup(self, config: EngineConfig) -> None:
        self.config = config

    def start(self) -> None:
        get_key_delay = 1 / self.config.fps
        self.scr = Screen(get_key_delay)
        self._launch_loop_handler()

    def load_world(self, world: World) -> None:
        self.game_world = world

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
                for entity in self.game_world.entities:
                    if (fn._self.pos - entity.pos).length() <= 1 and entity is not fn._self:
                        fn(fn._self)

    def _check_world_map_collision(self):
        for world_obj in self.game_world.map.config:
            for entity in self.game_world.entities:
                if world_obj.position == entity.pos:
                    entity.pos = entity.prev_pos

    def _draw_world(self):
        for world_obj in self.game_world.map.config:
            x, y = world_obj.position.x, world_obj.position.y
            self.scr.display_symbol(x, y, world_obj.texture)

    def _draw_entities(self):
        for entity in self.game_world.entities:
            self.scr.draw(entity)

    def _update_entities(self):
        self.event_manager.notify('pre_update')
        for entity in self.game_world.entities:
            entity._update()
        self.event_manager.notify('update')

    def _update_screen(self):
        self.scr.update()

    def __do_tick(self) -> None:
        self._update_entities()
        self._check_input()
        self._check_collision()
        self._draw_world()
        self._draw_entities()
        self._check_world_map_collision()
        self._update_screen()

    def _launch_loop_handler(self) -> LaunchError:
        try:
            self.__do_tick()
            sleep(1 / self.config.fps)
            self._launch_loop_handler()
        except Exception as ex:
            self.scr.terminate_terminal()
            self._deinit()
            raise LaunchError() from ex
