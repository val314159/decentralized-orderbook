from book import *

import math
def pow10(n): return 10**n
def log10trunc(x): return int(math.log(x, 10))
N_min = 2
N_max = 20
N_max = 9

class prcQ(set):

    def priceExists(self, x):
        return x in self
        
    def insertPost(self, b, a, d):
        if not self.priceExists(a):
            print(f"insert {b}->{a}->{d}")
            self.add(a)
            pass
        pass
    
    def insertSignposts(self,
                        nmin, y, prc_min,
                        nmax, z, prc_max,
                        x, n):
        print("IS",
                   nmin, y, prc_min,
                        nmax, z, prc_max,
                        x, n)
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
        self.pl = PriceList()
        self.pq = prcQ()
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
    def test(self):
        self.test1()
        self.test0()
        pass
    pass
if __name__=='__main__': Test().test()
