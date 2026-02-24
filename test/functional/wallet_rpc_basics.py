#!/usr/bin/env python3
"""Basic wallet RPC flow test."""

from decimal import Decimal

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal, assert_greater_than


class WalletRPCBasicsTest(BitcoinTestFramework):
    def set_test_params(self):
        self.num_nodes = 2
        self.setup_clean_chain = True

    def skip_test_if_missing_module(self):
        self.skip_if_no_wallet()

    def run_test(self):
          
        self.nodes[0].createwallet("node0_wallet")
        node0_wallet = self.nodes[0].get_wallet_rpc("node0_wallet")

        self.nodes[1].createwallet("node1_wallet")
        node1_wallet = self.nodes[1].get_wallet_rpc("node1_wallet")

         
        addr0 = node0_wallet.getnewaddress()
        self.generatetoaddress(self.nodes[0], 101, addr0)

        assert_equal(node0_wallet.getbalance(), Decimal("50.00000000"))

         
        addr = node1_wallet.getnewaddress()
        txid = node0_wallet.sendtoaddress(addr, 1)

          
        self.sync_mempools()
        assert txid in self.nodes[0].getrawmempool()
        assert txid in self.nodes[1].getrawmempool()

         
        assert_greater_than(Decimal("49"), node0_wallet.getbalance())

         
        self.generate(self.nodes[0], 1)


        assert txid not in self.nodes[0].getrawmempool()
        assert txid not in self.nodes[1].getrawmempool()

         
        assert_equal(node1_wallet.getbalance(), Decimal("1.00000000"))


if __name__ == '__main__':
    WalletRPCBasicsTest(__file__).main()