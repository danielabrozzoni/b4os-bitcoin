#!/usr/bin/env python3
# Copyright (c) 2017-present The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test Wallet RPC basics"""

from decimal import Decimal
from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal, assert_greater_than


class WalletRPCBasicsTest(BitcoinTestFramework):
    def set_test_params(self):
        self.setup_clean_chain = True
        self.num_nodes = 2

    def skip_test_if_missing_module(self):
        self.skip_if_no_wallet()

    def run_test(self):
        self.nodes[0].createwallet("node0_wallet")
        self.nodes[1].createwallet("node1_wallet")

        node0_wallet = self.nodes[0].get_wallet_rpc("node0_wallet")
        node1_wallet = self.nodes[1].get_wallet_rpc("node1_wallet")

        node0_wallet.getbalance()
        node1_wallet.getbalance()

        node0_address = node0_wallet.getnewaddress()

        self.generatetoaddress(self.nodes[0], 101, node0_address)

        assert_equal(node0_wallet.getbalance(), Decimal("50.0000000"))

        node1_address = node1_wallet.getnewaddress()
        txid = node0_wallet.sendtoaddress(node1_address, "1")

        self.sync_mempools()

        node0_mempool = self.nodes[0].getrawmempool()
        node1_mempool = self.nodes[1].getrawmempool()

        assert_equal(node0_mempool[0], txid)
        assert_equal(node1_mempool[0], txid)

        assert_greater_than(Decimal("49.0000000"), node0_wallet.getbalance())

        self.generatetoaddress(self.nodes[0], 1, node0_address)

        node0_mempool = self.nodes[0].getrawmempool()
        node1_mempool = self.nodes[1].getrawmempool()

        assert_equal(node0_mempool, [])
        assert_equal(node1_mempool, [])

        node1_balance = node1_wallet.getbalance()

        assert_equal(node1_balance, Decimal("1.00000000"))


if __name__ == "__main__":
    WalletRPCBasicsTest(__file__).main()
