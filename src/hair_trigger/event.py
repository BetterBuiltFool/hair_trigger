from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from functools import singledispatchmethod
from types import MethodType
from typing import Any
from weakref import WeakKeyDictionary

from hair_trigger import scheduler, threader


class _Sentinel:
    pass


SENTINEL = _Sentinel()


class Event(ABC):
    """
    Base class for per-instance events.
    Subclasses must define the `trigger` method, which defines the event signature.
    """

    def __init__(self) -> None:
        self.listeners: WeakKeyDictionary[Any, list[Callable]] = WeakKeyDictionary()
        self.method_listeners: WeakKeyDictionary[Any, list[Callable]] = (
            WeakKeyDictionary()
        )

    @singledispatchmethod
    def __call__(self, _) -> Any:
        raise NotImplementedError("Argument type not supported")

    @__call__.register
    def _(self, listener: Callable) -> Callable:
        if isinstance(listener, MethodType):
            self._register_method(listener)
        else:
            self._register(SENTINEL, listener)
        return listener

    @__call__.register
    def _(self, caller: object) -> Callable:

        def inner(listener: Callable):
            self._register(caller, listener)
            return listener

        return inner

    @abstractmethod
    def trigger(self, *args, **kwds) -> None:
        scheduler.schedule(self, *args, *kwds)

    def _register(self, caller, listener: Callable) -> None:
        listeners = self.listeners.setdefault(caller, [])
        listeners.append(listener)

    def _register_method(self, listener: MethodType) -> None:
        bound_object = listener.__self__
        listeners = self.method_listeners.setdefault(bound_object, [])
        listeners.append(listener)

    def _deregister(self, listener: Callable):
        for listeners in self.listeners.values():
            if listener in listeners:
                listeners.remove(listener)
                # Note: if a listener managed to get in there multiple times,
                # this will only remove one occurence.
                # If that happens, though, something went horribly wrong.
                # See you in 2 years!
                break

    def notify(self, *args, **kwds) -> None:
        """
        Calls all registered listeners, passing along the args and kwds.
        This is never called directly, the instance event subclass will have its own
        defined call method that defines its parameters, which are passed on to the
        listeners.
        """
        for caller, listeners in self.listeners.items():
            if caller is not SENTINEL:
                for listener in listeners:
                    threader.start(listener, *(caller, *args), **kwds)
                continue
            for listener in listeners:
                threader.start(listener, *args, **kwds)
        for method_listeners in self.method_listeners.values():
            for method in method_listeners:
                threader.start(method, *args, **kwds)
