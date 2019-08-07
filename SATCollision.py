"""
This module is to be used for determining whether or
not an intersection between
two convex shapes are occuring......
"""


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
        pass

    def test_full(self):
        """
        Performs a full test - that is the preliminary bounding box check for performance and the SAT algorithm - on the
        given polygons inputted when this instance was spawned.
        :return: IntersectResult containing information representing whether there is an intersection
        between the two polygons.
        :return:
        """
        pass


class BoundingBox:
    """
    Represents an axis-aligned BoundingBox.
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

    def intersects_with(self, other):
        """
        Checks for an intersection between itself and the other provided bounding box.
        :param other: The other bounding box to if intersecting. Will raise a
        TypeError if 'other' is not a BoundingBox.
        :return: A boolean - true for an intersection.
        """
        # Type checking to throw an error if the user inputted something other than a BoundingBox
        # otherwise Python will throw it's own vague error when the AABB intersection check is performed.
        if not isinstance(other, BoundingBox):
            raise TypeError("Incorrect type for parameter 'other'. Expected a BoundingBox not:" + type(other).__name__)

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
        min_vec = Vector2(9999999, 999999)
        max_vec = Vector2(-9999999, -99999999)
        for vertex in pol1:
            if vertex.x > max_vec.x:
                max_vec.x = vertex.x
            if vertex.x <= min_vec.x:
                min_vec.x = vertex.x

            if vertex.y > max_vec.y:
                max_vec.y = vertex.y
            if vertex.y <= min_vec.y:
                min_vec.y = vertex.y

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

    def magnitude(self):
        """
        Returns the magnitude of the vector.
        :return:
        """
        from math import sqrt
        return sqrt((self.x * self.x) + (self.y + self.y))

    def normalized(self):
        """
        Returns the unit vector of itself.
        :return:
        """
        return self / self.magnitude()

    # Operator overloads...
    # Division
    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)

    # Multiplication
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    # Addition
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    # Subtraction
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)


class IntersectResult:
    """
    Return type used for resolving shape intersections.
    Carries a boolean representing whether or not an intersection is occurring,
    and the MTV - Minimum Translation Vector - for moving the shapes out of each other.
    """
    def __init__(self, intersection, mtv):
        """"
        Spawns a IntersectResult instance using the provided intersection boolean
        and mtv vector.
        :param intersection:
        :param mtv:
        """
        self.intersection = intersection
        self.mtv = mtv
