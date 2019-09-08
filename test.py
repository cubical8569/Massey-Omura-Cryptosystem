from pyfinite.ffield import FField, FElement
from elliptic_curve import Point, ECurve
from cryptosystem import Cryptosystem
from user import User
import random

system = Cryptosystem()

alice = User(cryptosystem=system, id='Alice')
bob = User(cryptosystem=system, id='Bob')

alice.send_text(receiver_name='Bob', message_text='Hello!')

# curve = ECurve()
#
# point = curve.g
#
# point1 = point
# point2 = point * (curve.n + 1)
#
# assert point1.x == point2.x
# assert point1.y == point2.y
# assert point1.neutral == point2.neutral
# assert point1.curve == point2.curve
#
# assert point == point * (curve.n + 1)

# for i in range(100):
#     print(i)
#     assert curve.is_ok(point * random.randrange(curve.n, curve.curve_points))