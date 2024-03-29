"""
A module for determining whether an
intersection between two convex shapes are occurring.
"""

class IntersectTester:
    """
    Used to test for intersections between shapes.
    """

    def __init__(self, pol1, pol2):
        """
        Spawns an instance of an InterestTester provided the actual shapes to test for.
        Ensure that both the inputted polygons are not the same.
        Args:
            pol1: 1 of 2 polygons that a collision will be tested for.
            pol2: 1 of 2 polygons that a collision will be tested for.
        """
        self.pol1 = pol1
        self.pol2 = pol2

    def test_minor(self) -> bool:
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
        :return: An IntersectResult containing information on the intersection.
        """

        # Control overlap to be changed. Set to high value to find the lowest one.
        overlap = 999999
        # A default axis
        n = Vector2(0, 0)

        # Looping through axes's...
        for normal in IntersectTester._get_normals_from(self.pol1) + IntersectTester._get_normals_from(self.pol2):
            if normal.isZero():
                continue

            p1 = IntersectTester.projection_of_onto(self.pol1, normal)
            p2 = IntersectTester.projection_of_onto(self.pol2, normal)

            # Checking for axes overlap...
            if p1.overlaps(p2):
                o = p1.get_overlap(p2)

                # Checking for containment...
                if p1.contains(p2) or p2.contains(p1):
                    possibleMin = abs(p1.minimum - p2.minimum)
                    possibleMax = abs(p1.maximum - p2.maximum)

                    if possibleMin < possibleMax:
                        o += possibleMin
                    else:
                        o += possibleMax
                        
                if o < overlap:
                    overlap = o
                    n = normal

            else:
                # No Intersection. Quit algorithm right away.
                return IntersectResult(False, Vector2(0, 0))

        shape1Bounds = BoundingBox.generate_bounds_from(self.pol1)
        shape2Bounds = BoundingBox.generate_bounds_from(self.pol2)

        dot = Vector2.dot(shape2Bounds.get_center() - shape1Bounds.get_center(), n)

        if dot < 0:
            n = -n

        # If execution gets to this point, the algorithm did not return and thus there is an intersection
        # between the two shapes.
        return IntersectResult(True, n * overlap)

    def test(self):
        """
        Performs a full test - that is the preliminary bounding box check for performance and the SAT algorithm.
        :return: IntersectResult containing information representing whether there is an intersection
        between the two polygons.
        """
        bounds_is_intersecting = self.test_minor()
        if bounds_is_intersecting:
            return self.test_major()
        return IntersectResult(False, Vector2(0, 0))

    @staticmethod
    def _get_normals_from(polygon):
        """
        :param polygon: The polygon to get edge normals from.
        :return: Retrieves the edge normals of the provided convex polygon.
        """
        normals = []
        for i in range(len(polygon)):
            vertexVector1 = Vector2.from_type(polygon[i])
            if i + 1 >= len(polygon):
                return normals
            else:
                vertexVector2 = Vector2.from_type(polygon[i + 1])
            edge = vertexVector1 - vertexVector2
            normals.append(edge.get_perpendicular().normalized())
        return normals

    @staticmethod
    def projection_of_onto(pol1, axis):
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
            vecVertex = Vector2.from_type(vertex)
            p = Vector2.dot(axis, vecVertex)
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
        """
        :rtype: str
        """
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
        :rtype:
        """
        # Type checking to throw an error if the user inputted something other than a BoundingBox
        # otherwise Python will throw it's own vague error.
        if not isinstance(other, BoundingBox):
            raise TypeError("Incorrect type for parameter 'other'. Expected a BoundingBox not: " + type(other).__name__)

        return self.x < other.x + other.width \
               and self.x + self.width > other.x \
               and self.y < other.y + other.height \
               and self.y + self.height > other.y

    def corners(self):
        return [Vector2(self.x, self.y), Vector2(self.x + self.width, self.y),
                Vector2(self.x + self.width, self.y + self.height), Vector2(self.x, self.y + self.height),
                Vector2(self.x, self.y)]

    def get_center(self):
        return Vector2(self.x + (self.width / 2), self.y + (self.height / 2))

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
            vector_vertex = Vector2.from_type(vertex)
            if max_vec.x < vector_vertex.x:
                max_vec.x = vector_vertex.x

            if min_vec.x >= vector_vertex.x:
                min_vec.x = vector_vertex.x

            if max_vec.y < vector_vertex.y:
                max_vec.y = vector_vertex.y

            if min_vec.y > vector_vertex.y:
                min_vec.y = vector_vertex.y

        return BoundingBox(min_vec.x, min_vec.y, max_vec.x - min_vec.x, max_vec.y - min_vec.y)


