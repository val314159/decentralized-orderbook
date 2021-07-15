from collections import defaultdict
BID, ASK = 0, 1
N_min = 2
N_max = 20
N_max = 9

import math
def pow10(n): return 10**n
def log10trunc(x): return int(math.log(x, 10))

N_min10 = pow10(N_min)
N_max10 = pow10(N_max)

def boolean(x:int):  return bool(x)
def    side(x:bool): return  int(x)
def    flip(x):      return BID if x else ASK
class TestError(SystemError): pass
class Item:
    def __repr__(self): return self.__class__.__name__ + \
        f':{self.__dict__}'
    pass


