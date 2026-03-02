from __future__ import annotations

import asyncio
import threading
from typing import Any, TYPE_CHECKING

from .typing.scheduler import Scheduler

if TYPE_CHECKING:
    from collections.abc import Callable


class SyncScheduler(Scheduler):
    """
    Default, synchronous scheduler that simple calls the callable.
    """

    def schedule(self, func: Callable[..., Any], *args, **kwds) -> None:
        func(*args, **kwds)


class ThreadScheduler(Scheduler):
    """
    Simple asynchronous scheduler using the python threading library.
    """

    def schedule(self, func: Callable[..., Any], *args, **kwds) -> None:
        threading.Thread(target=func, args=args, kwargs=kwds).start()


class AsyncioScheduler(Scheduler):
    """
    Scheduler that relies on asyncio, useful for web deployment where python.threading
    doesn't work properly.
    """

    def schedule(self, func: Callable[..., Any], *args, **kwds) -> None:
        asyncio.create_task(func(*args, **kwds))


_active_scheduler: Scheduler = SyncScheduler()


def schedule(func: Callable, *args, **kwds) -> None:
    _active_scheduler.schedule(func, *args, **kwds)
