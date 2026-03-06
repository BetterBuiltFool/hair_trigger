import unittest

from hair_trigger import runner, scheduler, config


class TestConfig(unittest.TestCase):

    def tearDown(self) -> None:
        config(scheduler.DEFAULT(), runner.DEFAULT())

    def test_scheduler_no_threader(self) -> None:
        """
        Changing only the scheduler, see if the threader remains default.
        """

        config(scheduler=scheduler.QueueScheduler())

        self.assertIsInstance(scheduler._active_scheduler, scheduler.QueueScheduler)
        self.assertIsInstance(runner._active_threader, runner.DEFAULT)

    def test_threader_no_scheduler(self) -> None:
        """
        Changing only the threader, see if the scheduler remains default.
        """

        config(threader=runner.AsyncioThreader())

        self.assertIsInstance(scheduler._active_scheduler, scheduler.DEFAULT)
        self.assertIsInstance(runner._active_threader, runner.AsyncioThreader)

    def test_both(self) -> None:
        """
        Ensure that both change appropriately.
        """

        config(scheduler=scheduler.QueueScheduler(), threader=runner.AsyncioThreader())

        self.assertIsInstance(runner._active_threader, runner.AsyncioThreader)
        self.assertIsInstance(scheduler._active_scheduler, scheduler.QueueScheduler)


if __name__ == "__main__":
    unittest.main()
