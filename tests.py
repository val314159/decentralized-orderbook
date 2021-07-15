#!/usr/bin/env python3
import os, sys, json
from pprint import pprint

from kista import *
from util import *

w3 = w3_connect(0)

#set_default_address(0)

if __name__ == '__main__':
    print("RUN TESTS")

    a = [WrapAccount(a) for a in range(10)]

    x  = WrapContract(
        force_load_contract_address("Tests", 25, reload = 1))

    if 0:
        print(x.add(11,22))
        print(x.test0())
        print(x.test1())
        print(x.test2())
        pass

    try:
        print("TESTS=========0")
        #x.wtest()
        x.createOrder(BID, 500, 75, a[0].address)
        print(x.volume(500))
        x.createOrder(BID, 510, 50, a[0].address)
        x.createOrder(BID, 510, 10, a[0].address)
        x.createOrder(BID, 520, 25, a[0].address)
        x.createOrder(ASK, 600, 90, a[0].address)
        x.createOrder(ASK, 610, 50, a[0].address)
        x.createOrder(ASK, 620, 10, a[0].address)
        print(x.rtest())
        print(x.volume(0))
        print(x.volume(500))
        print(x.volume(510))
        
    finally:
        print("TESTS=========9")

