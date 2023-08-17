from dataclasses import dataclass
from typing import Callable


from .events import EventManager
from .world import World
from .errors import LaunchError
from .screen import Screen
from time import sleep
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

    def _check_collision(self):
        for i in range(len(self.game_world.entities)):
            for j in range(i+1, len(self.game_world.entities)):
                entity1 = self.game_world.entities[i]
                entity2 = self.game_world.entities[j]
                if (entity1.pos - entity2.pos).length() <= 1:
                    self.event_manager.dispatch(
                        entity1, 'collision', [entity2])
                    self.event_manager.dispatch(
                        entity2, 'collision', [entity1])

    def _draw_entities(self):
        for entity in self.game_world.entities:
            self.scr.draw(entity)

    def __do_tick(self) -> None:
        self.event_manager.tick()
        self._check_collision()

        for world_object in self.game_world.map.config:
            # handling world map collision
            for entity in self.game_world.entities:
                if world_object.position == entity.pos:
                    entity.pos = entity.prev_pos

            # drawing world objects
            x, y = world_object.position.x, world_object.position.y
            self.scr.display_symbol(x, y, world_object.texture)

        self._draw_entities()
        self.scr.update()

    def _launch_loop_handler(self) -> LaunchError:
        try:
            self.__do_tick()
            sleep(1 / self.config.fps)
            self._launch_loop_handler()
        except Exception as ex:
            self.scr.terminate_terminal()
            self._deinit()
            raise LaunchError() from ex