class Vector2:
    def __init__(self, x, y):
        """
        Initializes a new Vector2
        :param x: The x coordinate
        :param y: The y coordinate
        """
        self.x = x
        self.y = y

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __repr__(self):
        return "Vector2(" + str(self.x) + ", " + str(self.y) + ")"

    # Operator overloads...

    def __truediv__(self, scalar):
        """
        :return: Division between Vector2 and scalar. Vector2(1, 1) / 2.0 = Vector2(0.5, 0.5)
        """
        return Vector2(self.x / scalar, self.y / scalar)

    def __mul__(self, scalar):
        """
        :return: Vector2 multiplied by scalar. Vector2(1, 1) * 2 = Vector2(2, 2)
        """
        return Vector2(self.x * scalar, self.y * scalar)

    def __add__(self, other):
        """
        :return: Vector2(2, 2) + Vector2(2, 2) = Vector2(4, 4)
        """
        return Vector2(self.x + other.x, self.y + other.y)

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
        return sqrt((self.x * self.x) + (self.y * self.y))

    def normalized(self):
        """
        :return: Returns the unit vector of itself.
        """
        return self / self.magnitude()

    def distance_from(self, other):
        return (self - other).magnitude()

    @classmethod
    def from_type(cls, vertex):
        """
        Converts the inputted vertex from a tuple to a Vector2. If the inputted vertex
        is already a Vector2, the function will just return the inputted Vector2.
        If the inputted vertex is not a Vector2 or a tuple, the method will raise a TypeError.
        :param vertex: The tuple to be converted.
        :return: Returns a Vector2 representation of the tuple.
        """
        import sys
        if 'graphics' in sys.modules:
            from graphics import Point
            if isinstance(vertex, Point):
                return cls(vertex.x, vertex.y)
        if isinstance(vertex, Vector2):
            return vertex
        elif isinstance(vertex, tuple):
            return cls(vertex[0], vertex[1])
        else:
            raise TypeError("Inputted vertex is not a tuple, Vector2 or Point! Expected: tuple || Vector2 || Point got: " +
                            type(vertex).__name__)

    def dot(self, right):
        return self.x * right.x + self.y * right.y

    def get_perpendicular(self):
        """
        :return: Returns the normal vector.
        """
        return Vector2(self.y, -self.x)

    def isZero(self):
        return self.x == 0 and self.y == 0


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

    def get_overlap(self, other):
        """
        :return: Returns the overlap magnitude of 2 projections on the same axis.
        """
        if (self.overlaps(other)):
            return min(self.maximum, other.maximum) - max(self.minimum, other.minimum)
        else:
            return 0

    def contains(self, other):
        return other.minimum > self.minimum and other.maximum < self.maximum


class IntersectResult:
    """
    Return type used for resolving shape intersections.
    Carries a boolean representing whether or not an intersection is occurring,
    and the MTV - Minimum Translation Vector - for moving the shapes out of each other.
    """

    def __init__(self, intersection: bool, mtv: Vector2):
        """
        Spawns a IntersectResult instance using the provided intersection boolean
        and mtv vector.
        :param intersection:
        :param mtv:
        """
        self.intersecting = intersection
        self.mtv = mtv

    def __repr__(self):
        return "IntersectResult(Intersection: " + str(self.intersecting) + " MTV: " + str(self.mtv) + ")"

    def __eq__(self, other):
        return self.intersecting == other.intersection and self.mtv == other.mtv
