import unittest

from hair_trigger import scheduler, threader, config


class TestConfig(unittest.TestCase):

    def tearDown(self) -> None:
        config(scheduler.DEFAULT(), threader.DEFAULT())

    def test_scheduler_no_threader(self) -> None:
        """
        Changing only the scheduler, see if the threader remains default.
        """

        config(scheduler=scheduler.QueueScheduler())

        self.assertIsInstance(scheduler._active_scheduler, scheduler.QueueScheduler)
        self.assertIsInstance(threader._active_threader, threader.DEFAULT)

    def test_threader_no_scheduler(self) -> None:
        """
        Changing only the threader, see if the scheduler remains default.
        """

        config(threader=threader.AsyncioThreader())

        self.assertIsInstance(scheduler._active_scheduler, scheduler.DEFAULT)
        self.assertIsInstance(threader._active_threader, threader.AsyncioThreader)

    def test_both(self) -> None:
        """
        Ensure that both change appropriately.
        """

        config(
            scheduler=scheduler.QueueScheduler(), threader=threader.AsyncioThreader()
        )

        self.assertIsInstance(threader._active_threader, threader.AsyncioThreader)
        self.assertIsInstance(scheduler._active_scheduler, scheduler.QueueScheduler)


if __name__ == "__main__":
    unittest.main()
