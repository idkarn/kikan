from __future__ import annotations

from typing import Any, Callable, ClassVar

AnyCallable = Callable[..., Any]


class StateManager:
    __tracking_states: ClassVar[dict[State, dict[str, AnyCallable]]] = {}

    @classmethod
    def subscribe(cls, state: State, function: AnyCallable) -> None:
        if state in cls.__tracking_states:
            cls.__tracking_states[state][function.__name__] = function
        else:
            cls.__tracking_states[state] = {function.__name__: function}

    @classmethod
    def trigger(cls, state: State) -> None:
        for fn in cls.__tracking_states[state].values():
            fn()

    @classmethod
    def get_states(cls) -> dict[State, dict[str, AnyCallable]]:
        return cls.__tracking_states


class State:
    def __init__(self, initial_value: Any) -> None:
        self.__value = initial_value

    def set(self, new_value: Any) -> None:
        self.__value = new_value
        StateManager.trigger(self)

    def get(self) -> Any:
        return self.__value

    def affects(self, function: AnyCallable) -> AnyCallable:
        setattr(function, "_affected_by", self)
        StateManager.subscribe(self, function)
        return function

    def __hash__(self) -> int:
        return id(self)
