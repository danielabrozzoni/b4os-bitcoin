#!/usr/bin/env python3
"""Test basic wallet RPC flow: fund, send, confirm."""

from decimal import Decimal

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal, assert_greater_than


class WalletRPCBasicsTest(BitcoinTestFramework):
    def set_test_params(self):
        self.num_nodes = 2

    def skip_test_if_missing_module(self):
        self.skip_if_no_wallet()

    def run_test(self):
        # Step 2: Create wallets on each node
        self.nodes[0].createwallet("node0_wallet")
        node0_wallet = self.nodes[0].get_wallet_rpc("node0_wallet")

        self.nodes[1].createwallet("node1_wallet")
        node1_wallet = self.nodes[1].get_wallet_rpc("node1_wallet")

        # Step 3: Mine 101 blocks to node0 (1 mature coinbase = 50 BTC)
        self.generate(self.nodes[0], 101)

        # Step 4: Check node0 balance is 50 BTC
        assert_equal(node0_wallet.getbalance(), Decimal("50.00000000"))

        # Step 5: Send 1 BTC from node0 to node1
        addr1 = node1_wallet.getnewaddress()
        txid = node0_wallet.sendtoaddress(addr1, 1)

        # Step 6: Check tx is in both nodes' mempools
        self.sync_mempools()
        assert txid in self.nodes[0].getrawmempool()
        assert txid in self.nodes[1].getrawmempool()

        # Step 7: node0 balance is now less than 49 BTC (amount + fee)
        assert_greater_than(Decimal("49.00000000"), node0_wallet.getbalance())

        # Step 8: Mine one more block to confirm the transaction
        self.generate(self.nodes[0], 1)

        # Step 9: Transaction leaves the mempool
        assert txid not in self.nodes[0].getrawmempool()
        assert txid not in self.nodes[1].getrawmempool()

        # Step 10: node1 balance is 1 BTC
        assert_equal(node1_wallet.getbalance(), Decimal("1.00000000"))

        self.log.info("All checks passed!")


if __name__ == "__main__":
    WalletRPCBasicsTest(__file__).main()
