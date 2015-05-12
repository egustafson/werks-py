import unittest

import werks

class TestEventHandler(object):

    def __init__(self):
        self.triggered = False
        self.arg = None
        self.kw = None

    def callback(self):
        self.triggered = True

    def cb_arg(self, arg):
        self.arg = arg

    def cb_kw(self, kw=None):
        self.kw = kw

    def cb_arg_kw(self, arg, kw=None):
        self.arg = arg
        self.kw = kw



class EventBusTestCases(unittest.TestCase):

    def test_init_eventbus(self):
        b = werks.EventBus()
        self.assertIsNotNone(b)

    
    def test_subscribe_publish(self):
        b = werks.EventBus()
        cb = TestEventHandler()
        b.subscribe("ch1", cb.callback)
        b.publish("ch1")
        self.assertTrue(cb.triggered)


    def test_unsubscribe(self):
        channel_name = "ch1"
        b = werks.EventBus()
        cb1 = TestEventHandler()
        cb2 = TestEventHandler()
        b.subscribe(channel_name, cb1.callback)
        b.subscribe(channel_name, cb2.callback)
        b.unsubscribe(channel_name, cb1.callback)
        b.publish(channel_name)
        self.assertFalse(cb1.triggered)
        self.assertTrue(cb2.triggered)


    def test_pub_no_sub(self):
        b = werks.EventBus()
        b.publish("channel_name")
        self.assertTrue(True)


    def test_pub_with_arg(self):
        channel_name = "ch1"
        arg_value = "arg-value"
        b = werks.EventBus()
        cb = TestEventHandler()
        b.subscribe(channel_name, cb.cb_arg)
        b.publish(channel_name, arg_value)
        self.assertEqual(cb.arg, arg_value)

    
    def test_pub_with_keyword(self):
        channel_name = "ch1"
        kw_value = "kw-value"
        b = werks.EventBus()
        cb = TestEventHandler()
        b.subscribe(channel_name, cb.cb_kw)
        b.publish(channel_name, kw=kw_value)
        self.assertEqual(cb.kw, kw_value)


    def test_multi_pub_with_kw_and_arg(self):
        channel_name = "ch1"
        kw_value = "kw-value"
        arg_value = "arg-value"
        b = werks.EventBus()
        cb1 = TestEventHandler()
        cb2 = TestEventHandler()
        b.subscribe(channel_name, cb1.cb_arg_kw)
        b.subscribe(channel_name, cb2.cb_arg_kw)
        b.publish(channel_name, arg_value, kw=kw_value)
        self.assertEqual(cb1.arg, arg_value)
        self.assertEqual(cb2.arg, arg_value)
        self.assertEqual(cb1.kw, kw_value)
        self.assertEqual(cb2.kw, kw_value)
