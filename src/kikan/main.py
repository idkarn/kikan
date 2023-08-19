import typing as _typing
import kikan.world as _world

from .engine import Engine

if _typing.TYPE_CHECKING:
    ...

_default_world = _world.World(_world.WorldMap([]))
engine = Engine(_default_world)
