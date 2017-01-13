import unittest

import werks.bus


class TestEventHandler(werks.bus.EventHandler):

    def __init__(self, bus):
        self.triggered = False
        super(TestEventHandler, self).__init__(bus)

    def channel_name(self):
        self.triggered = True



class EventHandlerTestCase(unittest.TestCase):

    def test_event_handler(self):
        b = werks.bus.EventBus()
        b.add_channel("channel_name")
        eh = TestEventHandler(b)
        eh.subscribe()
        b.publish("channel_name")
        self.assertTrue(eh.triggered)
        #
        # Reset and verify unsubscribe works
        #
        eh.triggered = False
        eh.unsubscribe()
        b.publish("channel_name")
        self.assertFalse(eh.triggered)

