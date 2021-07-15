from util import *

class Node2:
    def __init__(self, cbr, car, cdr):
        (self.cbr, self.car, self.cdr) = (cbr, car, cdr)
        pass
    def __repr__(self):
        return str((self.cbr, self.car, self.cdr))
    pass

class PriceList2(dict):

    def add(self, node):
        self[node.car] = node
        pass
    
    def __init__(self, nmin_=N_min, nmax_=N_max):
        self.nmin = nmin_
        self.nmax = nmax_
        self.nmin10 = pow10(nmin_)
        self.nmax10 = pow10(nmax_)
        self.add(Node2(
            pow10(nmax_), 0, pow10(nmin_)
        ))
        self.add(Node2(
            0, pow10(nmin_), pow10(nmax_)
        ))
        self.add(Node2(
            pow10(nmin_), pow10(nmax_), 0
        ))
        pass
    
    def priceExists(self, x):
        return x in self

    def insertNode(self, node):
        self[node.cbr].cdr = node.car
        self[node.cdr].cbr = node.car
        self[node.car]     = node
        pass
    
    def deleteNode(self, node):
        self[node.cbr].cdr = node.cdr
        self[node.cdr].cbr = node.cbr
        del self[node.car]
        pass

    def findPrice2(self, x, q):
        if x in self:
            return x, x
        print("FIND PRC2", x)
        bot_node = None
        top_node = None
        for n in range(N_min+1, N_max+1):
            m = pow10(n)
            bot_price = x//m*m
            if bot_price == 0:
                bot_price = pow10(N_min)
                pass
            top_price = x//m*m+m
            bot_range = self.get(bot_price)
            top_range = self.get(top_price)
            if not bot_node:
                print("  b", bot_price, q.keys())
                if bot_price in q:
                    print("  b=")
                    bot_node = bot_range
            if not top_node:
                print("  t", top_price, q.keys())
                if top_price in q:
                    print("  t=")
                    top_node = top_range
            
            print("N", n, m)
            print("    ", bot_price, top_price)
            print("         ", bot_range, top_range)
            print("         ", bot_node, top_node)

            if bot_node and top_node:
                print("got ends")
                print("         ", bot_node, top_node)
                break
            
            pass

        print("OK THEN", bot_node, top_node)
        
        # need to search into the 10 part
        #print(" ****************1")
        #print(bot_node.car, top_node.car, m, bot_node.car+(m//10))
        m = pow10(n-1)
        cur_price = x//m*m
        #print("CP", cur_price, m,
        #bot_node.car, top_node.car)

        if bot_node:
            # count down
            for z in range(cur_price-m, bot_node.car, -m):
                y = self.get(z)
                print("DN", z, y)
                if y:
                    if y in q:
                        bot_node = y
                        break
              
        if top_node:
            # count up
            for z in range(cur_price+m, top_node.car, m):
                y = self.get(z)
                print("UP", z, y)
                if y:
                    if y in q:
                        top_node = y
                        break
        
        #bot_price = x//m*m
        #print(" ****************2")
        if bot_node:
            bot = bot_node.car
        else:
            bot = 0
            pass
        if top_node:
            top = top_node.car
        else:
            top = 0
            pass
        return bot, top

    def findPrice(self, x):
        if x in self:
            return x, x
        #print("FIND PRC", x)
        bot_node = None
        top_node = None
        for n in range(N_min+1, N_max+1):
            m = pow10(n)
            bot_price = x//m*m
            if bot_price == 0:
                bot_price = pow10(N_min)
                pass
            top_price = x//m*m+m
            bot_range = self.get(bot_price)
            top_range = self.get(top_price)
            if not bot_node:
                bot_node = bot_range
            if not top_node:
                top_node = top_range
            
            #print("N", n, m)
            #print("    ", bot_price, top_price)
            #print("         ", bot_range, top_range)
            #print("         ", bot_node, top_node)

            if bot_node and top_node:
                #print("got ends")
                #print("         ", bot_node, top_node)
                break
            
            pass

        # need to search into the 10 part
        #print(" ****************1")
        #print(bot_node.car, top_node.car, m, bot_node.car+(m//10))
        m = pow10(n-1)
        cur_price = x//m*m
        #print("CP", cur_price, m,
        #bot_node.car, top_node.car)
              
        # count down
        for z in range(cur_price-m, bot_node.car, -m):
            y = self.get(z)
            #print("DN", z, y)
            if y:
                bot_node = y
                break
              
        # count up
        for z in range(cur_price+m, top_node.car, m):
            y = self.get(z)
            #print("UP", z, y)
            if y:
                top_node = y
                break
        
        #bot_price = x//m*m
        #print(" ****************2")
        return bot_node.car, top_node.car

    def insertPrice(self, x):
        if x in self:
            return
            return self[x]
        #print("INSERT PRC", x)

        bot_node_car, top_node_car = self.findPrice(x)
        bot_node, top_node = self[bot_node_car], self[top_node_car]

        for n in range(N_max, N_min, -1):
            m = pow10(n)
            bot_price = x//m*m
            if bot_price == 0:
                bot_price = pow10(N_min)
                pass
            top_price = x//m*m+m
            bot_range = self.get(bot_price)
            top_range = self.get(top_price)
            
            #print("N", n, m)
            #print("    ", bot_price, top_price)
            #print("         ", bot_range, top_range)
            #print("         ", bot_node, top_node)

            if bot_price not in self:
                #print("insert bot price", bot_price)
                node = Node2(bot_node.car, bot_price, top_node.car)
                #print(node)
                self.insertNode(node)
                bot_node = node
                pass

            if top_price not in self:
                #print("insert top price", top_price)
                node = Node2(bot_node.car, top_price, top_node.car)
                #print(node)
                self.insertNode(node)
                top_node = node
                pass

            pass

        node = Node2(bot_node.car, x, top_node.car)
        self.insertNode(node)
        
    def findClosest(self, x, side) -> int:
        if side == BID:
            return self.findGE(x)
        else:
            return self.findLE(x)
        pass

    def findGE(self, x) -> int:
        print("find GE")
        ret = self.findPrice2(x)[1]
        if ret == self.nmax10:
            return 0
        return ret
    
    def findLE(self, x) -> int:
        print("find LE")
        ret = self.findPrice2(x)[0]
        if ret == self.nmin10:
            return 0
        return ret

    def findGE2(self, x, q) -> int:
        print("find GE")
        ret = self.findPrice2(x, q)[1]
        if ret == self.nmax10:
            return 0
        return ret
    
    def findLE2(self, x, q) -> int:
        print("find LE")
        ret = self.findPrice2(x, q)[0]
        if ret == self.nmin10:
            return 0
        return ret
