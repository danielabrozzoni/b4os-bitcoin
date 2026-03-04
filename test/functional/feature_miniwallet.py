#!/usr/bin/env python3
# Copyright (c) 2017-present The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test MiniWallet"""

from test_framework.test_framework import BitcoinTestFramework
from test_framework.wallet import MiniWallet
from test_framework.util import assert_greater_than, assert_equal, assert_not_equal


class MiniWalletTest(BitcoinTestFramework):
    def set_test_params(self):
        self.num_nodes = 1

    def setup_network(self):
        self.setup_nodes()

    def skip_test_if_missing_module(self):
        self.skip_if_no_wallet()

    def run_test(self):
        wallet = MiniWallet(self.nodes[0])
        assert_greater_than(wallet.get_balance(), 0)

        tx = wallet.send_self_transfer(from_node=self.nodes[0])

        mempool_before = self.nodes[0].getrawmempool()

        assert_equal(tx["txid"], mempool_before[0])

        self.generatetoaddress(self.nodes[0], 1, self.nodes[0].getnewaddress())

        mempool_after = self.nodes[0].getrawmempool()

        assert_equal(len(mempool_after), 0)


if __name__ == "__main__":
    MiniWalletTest(__file__).main()
