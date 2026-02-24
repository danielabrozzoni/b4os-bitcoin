#!/usr/bin/env python3
# Copyright (c) 2017-present The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""
https://github.com/exd02/b4os-bitcoin-core-materials/blob/master/learning-bitcoin-core-functional-tests/exercises/03-easy-miniwallet-support.md
"""

from decimal import Decimal
from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import (
    assert_greater_than,
)
from test_framework.wallet import (
    MiniWallet,
)

class MiniWalletTest2(BitcoinTestFramework):
    def run_test(self):
        self.log.info("Creating MiniWallet")
        miniwallet = MiniWallet(self.nodes[0])

        # by default miniwallet should start with balance
        assert_greater_than(miniwallet.get_balance(), Decimal(0.000000))

        tx = miniwallet.send_self_transfer(from_node=self.nodes[0])

        # transaction should be in mempool
        mempool = self.nodes[0].getrawmempool()
        assert tx["txid"] in mempool

        self.generate(self.nodes[0], 1)

        # after mining a block the txid should not be in mempool
        mempool = self.nodes[0].getrawmempool()
        assert tx["txid"] not in mempool

    def set_test_params(self):
        self.num_nodes = 1

if __name__ == '__main__':
    MiniWalletTest2(__file__).main()
