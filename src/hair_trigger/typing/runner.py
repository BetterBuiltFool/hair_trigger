from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any


class Runner(Protocol):
    """
    Runners call a callable with supplied arguments in one way or another, with the
    specific behavior being implementation defined.
    """

    def start(self, func: Callable[..., Any], *args, **kwds) -> None:
        """
        Runs the supplied callable with the supplied arguments.

        :param func: A callable, function or method, to be initiated.
        :param args: All positional arguments for _func_.
        :param kwds: All keyword arguments for _func_.
        """
        ...
