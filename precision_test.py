import math
import random
import sys
from decimal import Decimal
# TODO Coś nie tak z dokładnością

a = Decimal(-5)
# a += Decimal(sys.float_info.epsilon)
b = Decimal(-5)

step = Decimal(0.2)

minimum = math.ceil(a / step) * step
maximum = math.floor(b / step) * step

random_number = minimum + (maximum - minimum) * Decimal(random.random())
divided = int(random_number / step)
result = divided * step

print(minimum)
print(maximum)

print(result)
