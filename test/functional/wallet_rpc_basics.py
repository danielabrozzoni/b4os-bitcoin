#!/usr/bin/env python3
# Copyright (c) 2014-present The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test the wallet."""
from decimal import Decimal
from itertools import product

from test_framework.blocktools import COINBASE_MATURITY
from test_framework.descriptors import descsum_create
from test_framework.messages import (
    COIN,
    DEFAULT_ANCESTOR_LIMIT,
)
from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import (
    assert_equal,
    assert_greater_than,
)

NOT_A_NUMBER_OR_STRING = "Amount is not a number or string"
OUT_OF_RANGE = "Amount out of range"


class WalletTest(BitcoinTestFramework):
    def set_test_params(self):
        self.setup_clean_chain = True
        self.num_nodes = 2

    def skip_test_if_missing_module(self):
        self.skip_if_no_wallet()

    def setup_network(self):
        self.setup_nodes()
        # Only need nodes 0-1 running at start of test
        self.connect_nodes(0, 1)
        self.sync_all(self.nodes[0:1])


    def run_test(self):
        # Create wallets and rpc handles
        self.nodes[0].createwallet("node0_wallet")
        node0_wallet = self.nodes[0].get_wallet_rpc("node0_wallet")

        self.nodes[1].createwallet("node1_wallet")
        node1_wallet = self.nodes[1].get_wallet_rpc("node1_wallet")


        # Generate a new address for the wallet and mine to it
        mining_address = node0_wallet.getnewaddress()
        self.generatetoaddress(self.nodes[0], 101, mining_address)

        # Log balance after mining
        self.log.info(f"Balance after mining: {node0_wallet.getbalance()}")

        assert_equal(node0_wallet.getbalance(), Decimal("50.00000000"))

        node1_address = node1_wallet.getnewaddress()

        txid = node0_wallet.sendtoaddress(node1_address, 1)

        self.sync_mempools()

        assert_greater_than(Decimal("50.00000000"), node0_wallet.getbalance())
        
        self.generatetoaddress(self.nodes[0], 1, mining_address)

        assert_equal(Decimal("0.00000000"),len(self.nodes[0].getrawmempool()))
        assert_equal(Decimal("0.00000000"),len(self.nodes[1].getrawmempool()))
        
        assert_equal(node1_wallet.getbalance(), Decimal("1.00000000"))



if __name__ == '__main__':
    WalletTest(__file__).main()