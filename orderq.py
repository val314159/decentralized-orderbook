from util import *
class Order(Item):
    def __init__(self, side_, price_, size_, maker_):
        self.side, self.price, self.size, self.maker = \
            (side_,     price_,     size_,     maker_)
        self.filled, self.cancelled = False, False
        self.sibling,self.position  = 0, 0
        pass
    def getId(self): return id(self)
    pass
mkOrder = Order
class Sparce(Item):
    def init(self):
        self.volume = 0
        self.q = defaultdict(Order)
        self.i = defaultdict(int)
        pass
    def __init__(self):
        self.init()
        pass
    def   by(self,    id_:int): return self.at(self.i[id_])
    def   at(self,   pos_:int): return self.q[pos_]
    def  dlt(self, order_:Order):
        del self.q[self.i.pop(order.getId())]
        self.volume -= order.size
        pass
    def unsafeAddAt(self,  pos_:int, order_:Order):
        self.volume += order_.size
        self.q[pos_] = order_
        self.i[order_.getId()] = pos_
    def addAt(self,  pos_:int, order_:Order):
        oldOrder = self.q.get(pos_)
        if oldOrder: self.volume -= oldOrder.size
        self.unsafeAddAt(pos_, order_)
    pass
class Queue(Sparce):
    def __init__(self):
        self.init()
        self.first, self.last = 1, 0
        pass
    def isEmpty(self) -> bool:
        return self.first > self.last
    def whead(self) -> Order:
        return self.at(self.first)
    def wtail(self) -> Order:
        return self.at(self.last)
    def push(self, order_:Order) -> Order:
        self.last += 1
        self.unsafeAddAt(self.last, order_)
        pass
    def shift(self):
        self.dlt(self.whead())
        self.first += 1
        pass
    pass
