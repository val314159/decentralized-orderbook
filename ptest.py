#!/usr/bin/env python3
import os, sys, json
from pprint import pprint

from time import sleep

from kista import *

#w3 = w3_connect(0)

from web3.auto.infura import w3

#w3 = w3_connect(0)

#"https://mainnet.infura.io/v3/3471ef2a9eda43ee9b06159a1cb470ea"

#set_default_address(0)

if __name__ == '__main__':

    os.environ['WEB3_INFURA_PROJECT_ID'] = '3471ef2a9eda43ee9b06159a1cb470ea'
    os.environ['WEB3_INFURA_SECRET'] = '222660a87589473ba9fd9fb27890f6cf'

    print(w3)
    print(w3.isConnected())
    
    # The ethPM module is still experimental and subject to change,
    # so for now we need to enable it via a temporary flag.
    w3.enable_unstable_package_management_api()

    # Then we need to set the registry address that we want to use.
    # This should be an ENS address, but can also be a checksummed contract address.
    w3.pm.set_registry("ens.snakecharmers.eth")

    # This generates a Package instance of the target ethPM package.
    ens_package = w3.pm.get_package("ethregistrar", "3.0.0")

    print(ens_package)

    pass
