#!/usr/bin/env python3
"""
# what's the plan the avoid front-running?

===
# Stage 0: Market opens



"""
import os, sys, json
from pprint import pprint

from kista import *

import web3

w3 = w3_connect(0)

set_default_address(0)

if __name__ == '__main__':

    a = [WrapAccount(a) for a in range(10)]

    ed = WrapContract(force_load_contract_address("ED", reload = 1))

    try:
        print(0, str(ed.hash()))
        print(0, ed.getData2())
    except web3.exceptions.BadFunctionCallOutput:
        raise SystemError

    ed.test0()

    try:
        print(1, str(ed.hash()))
        print(1, ed.getData2())
        raise SystemError
    except web3.exceptions.BadFunctionCallOutput:
        pass

    ed.test1()

    try:
        print(2, str(ed.hash()))
        print(2, ed.getData2())
    except web3.exceptions.BadFunctionCallOutput:
        raise SystemError
    
    ed.test2()

    try:
        print(3, str(ed.hash()))
        print(3, ed.getData2())
        raise SystemError
    except web3.exceptions.BadFunctionCallOutput:
        pass

    print(ed.test3())
