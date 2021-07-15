#!/usr/bin/env python3
import os, sys, json
from pprint import pprint

from kista import *

w3 = w3_connect(0)

#set_default_address(0)

if __name__ == '__main__':

    a = [WrapAccount(a) for a in range(10)]

    btc  = WrapContract(
        force_load_contract_address("Coin", "Val's Wrapped BTC",
                                    "VBTC", reload = 1))
    usd  = WrapContract(
        force_load_contract_address("Coin", "Val's Wrapped USD",
                                    "VUSD", reload = 1))
    bank = WrapContract(
        force_load_contract_address("Bank"))

    def fline(prefix, address):
        #fmt = "{}| {:10.4f} ETH | {:10.4f} BTC | {:10.4f} USD |"
        fmt = "{}| {:22d} ETH | {:22d} BTC | {:22d} USD |"
        return fmt.format(prefix,
                          bank.get_balance(address),
                          btc.balanceOf(address),
                          usd.balanceOf(address))

    def status():
        print(".....")
        print(fline('bt', btc.address))
        print(fline('ut', usd.address))
        print(fline('bk',bank.address))
        print(fline('a0', a[0].address))
        print(fline('a1', a[1].address))
        print(fline('a2', a[2].address))
        pass

    status()

    a[1].transfer(a[2].address, 10)   

    status()
    
    btc.transfer(a[2].address, w3.toWei(   10, 'ether'), _from=a[0].address)
    usd.transfer(a[2].address, w3.toWei( 50, 'ether'))

    #btc.transfer(a[1].address, w3.toWei(   25, 'ether'), _from=a[0].address)
    #usd.transfer(a[1].address, w3.toWei(65000, 'ether'))

    bank.depositETH(value=999999)

    status()

    btc.approve(bank.address, 800)
    btc.approve(bank.address, 100, _from = a[2].address)

    bank.transferFrom(a[0].address, btc.address, 80)

    status()
    
    bank.transferFrom(a[2].address, btc.address, 16)

    status()

    bank.transferInto(a[2].address, btc.address, 2)

    status()
    
    bank.withdrawETH2()

    status()
    pass

