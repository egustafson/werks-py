import unittest

import werks.bus


class RegistryTestCases(unittest.TestCase):

    def test_init_registry(self):
        r = werks.bus.Registry()
        self.assertIsNotNone(r)

    def test_register_lookup(self):
        v = 1
        r = werks.bus.Registry()
        r.register("key", v)
        lu = r.lookup("key")
        self.assertEqual(lu, v)
