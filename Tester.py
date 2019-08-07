import unittest
from SATCollision import *


class MyTestCase(unittest.TestCase):
    def test_generating_bounds(self):
        # Testing if generated_bounds_from works.

        control_bounds = BoundingBox(0, 0, 100, 100)
        control_shape = [Vector2(0, 0), Vector2(100, 0), Vector2(100, 100), Vector2(0, 100), Vector2(0, 0)]

        generated_bounds = BoundingBox.generate_bounds_from(control_shape)
        self.assertEqual(control_bounds.x, generated_bounds.x)
        self.assertEqual(control_bounds.y, generated_bounds.y)
        self.assertEqual(control_bounds.height, generated_bounds.height)
        self.assertEqual(control_bounds.width, generated_bounds.width)

    def test_intersects_with(self):
        # Testing if intersects returns true.

        control_bounds = BoundingBox(0, 0, 100, 100)
        self.assertEqual(control_bounds.intersects_with(BoundingBox(10, 10, 110, 110)), True)
        self.assertEqual(control_bounds.intersects_with(BoundingBox(200, 200, 10, 10)), False)

    def test_intersects_with_types(self):
        # Testing the intersects_with method's type checking.

        control_bounds = BoundingBox(0, 0, 100, 100)
        with self.assertRaises(TypeError):
            control_bounds.intersects_with(False)


if __name__ == '__main__':
    unittest.main()
