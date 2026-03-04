import unittest

from hair_trigger import scheduler, event


class OnTestEvent(event.Event):
    """
    Provides a list and a number.
    """

    def trigger(self, list_: list[int], number: int) -> None:
        return super().trigger(list_, number)


class Dummy:
    pass


class TestInstantScheduler(unittest.TestCase):

    def setUp(self) -> None:
        scheduler._active_scheduler = scheduler.InstantScheduler()

    def test_order(self) -> None:
        """
        Tests the resulting order of event calls.
        This is assuming usage of the sync threader. Any async threader will result in
        race conditions that cause unpredicatable order.
        """
        numbers = [1, 2, 3]

        dummy_owner = Dummy()

        test_event_1 = OnTestEvent(dummy_owner)
        test_event_2 = OnTestEvent(dummy_owner)
        test_event_3 = OnTestEvent(dummy_owner)

        @test_event_1
        def _(list_: list[int], number: int) -> None:
            # Event is triggered before appending, so the next event does its thing
            # before we can add the number to the list.
            test_event_2.trigger(list_, numbers[1])
            test_event_3.trigger(list_, numbers[2])
            list_.append(number)

        @test_event_2
        def _(list_: list[int], number: int) -> None:
            test_event_3.trigger(list_, numbers[2])
            list_.append(number)

        @test_event_3
        def _(list_: list[int], number: int) -> None:
            list_.append(number)

        test_list: list[int] = []

        test_event_1.trigger(test_list, numbers[0])

        # Since we're instant, we flow through to the deepest event first, and resolve
        # backwards. The extra call is second to last, so it appends second to last.
        self.assertEqual(test_list, [3, 2, 3, 1])


class TestQueueScheduler(unittest.TestCase):

    def setUp(self) -> None:
        scheduler._active_scheduler = scheduler.QueueScheduler()

    def test_order(self) -> None:
        """
        Tests the resulting order of event calls.
        This is assuming usage of the sync threader. Any async threader will result in
        race conditions that cause unpredicatable order.
        """
        numbers = [1, 2, 3]

        dummy_owner = Dummy()

        test_event_1 = OnTestEvent(dummy_owner)
        test_event_2 = OnTestEvent(dummy_owner)
        test_event_3 = OnTestEvent(dummy_owner)

        @test_event_1
        def _(list_: list[int], number: int) -> None:
            # Event added to the queue
            test_event_2.trigger(list_, numbers[1])
            test_event_3.trigger(list_, numbers[2])
            list_.append(number)

        @test_event_2
        def _(list_: list[int], number: int) -> None:
            test_event_3.trigger(list_, numbers[2])
            list_.append(number)

        @test_event_3
        def _(list_: list[int], number: int) -> None:
            list_.append(number)

        test_list: list[int] = []

        test_event_1.trigger(test_list, numbers[0])

        # Need to manually pump the queue
        scheduler.pump_events()

        # Since we're in a queue, the listeners fully resolve before the next event is
        # run, and the events run in the order in which they are triggered. So, the '3'
        # event is triggered twice in a row.
        self.assertEqual(test_list, [1, 2, 3, 3])


class TestStackScheduler(unittest.TestCase):

    def setUp(self) -> None:
        scheduler._active_scheduler = scheduler.StackScheduler()

    def test_order(self) -> None:
        """
        Tests the resulting order of event calls.
        This is assuming usage of the sync threader. Any async threader will result in
        race conditions that cause unpredicatable order.
        """
        numbers = [1, 2, 3]

        dummy_owner = Dummy()

        test_event_1 = OnTestEvent(dummy_owner)
        test_event_2 = OnTestEvent(dummy_owner)
        test_event_3 = OnTestEvent(dummy_owner)

        @test_event_1
        def _(list_: list[int], number: int) -> None:
            # Event added to the queue
            test_event_2.trigger(list_, numbers[1])
            test_event_3.trigger(list_, numbers[2])
            list_.append(number)

        @test_event_2
        def _(list_: list[int], number: int) -> None:
            test_event_3.trigger(list_, numbers[2])
            list_.append(number)

        @test_event_3
        def _(list_: list[int], number: int) -> None:
            list_.append(number)

        test_list: list[int] = []

        test_event_1.trigger(test_list, numbers[0])

        # Need to manually pump the queue
        scheduler.pump_events()

        # Since we're in a stack, the listeners fully resolve before the next event is
        # run, and new events run before older events. So, the first '3' event is
        # triggered before the '2' event.
        self.assertEqual(test_list, [1, 3, 2, 3])


if __name__ == "__main__":
    unittest.main()
