import io
import unittest
import unittest.mock

from hair_trigger.event import Event, SENTINEL


class OnTestEvent1(Event):

    def trigger(self, param1: bool) -> None:
        return super().trigger(param1)


class OnTestEvent2(Event):

    def trigger(self, param2: int) -> None:
        return super().trigger(param2)


class TestObject:

    def __init__(self) -> None:
        self.OnTestEvent1 = OnTestEvent1()
        self.OnTestEvent2 = OnTestEvent2()
        self.param1 = True
        self.param2 = 8

    def call_event_1(self):
        self.OnTestEvent1.trigger(self.param1)

    def call_event_2(self):
        self.OnTestEvent2.trigger(self.param2)


class TestInstanceEvent(unittest.TestCase):

    def setUp(self) -> None:
        self.test_object = TestObject()

    def tearDown(self) -> None:
        self.test_object.OnTestEvent1.listeners.clear()
        self.test_object.OnTestEvent2.listeners.clear()

    def test_register(self):

        def test_dummy():
            pass

        self.test_object.OnTestEvent1._register(SENTINEL, test_dummy)

        callables = self.test_object.OnTestEvent1.listeners.get(SENTINEL)

        assert callables is not None

        self.assertIn(test_dummy, callables)

    def test_deregister(self):

        def test_dummy():
            pass

        self.test_object.OnTestEvent1._register(SENTINEL, test_dummy)

        callables = self.test_object.OnTestEvent1.listeners.get(SENTINEL)

        assert callables is not None

        self.assertIn(test_dummy, callables)

        self.test_object.OnTestEvent1._deregister(test_dummy)

        callables = self.test_object.OnTestEvent1.listeners.get(SENTINEL)

        assert callables is not None

        self.assertNotIn(test_dummy, callables)

    def test_call_registration(self):

        @self.test_object.OnTestEvent1
        def test_dummy(param1: bool):
            pass

        callables = self.test_object.OnTestEvent1.listeners.get(SENTINEL)

        assert callables is not None

        self.assertIn(test_dummy, callables)

        event1 = self.test_object.OnTestEvent1

        class TestItem:
            def __init__(self) -> None:
                @event1(self)
                def _(self):
                    pass

                event1(self.test_method)

            def test_method(self, param1: bool) -> None:
                pass

        test_item = TestItem()

        self.assertTrue(event1.listeners.get(test_item))

        self.assertTrue(event1.method_listeners.get(test_item))

        self.assertIn(test_item.test_method, event1.method_listeners.get(test_item, []))

    def test_notify(self):

        self.value1 = None

        @self.test_object.OnTestEvent1
        def test_dummy(param1: bool):
            self.value1 = param1

        self.assertIsNone(self.value1)

        self.test_object.OnTestEvent1._notify(True)

        self.assertTrue(self.value1)

    def test_notify_method(self) -> None:

        event1 = self.test_object.OnTestEvent1

        class TestItem:

            def __init__(self) -> None:
                self.param1: bool = False

                event1(self.test_method)

            def test_method(self, param1: bool) -> None:
                self.param1 = param1

        test_item = TestItem()

        self.assertFalse(test_item.param1)

        self.test_object.OnTestEvent1._notify(True)

        self.assertTrue(test_item.param1)

    def test_notify_lambda(self) -> None:

        with unittest.mock.patch("sys.stdout", new=io.StringIO()) as output_catcher:
            test_value = 1
            self.test_object.OnTestEvent2(lambda param2: print(param2))

            self.test_object.OnTestEvent2.trigger(test_value)

            output = output_catcher.getvalue()

            self.assertEqual(int(output), test_value)

    def test_call_(self):

        self.value1 = None
        self.value2 = None

        @self.test_object.OnTestEvent1
        def test_dummy(param1: bool):
            self.value1 = param1

        # listeners on two separate events
        @self.test_object.OnTestEvent2
        def test_dummy2(param2: int):
            self.value2 = param2

        self.assertIsNone(self.value1)
        self.assertIsNone(self.value2)

        self.test_object.call_event_1()

        self.assertTrue(self.value1)
        self.assertIsNone(self.value2)

        self.test_object.call_event_2()

        self.value1 = None

        self.assertIsNone(self.value1)
        self.assertEqual(self.value2, 8)

    def test_multiple_listeners(self):

        self.value1 = None
        self.value2 = None

        @self.test_object.OnTestEvent1
        def dummy1(param1):
            self.value1 = param1

        # listener of _same_ event
        @self.test_object.OnTestEvent1
        def dummy2(param1):
            self.value2 = param1

        self.assertIsNone(self.value1)
        self.assertIsNone(self.value2)

        self.test_object.call_event_1()

        self.assertTrue(self.value1)
        self.assertTrue(self.value2)


if __name__ == "__main__":
    unittest.main()
