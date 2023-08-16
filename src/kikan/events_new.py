from __future__ import annotations
from types import FunctionType
from typing import Literal, TYPE_CHECKING
if TYPE_CHECKING:
    from .entity import Entity
    from .engine import Engine


EventType = Literal["init", "pre_update", "update", "trigger", "collision"]


class EventManager:
    def __init__(self, engine: Engine) -> None:
        self.tracking_events = []
        self.engine = engine  # link to engine instance

    def add_event_listener(cls, fn: FunctionType) -> None:
        cls.tracking_events.append(fn)

    def tick(self):
        ...

    def notify(self, event: EventType) -> None:
        """Dispatches current event for all entities"""
        for entity in self.engine.game_world.entities + self.engine.game_world.meta_entities:
            self.dispatch(entity, event)

    def dispatch(self, entity: Entity, event: EventType):
        """Calls entity's method for handling this event"""
        method_name = f"on_{event}"
        if hasattr(entity, method_name) and (method := getattr(entity, method_name)):
            method()
