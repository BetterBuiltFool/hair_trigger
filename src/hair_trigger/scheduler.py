from __future__ import annotations

from collections import deque
from typing import Any, TYPE_CHECKING

from .typing.scheduler import Scheduler

if TYPE_CHECKING:
    from hair_trigger.event import Event

    type EventArgs = tuple[Event, Any, Any]


class InstantScheduler(Scheduler):
    """
    Default scheduler type, events are run immediately as they happen.
    """

    def schedule(self, event: Event[Any], *args, **kwds) -> None:
        event._notify(*args, **kwds)


class StackScheduler(Scheduler):
    """
    Scheduler that stores events and arguments in a stack until called upon.
    """

    def __init__(self) -> None:
        self._scheduled_events: list[EventArgs] = []

    def schedule(self, event: Event[Any], *args, **kwds) -> None:
        self._scheduled_events.append((event, args, kwds))


class QueueScheduler(Scheduler):
    """
    Scheduler that stores events and arguments in a queue until called upon.
    """

    def __init__(self) -> None:
        self._scheduled_events: deque[EventArgs] = deque()

    def schedule(self, event: Event[Any], *args, **kwds) -> None:
        self._scheduled_events.append((event, args, kwds))


_active_scheduler: Scheduler = InstantScheduler()


def schedule(event: Event[Any], *args, **kwds) -> None:
    _active_scheduler.schedule(event, *args, **kwds)


def process() -> None:
    """
    Processes the backlog of events.
    """
