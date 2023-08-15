from dataclasses import dataclass
from types import FunctionType
from typing import Any, Optional, TypeVar, Generic

# from kikan.utils import Logger

# TODO: move all this content into __init__.py


class ListenerDefiningError(Exception):
    ...


class ListenerInfo:
    class_: Optional[type]
    function: FunctionType
    arguments: Optional[dict[str, Any]]
    instance: Optional[object]

    def __init__(self, *args, **kwargs) -> None:
        if len(args) == 1 and isinstance(args[0], FunctionType):
            self.function = args[0]
        elif len(args) > 1:
            raise ListenerDefiningError
        else:
            self.arguments = kwargs

    def __repr__(self) -> str:
        repr_str = "Info: "
        if hasattr(self, "class_"):
            repr_str += f" {self.class_}"
        if hasattr(self, "function"):
            repr_str += f" {self.function}"
        if hasattr(self, "arguments"):
            repr_str += f" {self.arguments}"
        if hasattr(self, "instance"):
            repr_str += f" {self.instance}"
        return repr_str


class ListenerBase:
    """It must be set by python to get class if wrapped function is method
    """

    info: ListenerInfo

    def __set_name__(self, owner, name) -> None:
        orig_init = getattr(owner, "__init__")

        def init_wrapper(wrapped_self, *args, **kwargs):
            print(self, wrapped_self)
            self.info.instance = wrapped_self
            EventManager.add_event_listener(self)
            orig_init(wrapped_self, *args, **kwargs)

        self.info.class_ = owner
        setattr(owner, name, self.info.function)
        setattr(owner, "__init__", init_wrapper)

    def __init__(self, func: FunctionType) -> None:
        self.info = ListenerInfo(func)
        EventManager.add_event_listener(self)

    def __call__(self) -> None:
        self.info.function()

    def check(self, eng) -> None:
        ...


class TriggerBase:
    def __new__(cls, fn: FunctionType) -> FunctionType:
        def wrapper(*args, **kwargs):
            def check_events(event: EventType):
                if isinstance(event, DependentEvent) and event.depends_on is cls:
                    return True
            handled_funcs = filter(check_events, EventManager.tracking_events)
            for listener in handled_funcs:
                listener()
            fn(*args, **kwargs)
        return wrapper


EventType = TypeVar('EventType', ListenerBase, TriggerBase)


class Configurable(Generic[EventType]):
    """Unstable feature"""

    def __init__(self, *args, **kwargs) -> None:
        if len(args) > 0:
            raise ListenerDefiningError
        self.info = ListenerInfo(**kwargs)

    def __call__(self, fn: FunctionType) -> Any:
        if not hasattr(self.info, "function"):
            self.info.function = fn
            EventManager.add_event_listener(self)

        class Wrapper:
            def __set_name__(_, owner: type, name: str) -> None:
                self.info.class_ = owner
                setattr(owner, name, self.info.function)

            def __call__(_) -> None:
                fn()

        return Wrapper()


class DependentEvent(ListenerBase):
    depends_on: TriggerBase


class EventManager:
    tracking_events: list[EventType] = []

    @classmethod
    def add_event_listener(cls, new_event_listener: EventType) -> None:
        cls.tracking_events.append(new_event_listener)

    def tick(self, engine_instance: "Engine") -> None:
        for event in self.tracking_events:
            event.check(engine_instance)


class InitEvent(TriggerBase):
    ...


class OnInit(DependentEvent):
    depends_on = InitEvent


class Input(Configurable[ListenerBase]):
    ...


EventManager()


class A:
    @InitEvent
    def init(self):
        print("init")


class B:
    @OnInit
    def preinit(self):
        print("preinit")


for event in EventManager.tracking_events:
    print(event.info)
