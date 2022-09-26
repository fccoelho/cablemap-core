import unittest
from cablemap.core import cables_from_source


class TestSource(unittest.TestCase):
    def test_from_source(self):
        fname = "../cables.csv"
        i = 0
        for cable in cables_from_source(fname):
            self.assertIsInstance(cable.subject, str)
            self.assertIsInstance(cable.created, str)
            if i > 5:
                break
            i += 1



if __name__ == '__main__':
    unittest.main()
