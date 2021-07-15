from util import *
class Node(Item):
    def __init__(self, cur_:int=0, nxt_:int=0, prv_:int=0):
        self.cur, self.nxt, self.prv = cur_, nxt_, prv_
        pass
    def __repr__(self):
        return f'({self.nxt}^{self.prv})'
    pass
class PriceList(defaultdict):
    def __repr__(self): return self.__class__.__name__ + \
        f':{self.__dict__}:{dict(self)}'
    def __init__(self):
        defaultdict.__init__(self, Node)
        #self.ascending = asc_
        self[0] = Node()
        pass
    def insert(self, x, n, p):
        self[x].cur = x
        self[x].nxt = n
        self[x].prv = p
        self[n].prv = x
        self[p].nxt = x
        pass
    def prepend(self, x):
        n = self[0].nxt
        return self.insert(x, n, 0)
    def append(self, x):
        p = self[0].prv
        return self.insert(x, 0, p)
    def remove(self, x):
        n = self[x].nxt
        p = self[x].prv
        del self[x]
        self[n].prv = p
        self[p].nxt = n
        pass
    def shift(self):
        n = self[0].nxt
        if n == 0:
            raise IndexError('shift from empty PriceList')
        return self.remove(n)
    def pop(self):
        p = self[0].prv
        if p == 0:
            raise IndexError('pop from empty PriceList')
        return self.remove(p)
    def findClosest(self, x, side) -> int:
        if side == BID:
            return self.findGE(x)
        else:
            return self.findLE(x)
        pass
    def findGE(self, x) -> int:
        if x in self:
            return x
        n = self[0].nxt
        p = self[0].prv
        if x > p:
            raise IndexError('above range')
        if x < n:
            # below range, it's the bottom
            return n
        while x < p:
            if x in self:
                return x
            x += 1
            pass
        raise SystemError('shouldn\'t ever get here')
    def findLE(self, x) -> int:
        if x in self:
            return x
        p = self[0].prv
        n = self[0].nxt
        if x > p:
            # above range, it's the top
            return p
        if x < n:
            raise IndexError('below range')
        while x > n:
            if x in self:
                return x
            x -= 1
            pass
        raise SystemError('shouldn\'t ever get here')
    pass
