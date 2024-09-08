from __future__ import annotations

from typing import Any, Callable

AnyCallable = Callable[..., Any]


class Signal:
    def __init__(self) -> None:
        self.__subs: dict[str, AnyCallable] = {}

    def __call__(self, function: AnyCallable) -> AnyCallable:
        setattr(function, "_subscribed_on", self)
        self.subscribe(function)
        return function

    def subscribe(self, function: AnyCallable) -> None:
        self.__subs[function.__name__] = function

    def emit(self) -> None:
        for fn in self.__subs.values():
            fn()
