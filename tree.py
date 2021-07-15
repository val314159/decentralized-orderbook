#!/usr/bin/env python3
import os, sys, json
from pprint import pprint

from kista import *
from kista import force_load_contract_address as flca

w3 = w3_connect(0)

#set_default_address(0)

if __name__ == '__main__':

    a = [WrapAccount(a) for a in range(10)]

    tree = WrapContract(flca("TestBokkyPooBahsRedBlackTreeRaw", reload = 1))

    print(tree)

    print(tree.exists(44))

    tree.insert(1)
    tree.insert(1000000000000000)

    tree.insert(11)
    tree.insert(22)
    tree.insert(44)
    
    print(tree.exists(44))

    #tree.insert(44)

    tree.insert(500)
    
    print(tree.root())
    print(tree.first())

    print(tree.last())

    print(1, tree.findLE(9999999))
    
    print(2, tree.findLE(501))
    print(2, tree.findLE(500))
    print(2, tree.findLE(499))

    print(3, tree.findLE(45))
    print(3, tree.findLE(44))
    print(3, tree.findLE(42))

    print(4, tree.findLE(23))
    print(4, tree.findLE(22))
    print(4, tree.findLE(21))

    print(5, tree.findLE(12))
    print(5, tree.findLE(11))
    print(5, tree.findLE(10))

    print(6, tree.findLE(2))
    print(6, tree.findLE(1))
    #print(0, tree.findLE(0))

    #print(6,tree.findGE(20))
    #print(tree.findGE(21))
    #print(tree.findGE(22))
    #print(tree.findGE(42))
    #print(tree.findGE(43))
    #print(tree.findGE(44))
    #print(tree.findGE(45))
    
    exit()


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

