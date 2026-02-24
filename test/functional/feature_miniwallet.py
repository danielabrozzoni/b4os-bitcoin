#!/usr/bin/env python3
"""Test MiniWallet as a test helper."""

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_greater_than
from test_framework.wallet import MiniWallet


class MiniWalletTest(BitcoinTestFramework):
    def set_test_params(self):
        self.num_nodes = 1

    def run_test(self):
        wallet = MiniWallet(self.nodes[0])

        assert_greater_than(wallet.get_balance(), 0)

        tx = wallet.send_self_transfer(from_node=self.nodes[0])
        txid = tx["txid"]

        assert txid in self.nodes[0].getrawmempool()

        self.generate(self.nodes[0], 1)

        assert txid not in self.nodes[0].getrawmempool()


if __name__ == '__main__':
    MiniWalletTest(__file__).main()
