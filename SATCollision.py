"""
A module for determining whether or
not an intersection between two convex shapes are occurring.
"""
from typing import List


class IntersectTester:
    """
    A class used to test for intersections between shapes represented by lists of vertices.
    """
    def __init__(self, pol1, pol2):
        """
        Spawns an instance of an InterestTester provided the actual shapes to test for.
        Ensure that both the inputted polygons are not the same.
        :param pol1: 1 of 2 polygons that a collision will be tested for.
        :param pol2: 1 of 2 polygons that a collision will be tested for.
        """
        self.pol1 = pol1
        self.pol2 = pol2

    def test_minor(self):
        """
        Performs only a check against the polygons bounding boxes. May provide inconsistent
        information about the intersection as a single axis-aligned bounding box check
        is not very accurate.
        """
        bounds1 = BoundingBox.generate_bounds_from(self.pol1)
        bounds2 = BoundingBox.generate_bounds_from(self.pol2)
        return bounds1.intersects_with(bounds2)

    def test_major(self):
        """
        Performs only the SAT algorithm to determine an intersection result. Can be inefficient when used
        without the test_minor method as there may not even be an intersection between the two shapes
        and now you're running through an entire SAT algorithm to check for an intersection. When used with test_minor,
        it will inform you of the possibility of a current intersection between the two shapes.
        :return:
        """
        normals1 = IntersectTester._get_normals_from(self.pol1)
        normals2 = IntersectTester._get_normals_from(self.pol2)
        normals = normals1 + normals2

        for normal in normals:
            p1 = IntersectTester.projection_from_onto(self.pol1, normal)
            p2 = IntersectTester.projection_from_onto(self.pol2, normal)

            if not p1.overlaps(p2):
                # No Intersection. Quit algorithm right away.
                return IntersectResult(False, None)

        # If execution gets to this point, the algorithm did not return and thus there is an intersection
        # between the two shapes.
        return IntersectResult(True, None)

    def test_full(self):
        """
        Performs a full test - that is the preliminary bounding box check for performance and the SAT algorithm - on the
        given polygons inputted when this instance was spawned.
        :return: IntersectResult containing information representing whether there is an intersection
        between the two polygons.
        """
        bounds_is_intersecting = self.test_minor()
        if bounds_is_intersecting:
            return self.test_major()
        return False

    @staticmethod
    def _get_normals_from(polygon):
        """
        :param polygon: The polygon to get edge normals from.
        :return: Retrieves the edge normals of the provided convex polygon.
        """
        normals: List[Vector2] = []  # List hint...
        for i in range(len(polygon)):
            vertexVector1 = Vector2.from_tuple(polygon[i])
            if i + 1 == len(polygon):
                return normals
            else:
                vertexVector2 = Vector2.from_tuple(polygon[i + 1])
            edge = vertexVector1 - vertexVector2
            normals.append(edge.get_perpendicular())
        return normals

    @staticmethod
    def projection_from_onto(pol1, axis):
        """
        Makes a Projection of the inputted shape onto the
        provided axis.
        :param pol1: The 2D polygon to be projected.
        :param axis: The Axis to project the polygon onto.
        :return: A ShapeProjection.
        """
        minimum = 9999999
        maximum = -9999999
        for vertex in pol1:
            vecVertex = Vector2.from_tuple(vertex)
            p = Vector2.dot_product(axis, vecVertex)
            if p < minimum:
                minimum = p
            elif p > maximum:
                maximum = p
        return ShapeProjection(minimum, maximum)


