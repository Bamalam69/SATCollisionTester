class BoundingBox:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def intersects_with(self, other):
        if not isinstance(other, BoundingBox):
            raise TypeError("Incorrect type for parameter 'other'. Expected a BoundingBox not:" + type(other).__name__)

        return self.x < other.x + other.width \
            and self.x + self.width > other.x \
            and self.y < other.y + other.height \
            and self.y + self.height > other.y


class SATResult:
    def __init__(self, intersection, mtv):
        self.intersection = intersection
        self.mtv = mtv


class SATTester:
    def __init__(self, pol1, pol2):
        pass

    def test_aabb(self):
        return False

    def test_sat(self):
        return SATResult(False, None)

    def test_full(self):
        return SATResult(False, None)


def generate_bounds(pol1):
    return BoundingBox(0, 0, 10, 10)
