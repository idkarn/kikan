from __future__ import annotations
from types import FunctionType
from typing import Literal, TYPE_CHECKING, List, Any

from kikan.utils import Logger
if TYPE_CHECKING:
    from .entity import Entity
    from .engine import Engine


EventType = Literal["init", "pre_update",
                    "update", "trigger", "collision", "input"]
EventContext = List[Any]


class EventManager:
    def __init__(self, engine: Engine) -> None:
        self.tracking_events = []
        self.engine = engine  # link to engine instance

    def add_event_listener(cls, fn: FunctionType) -> None:
        cls.tracking_events.append(fn)

    def handle_input(self):
        if pressed_key := self.engine.screen.get_key():
            self.notify('input', [pressed_key])

    def tick(self):
        self.notify('pre_update')
        for entity in self.engine.game_world.entities.values():
            entity._update()
        self.notify('update')

        self.handle_input()

    def notify(self, event: EventType, ctx=None) -> None:
        """Dispatches current event for all entities"""
        if ctx is None:
            ctx = []
        for entity in self.engine.game_world.entities.values():
            self.dispatch(entity, event, ctx)
        for entity in self.engine.game_world.meta_entities.values():
            self.dispatch(entity, event, ctx)

    def dispatch(self, entity: Entity, event: EventType, ctx=None):
        """Calls entity's method for handling this event"""
        if ctx is None:
            ctx = []
        method_name = f"on_{event}"
        if hasattr(entity, method_name) and (method := getattr(entity, method_name)):
            method(*ctx)
