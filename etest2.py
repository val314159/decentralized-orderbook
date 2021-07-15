#!/usr/bin/env python3
import os, sys, json
from pprint import pprint

from time import sleep

from kista import *

w3 = w3_connect(0)

set_default_address(0)

if __name__ == '__main__':

    a = [WrapAccount(a) for a in range(10)]

    etest = WrapContract(
        force_load_contract_address("Etest"))

    etest.add(9000, 550)

    sleep(0.5)
