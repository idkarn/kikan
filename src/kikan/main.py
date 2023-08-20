import typing as _typing
import kikan.world as _world

from .engine import Engine

if _typing.TYPE_CHECKING:
    ...

engine = Engine()
engine.game_world = _world.World(_world.WorldMap([]))
