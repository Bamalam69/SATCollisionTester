import unittest
from SATCollision import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(BoundingBox(0, 0, 100, 100).intersects_with(BoundingBox(10, 10, 110, 110)), True)

        with self.assertRaises(TypeError):
            BoundingBox(0, 0, 100, 100).intersects_with(False)


if __name__ == '__main__':
    unittest.main()
