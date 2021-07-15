from book import *
from pricelist2 import *

class prcQ(set):

    def priceExists(self, x):
        return x in self
        
    def insertPost(self, b, a, d):
        if not self.priceExists(a):
            #print(f"insert {b}->{a}->{d}")
            self.add(a)
            pass
        pass
    
    def insertSignposts(self,
                        nmin, y, prc_min,
                        nmax, z, prc_max,
                        x, n):
        #print("IS", nmin, y, prc_min,
        #      nmax, z, prc_max,
        #      x, n)
        self.insertPost(y, prc_min, z)       
        self.insertPost(prc_min, prc_max, z)
        self.insertPost(prc_min,x,prc_max)
        xmin = pow10(nmin)
        xmax = pow10(nmax)
        for s in range(nmin, n+1): self.insertPost(xmin,pow10(s),prc_min)
        for s in range(n+1,   nmax): self.insertPost(prc_max,pow10(s),xmax)
        pass
    
    def findSignposts(self, x, n, y) -> (int, int,
                                         int, int,
                                         int, int,
                                         int, int):
        # n = int(log10(x))
        # y = pow10(n)
        nmin, nmax, z = n, n+1, y*10
        # look for nmin
        while not self.priceExists(y):
            y = int(y / 10)
            nmin -= 1
            pass
        # look for nmax
        while not self.priceExists(z):
            z = int(z * 10)
            nmax += 1
            pass
        return(nmin, y, int(x/y)*y,
               nmax, z, int(x/y)*y+y,
               x, n)
    
    def find10Bounds(self, x, n) -> (int, int,
                                     int, int,
                                     int, int,
                                     int, int):
        # n = int(log10(x))
        if self.priceExists(x):
            return(n, x, x, n, x, x, x, n)
        return self.findSignposts(x, n, pow10(n))

    def findBounds2(self, x, y = None) -> (int, int):
        return self.find10Bounds(x, log10trunc(x))

    pass
    
class Test(Item):
    def __init__(self):
        self.book = Book(100)
        self.pl = PriceList2()
        #self.pq = prcQ()
    def test0(self):
        print(self.pl);       self.pl.append(707)
        print(self.pl);       self.pl.append(808)
        print(self.pl);       self.pl.prepend(606)
        print(self.pl);       self.pl.prepend(505)
        print(self.pl);       self.pl.pop()
        print(self.pl);       self.pl.pop()
        print(self.pl);       self.pl.pop()
        print(self.pl);       self.pl.pop()
        try: print(self.pl) ; self.pl.pop()   ; raise TestError
        except IndexError: pass # expecting an error
        try: print(self.pl) ; self.pl.shift() ; raise TestError
        except IndexError: pass # expecting an error
        self.pl.append(404)
        self.pl.append(505)
        #self.pl.remove(606)
        self.pl.append(707)
        self.pl.append(808)
        print(self.pl)
        self.pl.shift()
        self.pl.shift()
        self.pl.shift()
        self.pl.shift()
        try: self.pl.shift(); raise TestError
        except IndexError: pass # expecting an error
        try: self.pl.pop();   raise TestError
        except IndexError: pass # expecting an error
        pass
    def test1(self):
        print("TEST1++")
        self.pq.add(pow10(N_min))
        #self.pq.add(pow10(N_min+1))
        self.pq.add(pow10(N_max))
        r = self.pq.findBounds2(pow10(N_min))
        print("R", r)
        r = self.pq.findBounds2(pow10(N_min))
        print("R", r)
        r = self.pq.findBounds2(512)
        print("R", r)
        r = self.pq.findBounds2(51207)
        print("R", r)
        r = self.pq.findBounds2(pow10(N_max))
        print("R", r)
        print("TEST1--")
        r = self.pq.findBounds2(51234)
        print("R1", r)
        self.pq.insertSignposts(*r)
        print("PQ", sorted(list(self.pq)))
        print("....")
        r = self.pq.findBounds2(52334)
        print("R2", r)
        self.pq.insertSignposts(*r)
        print("PQ", sorted(list(self.pq)))
        print("....")
        r = self.pq.findBounds2(52336)
        print("R2", r)
        self.pq.insertSignposts(*r)
        print("PQ", sorted(list(self.pq)))
        print("....")
        r = self.pq.findBounds2(72336)
        print("R2", r)
        self.pq.insertSignposts(*r)
        print("PQ", sorted(list(self.pq)))
        print("TEST1==")
        pass
    def test8(self):
        print("TEST8==")
        pl = self.book.sides[BID].prices
        pq = self.book.sides[BID].priceQ
        print(pl)
        print(pq)
        pl.insertPrice( 12345600)
        #pl.insertPrice2(12345700, pq)
        print(pl)
        print(100, pl.findPrice2(12345600, pq))
        print(200, pl.findPrice2(12345700, pq))
        #print(pl)
        print("TEST8==")
    def test2(self):
        print("TEST2==")
        print(self.pl)
        self.pl.insertNode(Node2(pow10(N_min),
                                 12345600,
                                 pow10(N_max)))
        #print(1,self.pq2.findNode(12345600))
        #print(2,self.pq2.findNode(78912300))
        print(self.pl)
        self.pl.deleteNode(Node2(pow10(N_min),
                                 12345600,
                                 pow10(N_max)))
        print(self.pl)
        print("TEST2==")
        self.pl.insertPrice(12345600)
        print(len(self.pl))
        self.pl.insertPrice(12345700)
        print(len(self.pl))
        print("TEST2--")
        print(self.pl)
        print("TEST2==")
        print(self.pl.findPrice(12376500))
        print(self.pl.findPrice(12345700))
        print(self.pl.findPrice(22345700))
        print("TEST2==")
        pass
    def test3(self):
        #self.book.createOrder(BID, 12340000, 25, 'user1')
        #self.book.createOrder(BID, 12350000, 50, 'user2')
        #self.book.createOrder(BID, 12345800, 12, 'user2')
        #self.book.createOrder(BID, 12346100, 20, 'user3')
        #print(self.book.sides[BID].prices)
        #if 0:
        #    print(self.book.sides[BID].prices.findLE2(12343200,
        #                                              self.book.sides[BID].priceQ))
        #if 1:
        #    print(self.book.sides[BID].prices.findGE2(12345400,
        #                                              self.book.sides[BID].priceQ))
        #print(self.book.sides[BID].findLE(12345600))
        #print("----")
        #print(self.book.sides[BID].findGE(12345600))
        self.book.createOrder(BID, 12345600, 12, 'user2')
        #print("----")
        #print(self.book.sides[BID].findLE(12345600))
        #print("----")
        print(self.book.sides[BID].findLE(12365600))
        #print("----")
        #print(self.book.sides[BID].findGE(12330000))
        #print(self.book.submitLimitOrder(ASK, 12346050, 20, 'user8'))
        #print(self.book.submitLimitOrder(ASK, 12346100, 20, 'user9'))
        #print(self.book.submitLimitOrder(ASK, 12346000, 20, 'user8'))
    def test(self):
        #self.test8()
        self.test3()
        #self.test2()
        #print('***************')
        #self.test3()
        pass
    pass
#Queue()
if __name__=='__main__': Test().test()
