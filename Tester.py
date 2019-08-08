import unittest
import SATCollision


class MyTestCase(unittest.TestCase):
    def test_generating_bounds(self):
        # Testing if generated_bounds_from works.

        control_bounds = SATCollision.BoundingBox(0, 0, 100, 100)
        control_shape = [SATCollision.Vector2(0, 0), SATCollision.Vector2(100, 0), SATCollision.Vector2(100, 100), SATCollision.Vector2(0, 100), SATCollision.Vector2(0, 0)]

        generated_bounds = SATCollision.BoundingBox.generate_bounds_from(control_shape)
        self.assertEqual(control_bounds.x, generated_bounds.x)
        self.assertEqual(control_bounds.y, generated_bounds.y)
        self.assertEqual(control_bounds.height, generated_bounds.height)
        self.assertEqual(control_bounds.width, generated_bounds.width)

    def test_intersects_with(self):
        # Testing if intersects returns true.

        control_bounds = SATCollision.BoundingBox(0, 0, 100, 100)
        self.assertEqual(control_bounds.intersects_with(SATCollision.BoundingBox(10, 10, 110, 110)), True)
        self.assertEqual(control_bounds.intersects_with(SATCollision.BoundingBox(200, 200, 10, 10)), False)

    def test_intersects_with_types(self):
        # Testing the intersects_with method's type checking.

        control_bounds = SATCollision.BoundingBox(0, 0, 100, 100)
        with self.assertRaises(TypeError):
            control_bounds.intersects_with(False)

    def test_sat(self):
        control_shape1 = [(0, 0), (0, 10), (10, 10), (10, 0), (0, 0)]
        control_shape2 = [SATCollision.Vector2(tuple_vector[0], tuple_vector[1]) + SATCollision.Vector2(5, 5) for tuple_vector in control_shape1]
        control_shape3 = [vector + SATCollision.Vector2(20, 20) for vector in control_shape2]
        self.assertEqual(SATCollision.IntersectTester(control_shape2, control_shape1).test_major(), True)
        self.assertEqual(SATCollision.IntersectTester(control_shape2, control_shape3).test_major(), False)

    def test_aabb(self):
        control_shape1 = [(0, 0), (0, 10), (10, 10), (10, 0), (0, 0)]
        control_shape2 = [SATCollision.Vector2(tuple_vector[0], tuple_vector[1]) + SATCollision.Vector2(5, 5) for tuple_vector in control_shape1]
        self.assertEqual(SATCollision.BoundingBox.generate_bounds_from(control_shape1).
                         intersects_with(SATCollision.BoundingBox.generate_bounds_from(control_shape2)), True)
        self.assertEqual(SATCollision.BoundingBox.generate_bounds_from([vector + SATCollision.Vector2(30, 30) for vector in control_shape2]).
                         intersects_with(SATCollision.BoundingBox.generate_bounds_from(control_shape2)), False)

# Could maybe handle a shape as a wrapper, could chain methods like shape.test_major(otherShape)


if __name__ == '__main__':
    unittest.main()
help(SATCollision)
