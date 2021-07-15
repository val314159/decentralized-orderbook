from util import *
from orderq import *
#from pricelist import *
from pricelist2 import *
class Side(Item):
    def __init__(self, asc_):
        self.ascending = asc_
        self.priceQ = defaultdict(Queue)
        self.prices = PriceList2()
        pass

    def findLE(self, x):
        if x in self.priceQ:
            return x
            return self.priceQ[x]

        for n in range(N_min+1, N_max+1):
            #print("X", n)
            p = pow10(n-1)
            m = pow10(n)
            x_lo = x//m*m
            x_hi = x//m*m+m
            z = (x // p * p) % m
            print("N", n, m, x_lo, z, p)
            for r in range(x_lo+z, x_lo, -p):
                print("..R", r, self.prices.get(r), self.prices.get(r+p))
                if self.prices.get(r):
                    z = self.prices.get(r).cbr
                    #print("XXXX", z, self.priceQ[z])
                    if self.priceQ.get(z):
                        #print("ZZZZ", z, self.priceQ[z])
                        return z
                    pass
                pass
            #for r in range(x_lo+z, x_lo, -p):
            #    print("..r", r, self.prices.get(r))
            pass
        node = self.prices.get(N_min10)
        if node and self.priceQ.get(node.cdr):
            if node.cdr < x:
                return node.cdr
        return 0
    
    def findGE(self, x):
        if x in self.priceQ:
            return x
            return self.priceQ[x]

        node = self.prices.get(x)
        if node and self.priceQ.get(node.cdr):
            return node.cdr
        
        for n in range(N_min+1, N_max+1):
            #print("X", n)
            p = pow10(n-1)
            m = pow10(n)
            x_lo = x//m*m
            z = (x // p * p) % m
            #print("N", n, m, z, 0, x_lo+z)
            for r in range(x_lo+z+p, x_lo+m, p):
                #print("..R", r, self.prices.get(r))
                if self.prices.get(r):
                    z = self.prices.get(r).cbr
                    #print("XXXX", z, self.priceQ[z])
                    if self.priceQ.get(z):
                        #print("ZZZZ", z, self.priceQ[z])
                        return z
                    pass
                pass
            pass
        node = self.prices.get(N_max10)
        if node and self.priceQ.get(node.cdr):
            if node.cdr > x:
                return node.cdr
        return 0
    
    pass
class Book(Item):
    def __init__(self, id_ = 0):
        self.id, self.sides = id_, [ Side(BID), Side(ASK) ]
        pass
    def dleteOrder(self, order_):
        return(self.sides[side_].priceQ[price_].dlt(order_))
    def orderAt(self, side_, price_, pos_) -> Order:
        return self.sides[side_].priceQ[price_].at(pos_)
    def orderBy(self, side_, price_, id_) -> Order:
        return self.sides[side_].priceQ[price_].by(id_)
    def createOrder(self, side_, price_, size_, owner_):
        order = mkOrder(side_, price_, size_, owner_)
        self.sides[side_].priceQ[price_].push(order)
        self.sides[side_].prices.insertPrice(price_)
        print(f'Create {order}')
        return
    def submitLimitOrder(self, side_, price_, size_, owner_):

        print("SUBMIT LIMIT ORDER", price_)

        sid = self.sides[flip(side_)]

        #print(sid)
        
        print(sid.prices.findPrice2(price_, sid.priceQ))
        
        #print(sid.prices.findClosest(price_, side_))       
        #order = mkOrder(side_, price_, size_, owner_)
        #order = rawCreateOrder(side_, price_, size_, owner_)

        return
    def cancelOrder(self, order_):
        # rip it out of the book
        order_.cancelled = True
        print(f'Cancel {order}')
        self.dleteOrder(order_)
        return
    def fillOrder(self, order_, dlt):
        order_.filled = True
        print(f'Filled {order}')
        if dlt: self.dleteOrder(order_)
        pass
    def matchOrders(self, thisOrder_, thatOrder_) -> int:
        # maker and taker
        thisOrder_.sibling   = thatOrder_.getId()
        thatOrder_.sibling   = thisOrder_.getId()
        thisOrder_.fillPrice = thisOrder_.price
        thatOrder_.fillPrice = thisOrder_.price
        size_ = min(thisOrder.size, thatOrder.size)
        print(f'Matched {thisOrder_} {thatOrder_} {size_}')
        thisOrder.size -= size_
        thatOrder.size -= size_
        if thisOrder.size == 0: self.fillOrder(thisOrder,  True)
        if thatOrder.size == 0: self.fillOrder(thatOrder, False)
        pass
    def flipSide(self, side_) -> Side: return self.sides[flip(side_)]
    def thisSide(self, side_) -> Side: return self.sides[     side_ ]
    def attemptMatch(self, newOrder) -> bool:

        # newOrder isn't in book yet.            
        oside = self.flipSide(newOrder.side)

        try:                
            # find closest price
            oprice = oside.prices.findClosest(newOrder.price)
        except IndexError:

            # no qualifying orders, put this in the book
            self.thisSide(newOrder.side).addToBook(newOrder)

            # and tell everyone match failed
            return False

        # find the next order,
        oldOrder = oside.priceQ.at(price).whead()

        # match it,
        self.matchOrders(oldOrder, newOrder)

        # tell everyone match succeeded
        return True
    def attemptMatches(self, newOrder, maxFills) -> bool:
        for n in range(maxFills):
            if newOrder.size <= 0:
                # we're done! entirely filled!
                return True
            if not self.attemptMatch(newOrder):
                # no match, we're done!
                # attemptMatch already put this in book
                # but since we put part of it in the book,
                # we haven't really finished the fill yet
                return False
            pass
        if newOrder.size <= 0:
            # we're done! entirely filled!
            return True
        # since we hit maxfills,
        # we haven't really finished the fill yet
        return False
    pass