class BoundingBox:
    """
    Represents an axis-aligned BoundingBox - AABB.
    Consists of an x and a y coordinate representing the top
    left corner of the box, and a width and height
    value for the width and height of the bounding box.
    """

    def __init__(self, x, y, width, height):
        """
        Creates an instance of BoundingBox.
        :param x: x coordinate of the top left corner of the bounding box.
        :param y: y coordinate of the top left corner of the bounding box.
        :param width: Width of the bounding box.
        :param height: Height of the bounding box.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return "Bounding Box(X: " + str(self.x) + " Y: " + str(self.y) + " Width: " + str(self.width) + \
               " Height: " + str(self.height) + ")"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.height == other.height and self.width == other.width

    def intersects_with(self, other):
        """
        Checks for an intersection between itself and the other provided bounding box.
        :param other: The other bounding box to if intersecting. Will raise a
        TypeError if 'other' is not a BoundingBox.
        :return: A boolean - true for an intersection.
        """
        # Type checking to throw an error if the user inputted something other than a BoundingBox
        # otherwise Python will throw it's own vague error.
        if not isinstance(other, BoundingBox):
            raise TypeError("Incorrect type for parameter 'other'. Expected a BoundingBox not: " + type(other).__name__)

        return self.x < other.x + other.width \
            and self.x + self.width > other.x \
            and self.y < other.y + other.height \
            and self.y + self.height > other.y

    @staticmethod
    def generate_bounds_from(pol1):
        """
        Creates a bounding box from the inputted polygon.
        :param pol1: The polygon represented by list of vertices.
        :return: An axis-aligned bounding box from the provided shape.
        """
        min_vec = Vector2(9999999, 99999999)
        max_vec = Vector2(-9999999, -99999999)
        for vertex in pol1:
            vector_vertex = Vector2.from_tuple(vertex)
            if vector_vertex.x > max_vec.x:
                max_vec.x = vector_vertex.x
            if vector_vertex.x <= min_vec.x:
                min_vec.x = vector_vertex.x

            if vector_vertex.y > max_vec.y:
                max_vec.y = vector_vertex.y
            if vector_vertex.y <= min_vec.y:
                min_vec.y = vector_vertex.y

        return BoundingBox(min_vec.y, min_vec.y, max_vec.x - min_vec.x, max_vec.y - min_vec.y)


class Vector2:
    def __init__(self, x, y):
        """
        Initializes a new Vector2
        :param x: The x coordinate
        :param y: The y coordinate
        """
        self.x = x
        self.y = y

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    # Operator overloads...
    # Division
    def __truediv__(self, scalar):
        """
        :return: Division between Vector2 and scalar. Vector2(1, 1) / 2.0 = Vector2(0.5, 0.5)
        """
        return Vector2(self.x / scalar, self.y / scalar)

    # Multiplication
    def __mul__(self, scalar):
        """
        :return: Vector2 multiplied by scalar. Vector2(1, 1) * 2 = Vector2(2, 2)
        """
        return Vector2(self.x * scalar, self.y * scalar)

    # Addition
    def __add__(self, other):
        """
        :return: Vector2(2, 2) + Vector2(2, 2) = Vector2(4, 4)
        """
        return Vector2(self.x + other.x, self.y + other.y)

    # Subtraction
    def __sub__(self, other):
        """
        :return: Vector2(5, 5) - Vector2(2, 3) = Vector2(3, 2)
        """
        return Vector2(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def magnitude(self):
        """
        Returns the magnitude of the vector.
        :return:
        """
        from math import sqrt
        return sqrt((self.x * self.x) + (self.y + self.y))

    def normalized(self):
        """
        :return: Returns the unit vector of itself.
        """
        return self / self.magnitude()

    @staticmethod
    def from_tuple(vertex):
        """
        Converts the inputted vertex from a tuple to a Vector2. If the inputted vertex
        is already a Vector2, the function will just return the inputted Vector2.
        If the inputted vertex is not a Vector2 or a tuple, the method will raise a TypeError.
        :param vertex: The tuple to be converted.
        :return: Returns a Vector2 representation of the tuple.
        """
        if isinstance(vertex, Vector2):
            return vertex
        elif isinstance(vertex, tuple):
            return Vector2(vertex[0], vertex[1])
        else:
            raise TypeError("Inputted vertex is not a tuple or Vector2! Expected: tuple | Vector2 got: " +
                            type(vertex).__name__)

    @staticmethod
    def dot_product(left, right):
        return left.x * right.x + left.y * right.y

    def get_perpendicular(self):
        """
        :return: Returns the normal vector.
        """
        return Vector2(self.y, -self.x)


class ShapeProjection:
    """
    Projection of 2D polygon into 1D.
    """
    def __init__(self, minimum, maximum):
        """
        :param minimum: The lower value of the projection on the axis.
        :param maximum: The upper value of the projection on the axis.
        """
        self.minimum = minimum
        self.maximum = maximum

    def __eq__(self, other):
        return self.minimum == other.minimum and self.maximum == other.maximum

    def __repr__(self):
        return "ShapeProjection(Minimum:" + str(self.minimum) + " Maximum: " + str(self.maximum) + ")"

    def overlaps(self, other):
        """
        Check for an overlap against another ShapeProjection.
        :param other: The other ShapeProjection instance to check for an overlap against.
        :return: A boolean representing whether there is an overlap.
        """
        return max(self.minimum, self.maximum) >= min(other.minimum, other.maximum) and \
               max(other.minimum, other.maximum) >= min(self.minimum, self.maximum)


class IntersectResult:
    """
    Return type used for resolving shape intersections.
    Carries a boolean representing whether or not an intersection is occurring,
    and the MTV - Minimum Translation Vector - for moving the shapes out of each other.
    """
    def __init__(self, intersection, mtv):
        """
        Spawns a IntersectResult instance using the provided intersection boolean
        and mtv vector.
        :param intersection:
        :param mtv:
        """
        self.intersection = intersection
        self.mtv = mtv

    def __repr__(self):
        return "IntersectResult(Intersection: " + str(self.intersection) + " MTV: " + str(self.mtv) + ")"

    def __eq__(self, other):
        return self.intersection == other.intersection and self.mtv == other.mtv
