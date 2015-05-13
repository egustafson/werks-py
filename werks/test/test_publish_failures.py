import unittest

import werks

class TestFailure(Exception):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        

class FailingEventHandler(object):

    def callback(self):
        raise TestFailure()


class BusSubscriberExceptionTestCase(unittest.TestCase):

    def test_exception_thrown(self):
        b = werks.EventBus()
        cb = FailingEventHandler()
        b.subscribe("ch1", cb.callback)
        with self.assertRaises(werks.PublishFailures):
            b.publish("ch1")


    def test_nested_exeception_thrown(self):
        b = werks.EventBus()
        cb = FailingEventHandler()
        b.subscribe("ch1", cb.callback)
        try:
            b.publish("ch1")
            self.fail("publish should have thrown")
        except werks.PublishFailures as err:
            nested = err.get_instances()
            self.assertTrue( len(nested) == 1 )
            self.assertIsInstance( nested[0], TestFailure )
            self.assertTrue( err.__bool__() )
            #
            # just exercise the __str__ method
            string = err.__str__()
