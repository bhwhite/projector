import unittest

from .. import asset

class AssetTest(unittest.TestCase):
    def test_asset(self):
        a = asset.Asset('SP500')
        self.assertTrue(a is not None)

