from __future__ import annotations

from collections import deque
from typing import Any, TYPE_CHECKING

from hair_trigger.typing.scheduler import Scheduler

if TYPE_CHECKING:
    from hair_trigger.event import Event

    type EventArgs = tuple[Event, Any, Any]


class InstantScheduler(Scheduler):
    """
    Default scheduler type, events are run immediately as they happen.
    """

    def schedule(self, event: Event, *args, **kwds) -> None:
        event.notify(*args, **kwds)

    def pump(self) -> None:
        # No backlog to pump
        pass


class StackScheduler(Scheduler):
    """
    Scheduler that stores events and arguments in a stack until called upon.
    """

    def __init__(self) -> None:
        self._scheduled_events: list[EventArgs] = []

    def schedule(self, event: Event, *args, **kwds) -> None:
        self._scheduled_events.append((event, args, kwds))

    def pump(self) -> None:
        while self._scheduled_events:
            event, args, kwds = self._scheduled_events.pop()
            event.notify(*args, **kwds)


class QueueScheduler(Scheduler):
    """
    Scheduler that stores events and arguments in a queue until called upon.
    """

    def __init__(self) -> None:
        self._scheduled_events: deque[EventArgs] = deque()

    def schedule(self, event: Event, *args, **kwds) -> None:
        self._scheduled_events.append((event, args, kwds))

    def pump(self) -> None:
        while self._scheduled_events:
            event, args, kwds = self._scheduled_events.popleft()
            event.notify(*args, **kwds)


DEFAULT: type[Scheduler] = InstantScheduler

_active_scheduler: Scheduler = DEFAULT()


def schedule(event: Event, *args, **kwds) -> None:
    """
    Schedules an event to notify its listeners.

    :param event: The event being scheduled.
    :param args: All position arguments for the event.
    "param kwds: All keyword arguments for the event.
    """
    _active_scheduler.schedule(event, *args, **kwds)


def pump_events() -> None:
    """
    Processes the backlog of events.
    """
    _active_scheduler.pump()
