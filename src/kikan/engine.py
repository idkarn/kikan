from dataclasses import dataclass
from time import sleep
from typing import Callable

from .math import Vector
from .utils import Logger
from .errors import LaunchError
from .events import EventManager
from .screen import Screen
from .world import World, WorldMap


@dataclass
class EngineConfig:
    fps: float = 10


class Engine:
    # noinspection PyTypeChecker
    def __init__(self):  # start engine init phase to create all necessary objects
        self.screen: Screen = None
        self.game_world: World = World(WorldMap([]))
        self._init_hooks: list[Callable[[], None]] = []
        self._terminate_hooks: list[Callable[[], None]] = []
        self.event_manager = EventManager(self)
        self.config = EngineConfig()
        self.__is_running = True
        Logger.init()

    #! deprecated
    def init(self):
        ...

    def setup(self, config: EngineConfig):
        self.config = config

    def start(self):
        get_key_delay = 1 / self.config.fps
        self.screen = Screen(get_key_delay)
        self._launch_loop_handler()

    def stop(self):
        self.__is_running = False

    def load_world_map(self, world_map: WorldMap):
        self.game_world.map = world_map

    def _terminate(self):
        # TODO: dispatch Terminate event
        Logger.terminate()

    def _check_collision(self):
        entities = list(self.game_world.entities.values())
        for i in range(len(entities)):
            for j in range(i+1, len(entities)):
                entity1 = entities[i]
                entity2 = entities[j]
                if (entity1.position - entity2.position).length() <= 1:
                    self.event_manager.dispatch(
                        entity1, 'collision', [entity2])
                    self.event_manager.dispatch(
                        entity2, 'collision', [entity1])

    def _remove_destroyed_entities(self):
        for key, value in reversed(self.game_world.entities.items()):
            if value._is_destroyed:
                del self.game_world.entities[key]
        for key, value in reversed(self.game_world.meta_entities.items()):
            if value._is_destroyed:
                del self.game_world.meta_entities[key]

    def _draw_entities(self):
        for entity in self.game_world.entities.values():
            if not entity._is_hidden:
                self.screen.draw(entity)

    def __do_tick(self) -> None:
        self.event_manager.tick()
        self._check_collision()

        for world_object in self.game_world.map.config:
            # handling world map collision
            for entity in self.game_world.entities.values():
                if (world_object.position - entity.position).length() <= 0.5:
                    entity.position = entity.prev_pos
                    entity.velocity = Vector(0, 0)

            # drawing world objects
            x, y = world_object.position.x, world_object.position.y
            self.screen.display_symbol(x, y, world_object.texture)

        self._remove_destroyed_entities()
        self._draw_entities()
        self.screen.update()

    def _launch_loop_handler(self) -> None:
        while self.__is_running:
            try:
                self.__do_tick()
                sleep(1 / self.config.fps)
            except Exception as e:
                Logger.print(repr(e))
                self.screen.terminate_terminal()
                self._terminate()
                raise LaunchError() from e
        self._terminate()
