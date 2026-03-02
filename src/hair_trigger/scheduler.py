from __future__ import annotations

from typing import Any, TYPE_CHECKING
from weakref import WeakKeyDictionary

from .typing.scheduler import Scheduler

if TYPE_CHECKING:
    from hair_trigger.event import Event

    type EventArgs = tuple[Any, Any]


class InstantScheduler(Scheduler):
    """
    Default scheduler type, events are run immediately as they happen.
    """

    def schedule(self, event: Event[Any], *args, **kwds) -> None:
        event._notify(*args, **kwds)


class DeferredScheduler(Scheduler):
    """
    Scheduler that stores events and arguments until called upon.
    """

    def __init__(self) -> None:
        self._scheduled_events: WeakKeyDictionary[Event, EventArgs] = (
            WeakKeyDictionary()
        )

    def schedule(self, event: Event[Any], *args, **kwds) -> None:
        self._scheduled_events[event] = (args, kwds)


_active_scheduler: Scheduler = InstantScheduler()


def schedule(event: Event[Any], *args, **kwds) -> None:
    _active_scheduler.schedule(event, *args, **kwds)
