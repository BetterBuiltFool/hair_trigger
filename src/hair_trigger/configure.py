from __future__ import annotations

from typing import TYPE_CHECKING

import hair_trigger.scheduler as scheduler_module
import hair_trigger.runner as runner_module

if TYPE_CHECKING:
    from hair_trigger.typing import Scheduler, Runner


def config(
    scheduler: Scheduler | None = None,
    runner: Runner | None = None,
) -> None:
    """
    Allows for setting how hair_trigger handle threading and scheduling of events.

    Runners are found in hair_trigger.runner.

    Schedulers are found in hair_trigger.scheduler.

    :param scheduler: A new scheduler to replace the active scheduler, defaults to None.
        Will not replace the current scheduler if none is passed.
    :param runner: A new runner to replace the active runner, defaults to None.
        Will not replace the current runner if none is passed.
    """
    if scheduler:
        scheduler_module._active_scheduler = scheduler
    if runner:
        runner_module._active_runner = runner
