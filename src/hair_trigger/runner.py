from __future__ import annotations

import asyncio
import threading
from typing import Any, TYPE_CHECKING

from hair_trigger.typing.runner import Runner

if TYPE_CHECKING:
    from collections.abc import Callable


class SyncRunner(Runner):
    """
    Default, synchronous runner that simple calls the callable.
    """

    def start(self, func: Callable[..., Any], *args, **kwds) -> None:
        func(*args, **kwds)


class ThreadRunner(Runner):
    """
    Simple asynchronous runner using the python threading library.
    """

    def start(self, func: Callable[..., Any], *args, **kwds) -> None:
        threading.Thread(target=func, args=args, kwargs=kwds).start()


class AsyncioRunner(Runner):
    """
    Runner that relies on asyncio, useful for web deployment where python.threading
    doesn't work properly.
    """

    def start(self, func: Callable[..., Any], *args, **kwds) -> None:
        asyncio.create_task(func(*args, **kwds))


DEFAULT: type[Runner] = SyncRunner

_active_runner: Runner = DEFAULT()


def start(func: Callable[..., Any], *args, **kwds) -> None:
    _active_runner.start(func, *args, **kwds)
