#!/usr/bin/env python3
# Copyright (c) 2015-present The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
#!/usr/bin/env python3
from decimal import Decimal
from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal

class WalletRPCBasics(BitcoinTestFramework):
    def set_test_params(self):
        self.num_nodes = 2

    def skip_test_if_missing_module(self):
        self.skip_if_no_wallet()


    def run_test(self):
        # Step 2: Create wallets and get RPC handles
        self.nodes[0].createwallet("node0_wallet")
        node0_wallet = self.nodes[0].get_wallet_rpc("node0_wallet")
        self.nodes[1].createwallet("node1_wallet")
        node1_wallet = self.nodes[1].get_wallet_rpc("node1_wallet")

        # Step 3: Mine 101 blocks to node0_wallet
        mining_address = node0_wallet.getnewaddress()
        self.generatetoaddress(self.nodes[0], 101, mining_address)

        # Step 4: Check node0_wallet balance is 25 BTC (current regtest block reward)
        assert_equal(node0_wallet.getbalance(), Decimal("25.00000000"))

        # Step 5: Send 1 BTC to node1_wallet address
        address1 = node1_wallet.getnewaddress()
        txid = node0_wallet.sendtoaddress(address1, Decimal("1.00000000"))

        # Step 6: Check txid in both mempools
        self.sync_mempools()
        assert txid in node0_wallet.getrawmempool()
        assert txid in node1_wallet.getrawmempool()

        # Step 7: Check node0_wallet balance is less than 49 BTC
        assert node0_wallet.getbalance() < Decimal("49.00000000")

        # Step 8: Mine one more block to node0_wallet
        self.generate(self.nodes[0], 1)

        # Step 9: Check txid leaves mempool
        assert txid not in node0_wallet.getrawmempool()
        assert txid not in node1_wallet.getrawmempool()

        # Step 10: Check node1_wallet balance is 1 BTC
        assert_equal(node1_wallet.getbalance(), Decimal("1.00000000"))

if __name__ == '__main__':
    WalletRPCBasics(__file__).main()