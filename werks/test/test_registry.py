import unittest

import werks


class RegistryTestCases(unittest.TestCase):

    def test_init_registry(self):
        r = werks.Registry()
        self.assertIsNotNone(r)

    def test_register_lookup(self):
        v = 1
        r = werks.Registry()
        r.register("key", v)
        lu = r.lookup("key")
        self.assertEqual(lu, v)
