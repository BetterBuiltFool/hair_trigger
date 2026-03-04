from __future__ import annotations

from typing import TYPE_CHECKING

import hair_trigger.scheduler as scheduler_module
import hair_trigger.threader as threader_module

if TYPE_CHECKING:
    from hair_trigger.typing import Scheduler, Threader


def config(
    scheduler: Scheduler | None = None,
    threader: Threader | None = None,
) -> None:
    """
    Allows for setting how hair_trigger handle threading and scheduling of events.

    Threaders are found in hair_trigger.threader.

    Schedulers are found in hair_trigger.scheduler.

    :param scheduler: A new scheduler to replace the active scheduler, defaults to None.
        Will not replace the current scheduler if none is passed.
    :param threader: A new threader to replace the active threader, defaults to None.
        Will not replace the current threader if none is passed.
    """
    if scheduler:
        scheduler_module._active_scheduler = scheduler
    if threader:
        threader_module._active_threader = threader
