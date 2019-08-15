import unittest
from SATCollision import *


class MyTestCase(unittest.TestCase):
    def test_generating_bounds(self):
        # Testing if generated_bounds_from works.

        control_bounds = BoundingBox(0, 0, 100, 100)
        control_shape = [Vector2(0, 0), Vector2(100, 0), Vector2(100, 100), Vector2(0, 100), Vector2(0, 0)]

        generated_bounds = BoundingBox.generate_bounds_from(control_shape)
        self.assertEqual(control_bounds, generated_bounds)

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

    def test_sat(self):
        control_shape1 = [(0, 0), (0, 10), (10, 10), (10, 0), (0, 0)]
        control_shape2 = [Vector2(tuple_vector[0], tuple_vector[1]) + Vector2(5, 5) for tuple_vector in control_shape1]
        control_shape3 = [vector + Vector2(20, 20) for vector in control_shape2]
        self.assertEqual(IntersectTester(control_shape2, control_shape1).test_major().intersection, True)
        self.assertEqual(IntersectTester(control_shape2, control_shape3).test_major().intersection, False)

    def test_minor(self):
        control_shape1 = [(0, 0), (0, 10), (10, 10), (10, 0), (0, 0)]
        control_shape2 = [Vector2(tuple_vector[0], tuple_vector[1]) + Vector2(5, 5) for tuple_vector in control_shape1]
        self.assertEqual(BoundingBox.generate_bounds_from(control_shape1).
                         intersects_with(BoundingBox.generate_bounds_from(control_shape2)), True)
        self.assertEqual(BoundingBox.generate_bounds_from([vector + Vector2(30, 30) for vector in control_shape2]).
                         intersects_with(BoundingBox.generate_bounds_from(control_shape2)), False)

    def test_major(self):
        control_shape1 = [(0, 0), (0, 10), (10, 10), (10, 0), (0, 0)]
        control_shape2 = [Vector2(tuple_vector[0], tuple_vector[1]) + Vector2(5, 5) for tuple_vector in control_shape1]
        self.assertEqual(IntersectTester(control_shape1, control_shape2).test_major().intersection, True)

        control_shape3 = [el + Vector2(100, 100) for el in control_shape2]
        self.assertEqual(IntersectTester(control_shape1, control_shape3).test_major().intersection, False)

    def test_full(self):
        control_shape1 = [Vector2.from_tuple(vertex) for vertex in [(0, 0), (0, 10), (10, 10), (10, 0), (0, 0)]]

        result = IntersectTester(control_shape1, [vertex + Vector2(5, 5) for vertex in control_shape1]).test_full()
        self.assertEqual(result.intersection, True)

        self.assertEqual(IntersectTester(control_shape1, [vertex + Vector2(15, 15) for vertex in control_shape1])
                         .test_full().intersection, False)
        print(result)

# Could maybe handle a shape as a wrapper, could chain methods like shape.test_major(otherShape)


if __name__ == '__main__':
    unittest.main()
