#!/usr/bin/env python3
import os, sys, json
from pprint import pprint

from time import sleep

from kista import *

w3 = w3_connect(0)

#set_default_address(0)

if __name__ == '__main__':
    a = [WrapAccount(a) for a in range(10)]

    etest = WrapContract(
        force_load_contract_address("Etest", reload = 1))

    filt = etest.events.moneySent.createFilter(fromBlock=w3.eth.block_number)

    etest.add(11,22)

    e = filt.get_all_entries()
    print(len(e), e)

    if 1:
        for entry in e:
            # print("E", entry.args)
            a = entry.args
            print("E", a._from, a._to, a._amount)
            pass
        pass
    
    while 1:
        sleep(1)
        e = filt.get_new_entries()
        for entry in e:
            # print("E", entry.args)
            a = entry.args
            print("E", a._from, a._to, a._amount)
            pass
        pass
