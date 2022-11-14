import unittest
from difflib import SequenceMatcher

from sherlock.utils import check_for_parameter, multiple_usernames

checksymbols = ["_", "-", "."]


class TestMultipleUsernames(unittest.TestCase):
    def test_area(self):
        test_usernames = ["test{?}test", "test{?feo", "test"]
        for name in test_usernames:
            if check_for_parameter(name):
                names = zip(multiple_usernames(name), ["test_test", "test-test", "test.test"])
                for name1, name2 in names:
                    ratio = SequenceMatcher(a=name1, b=name2).ratio()
                    self.assertAlmostEqual(ratio, 1.0)
            else:
                ratio = SequenceMatcher(a=name, b=name).ratio()
                self.assertAlmostEqual(ratio, 1.0)
