#!/usr/bin/env python3
import os, sys, json
from pprint import pprint

from kista import *
from kista import force_load_contract_address as flca

w3 = w3_connect(0)

#set_default_address(0)

BID, ASK = 0, 1

def best_status():
    bpb, bvb = c.bestPrice(BID), c.bestVolume(BID)
    bda, bva = c.bestPrice(ASK), c.bestVolume(ASK)
    print("bid", bpb, bvb)
    print("ask", bda, bva)
    return bpb, bvb, bda, bva

if __name__ == '__main__':
    a = [WrapAccount(a) for a in range(10)]
    print(a[0])
    print(type(a[0]))
    c = WrapContract(flca("OrderBookContract",
                          a[8].address,
                          a[9].address,
                          reload = 1))
    if 0:

        best_status()

        c.createLimitOrder(ASK, 110, 1234700)

        id_ = c.getOrderId(ASK, 1234700, a[0].address)

        print(id_)

        c.cancelOrderId(ASK, 1234700, id_)

        best_status()

    if 1:

        c.createLimitOrder(ASK, 110, 1234700)

        best_status()

        c.createLimitOrder(BID,  90, 1234700)

        best_status()        
        
        c.createLimitOrder(BID,  30, 1234700)

        c.createLimitOrder(BID,  30, 1200000)

        best_status()        
        
        c.createMarketOrder(ASK, 20)

        best_status()        
        
    if 1:
        #assert(best_status() == (0,0,0,0))
        best_status()        

        c.createLimitOrder(BID, 100, 1234500)
        c.createLimitOrder(ASK, 110, 1234700)

        #$assert(best_status() == (1234500, 110, 1234700, 110))
        best_status()        

        c.createLimitOrder(BID, 120, 1234600)
        c.createLimitOrder(ASK,  80, 1234800)

        #assert(best_status() == (1234600, 110, 1234700, 110))
        best_status()        

        c.createLimitOrder(BID, 100, 1234700) # should leave 10

        best_status()

    #c.createLimitOrder(BID,  36, 
    
    #print(c.bestPrice(BID), c.bestPrice(ASK))

