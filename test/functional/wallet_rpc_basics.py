#!/usr/bin/env python3
# Copyright (c) 2017-present The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""My first test
"""

from test_framework.test_framework import BitcoinTestFramework
from decimal import Decimal
from test_framework.util import (
    assert_equal,
    assert_greater_than_or_equal,
)
from test_framework.blocktools import COINBASE_MATURITY

class HelloWorldTest(BitcoinTestFramework):
    def set_test_params(self):
        """Setup two nodes"""
        self.num_nodes = 2
        self.setup_clean_chain = True


    def skip_test_if_missing_module(self):
        self.skip_if_no_wallet()
        

    def run_test(self):
        """Wallet RPC Basics"""
        self.log.info("Setup wallet 0...")
        self.nodes[0].createwallet("node0_wallet")
        w0 = self.nodes[0].get_wallet_rpc("node0_wallet")
        w0_addy = w0.getnewaddress()

        self.log.info(f"Mining {COINBASE_MATURITY + 1} blocks and sending rewards to node0_wallet")
        self.generatetoaddress(
            self.nodes[0],
            COINBASE_MATURITY + 1,
            w0_addy,
            sync_fun=lambda: self.sync_all(self.nodes[0:2])
        )

        # After mining 101 blocks we should have 50 BTC
        # Because only 1st block can be spent at the current height
        assert_equal(w0.getbalance(), Decimal("50.00000000"))

        self.log.info("Setup wallet 1...")
        self.nodes[1].createwallet("node1_wallet")
        w1 = self.nodes[1].get_wallet_rpc("node1_wallet")
        w1_addy = w1.getnewaddress()

        # Send 1.0 BTC balance w0 -> w1
        txid = w0.sendtoaddress(w1_addy, 1)

        self.log.info("Validating mempool and balance...")
        # We should not have the balance yet ( we need to mine a block)
        assert_equal(w1.getbalance(), Decimal("0.00000000"))

        # txout should not be outside of the mempool
        txout = self.nodes[0].gettxout(txid, 0, False)
        assert txout is None

        # txout should be on the local the mempool
        txout = self.nodes[0].gettxout(txid, 0, True)
        assert txout is not None

        # Wallet 0 should have 49 BTCs
        assert_greater_than_or_equal(Decimal(49.00), w0.getbalance())
        
        self.generate(
            self.nodes[0],
            1,
            sync_fun=lambda: self.sync_all(self.nodes[0:2])
        )
        txout = self.nodes[0].gettxout(txid, 0, True)

        # Wallet 0 should have 49 BTCs + 50 (2nd block reward)
        assert_greater_than_or_equal(Decimal(99.00), w0.getbalance())

        # Assert tx is outside the mempool
        txout = self.nodes[0].gettxout(txid, 0, False)
        assert txout is not None

        # After mining a block the balance should show up
        assert_equal(w1.getbalance(), Decimal("1.00000000"))


if __name__ == '__main__':
    HelloWorldTest(__file__).main()
