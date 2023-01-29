from dataclasses import dataclass
import inspect


_events_index = {}
_tracking_events: list[tuple[object, callable]] = []


@dataclass
class EventType:
    name: str
    description: str
    code: int

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
        self.code = len(_events_index)
        _events_index[self.code] = self

    @staticmethod
    def get_event_by_code(code: int):
        return _events_index[code]


class EventBase:
    TYPE = EventType(
        "Primitive",
        "Internal using only"
    )

    def __init__(self, fn: callable) -> None:
        self.args = {}
        func_params = inspect.signature(fn).parameters
        for i in func_params.values():
            i: inspect.Parameter
            self.args[i.name] = True if i.default is i.empty else i.default
        self._handle(fn)

    def _handle(self, fn: callable) -> None:
        _tracking_events.append((self, fn))

    @classmethod
    def trigger(cls, fn: callable) -> callable:
        def trigger_wrapper(*args, **kwargs):
            # trigger event here
            def check_events(event: tuple[EventBase, callable]):
                if event[0].TYPE is cls.TYPE:
                    return True
            handled_funcs = filter(check_events, _tracking_events)
            for handled_event, handled_func in handled_funcs:
                handled_func()
            # then call wrapped function
            fn(*args, **kwargs)

        return trigger_wrapper


class InitEvent(EventBase):
    TYPE = EventType(
        "InitEvent",
        "Event triggered on initialization phase"
    )


class CreationEvent(EventBase):
    TYPE = EventType(
        "CreationEvent",
        "Event triggered when the entity is created"
    )
