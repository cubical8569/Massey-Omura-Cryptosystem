from pyfinite import ffield


class Point:
    # pair (a, b) where a, b are field elements
    def __init__(self, curve, neutral, x=None, y=None):
        self.curve = curve
        self.neutral = neutral

        if self.neutral:
            self.x = None
            self.y = None
        else:
            if isinstance(x, ffield.FElement):
                self.x = x
            else:
                self.x = ffield.FElement(self.curve.field, x)

            if isinstance(y, ffield.FElement):
                self.y = y
            else:
                self.y = ffield.FElement(self.curve.field, y)

    def __eq__(self, other):
        return (self.curve, self.neutral, self.x, self.y) \
               == (other.curve, other.neutral, other.x, other.y)

    def __hash__(self):
        return hash((self.curve, self.neutral, self.x, self.y))

    def __neg__(self):
        if self.neutral:
            return Point(curve=self.curve, neutral=True)

        x1 = self.x
        y1 = self.x

        new_x = x1
        new_y = x1 + y1

        return Point(curve=self.curve, neutral=False, x=new_x, y=new_y)

    def _double(self):
        if self == -self or self.neutral:
            return Point(self.curve, True)

        x1 = self.x
        y1 = self.y
        a = self.curve.a

        l = x1 + (y1 / x1)
        new_x = l ** 2 + l + a
        new_y = x1 ** 2 + (l * new_x) + new_x

        return Point(self.curve, neutral=False, x=new_x, y=new_y)

    def __add__(self, other):
        if self == other:
            return self._double()

        if other.neutral:
            return self

        if self.neutral:
            return other

        if self == -other:
            return Point(self.curve, True)

        x1 = self.x
        y1 = self.y

        x2 = other.x
        y2 = other.y

        a = self.curve.a

        l = (y2 + y1) / (x2 + x1)
        new_x = (l * l) + l + x1 + x2 + a
        new_y = (l * (x1 + new_x)) + new_x + y1

        return Point(self.curve, neutral=False, x=new_x, y=new_y)

    def __mul__(self, times):
        assert isinstance(times, int)
        assert times >= 0

        times %= self.curve.curve_points

        result = Point(self.curve, True)
        tmp = self

        while times != 0:
            if times % 2 == 1:
                result += tmp

            tmp += tmp
            times //= 2

        return result

    def __str__(self):
        return "(" + str(self.x) + ":" + str(self.y) + ")"

class ECurve:
    # Elliptic curve y ** 2 + x * y = x ** 3 + a * x ** 2 + b
    # a, b are from field F

    def __init__(self):
        self.field = ffield.FField(163)
        self.a = ffield.FElement(self.field, 1)
        self.b = ffield.FElement(
            self.field,
            0x000000020A601907B8C953CA1481EB10512F78744A3205FD
        )

        self.n = 0x000000040000000000000000000292FE77E70C12A4234C33
        self.h = 2

        self.curve_points = self.n * self.h

        self.g = Point(
            self,
            False,
            0x3f0eba16286a2d57ea0991168d4994637e8343e36,
            0x0d51fbc6c71a0094fa2cdd545b11c5c0c797324f1
        )

    def calculate_left(self, point):
        return point.y ** 2 + point.x * point.y

    def calculate_right(self, point):
        return point.x ** 3 + self.a * point.x ** 2 + self.b

    def is_ok(self, point):
        return self.calculate_left(point) == self.calculate_right(point)