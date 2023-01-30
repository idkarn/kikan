from .events import EventBase, EventType

class Input(EventBase):
    TYPE = EventType(
        "InputEvent",
        "Event triggered when the key is pressed"
    )