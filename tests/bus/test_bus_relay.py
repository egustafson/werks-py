import unittest

import werks.bus

class TestCountingRelay(object):

    def __init__(self, event_bus, out_channel):
        self.bus = event_bus
        self.ch = out_channel
        self.count = 0

    def callback(self, arg):
        self.count += 1
        self.bus.publish(self.ch, arg)


class TestQueuingEventHandler(object):

    def __init__(self):
        self.args = []

    def callback(self, arg):
        self.args.append(arg)



class EventBusRelayTestCase(unittest.TestCase):

    def setUp(self):
        self.input_ch = "input-ch"
        relay_ch = "relay-ch"
        self.b = werks.bus.EventBus()
        r = TestCountingRelay(self.b, relay_ch)
        self.cb = TestQueuingEventHandler()
        self.b.subscribe(self.input_ch, r.callback)
        self.b.subscribe(relay_ch, self.cb.callback)


    def tearDown(self):
        self.input_ch = None
        self.b = None
        self.cb = None

    def test_single_relay(self):
        arg = "test-argument"
        self.b.publish(self.input_ch, arg)
        self.assertSequenceEqual(self.cb.args, [arg])

    def test_multi_relay(self):
        args = list(range(100))
        for x in args:
            self.b.publish(self.input_ch, x)
        self.assertSequenceEqual(self.cb.args, args)
