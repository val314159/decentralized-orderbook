#!/usr/bin/env python3
import os, sys, json
from web3.auto import w3, Web3

from kista import *

w3 = w3_connect()

w3.eth.default_account = w3.eth.accounts[0]

a = [WrapAccount(a) for a in range(10)]

t = WrapContract(force_load_contract_address("T", reload = 1))

#print(a)
#print(t)

if 0:
    lca = "0x356112e1e417d6DcEB3981495EB5FA451294954E"
    account_3 = Web3.toChecksumAddress(lca)

    a4 = "0xCc021c055E712AFDBCBaEF956AeA9262DDC309B3"

    lower_case_address = "a990077c3205cbdf861e17fa532eeb069ce9ff96"
    account_2 = Web3.toChecksumAddress(lower_case_address)

    print(t.ecrecoverVerify2(account_2))

    print(t.ecrecoverVerify2(account_3))

    print(t.ecrecoverVerify2(a4))
    pass


    
exit()

#lower_case_address = "a990077c3205cbdf861e17fa532eeb069ce9ff96"
#account_2 = Web3.toChecksumAddress(lower_case_address)

account_1    = open("0.pub").read().strip()
private_key1 = open("0.prv").read().strip()

print('balance1:', w3.eth.get_balance(account_1))
print('balance2:', w3.eth.get_balance(account_2))

signed_tx = w3.eth.account.sign_transaction({
    'nonce': w3.eth.getTransactionCount(account_1),
    'to': account_2,
    'value': w3.toWei(1, 'ether'),
    'gas': 2000000,
    'gasPrice': w3.toWei('50', 'gwei')
}, private_key1)

tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(tx_hash.hex())
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt['transactionHash'].hex())

print('balance1:', w3.eth.get_balance(account_1))
print('balance2:', w3.eth.get_balance(account_2))

tx_hash = w3.eth.send_raw_transaction(open('erc1820.bin').read())
print(tx_hash.hex())
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt['transactionHash'].hex())

print('balance1:', w3.eth.get_balance(account_1))
print('balance2:', w3.eth.get_balance(account_2))
