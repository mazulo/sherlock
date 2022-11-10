import imp
import sys
import unittest

sys.path.append("../")
import sherlock as sh

checksymbols = ["_", "-", "."]


class Testmultiple_usernames(unittest.TestCase):
    def test_area(self):
        test_usernames = ["test{?}test", "test{?feo", "test"]
        for name in test_usernames:
            if sh.check_for_parameter(name):
                self.assertAlmostEqual(
                    sh.multiple_usernames(name), ["test_test", "test-test", "test.test"]
                )
            else:
                self.assertAlmostEqual(name, name)
