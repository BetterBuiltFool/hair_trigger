from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any
    from hair_trigger.event import Event


class Scheduler(Protocol):
    """
    Object used for following through on func registered to events.
    """

    def schedule(self, event: Event[Any], *args, **kwds) -> None:
        """
        Schedules a event to be triggered.

        :param event: Event to be scheduled.
        :type event: Event
        :param args: Pass-through positional arguments for _event_.
        :type args: Any
        :param kwds: Pass-through keyword arguments for _event_.
        :type kwds: Any
        """
        ...

    def pump(self) -> None:
        """
        Processes all pending events, if any.
        Will attempt to run until backlog is cleared.
        """
        ...
