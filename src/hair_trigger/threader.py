from __future__ import annotations

import asyncio
import threading
from typing import Any, TYPE_CHECKING

from .typing.threader import Threader

if TYPE_CHECKING:
    from collections.abc import Callable


class SyncThreader(Threader):
    """
    Default, synchronous threader that simple calls the callable.
    """

    def start(self, func: Callable[..., Any], *args, **kwds) -> None:
        func(*args, **kwds)


class ThreadThreader(Threader):
    """
    Simple asynchronous threader using the python threading library.
    """

    def start(self, func: Callable[..., Any], *args, **kwds) -> None:
        threading.Thread(target=func, args=args, kwargs=kwds).start()


class AsyncioThreader(Threader):
    """
    threader that relies on asyncio, useful for web deployment where python.threading
    doesn't work properly.
    """

    def start(self, func: Callable[..., Any], *args, **kwds) -> None:
        asyncio.create_task(func(*args, **kwds))


_active_threader: Threader = SyncThreader()


def start(func: Callable[..., Any], *args, **kwds) -> None:
    _active_threader.start(func, *args, **kwds)
