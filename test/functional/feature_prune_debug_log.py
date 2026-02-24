#!/usr/bin/env python3
# Copyright (c) 2017-present The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

#!/usr/bin/env python3
from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal

class FeaturePruneDebugLog(BitcoinTestFramework):
    def set_test_params(self):
        self.num_nodes = 1

    def run_test(self):
        # Step 2 & 3: Restart with default args, assert prune log not present
        with self.nodes[0].assert_debug_log([], unexpected_msgs=['Prune configured to target']):
            self.restart_node(0, extra_args=[])

        # Step 4: Assert pruning is not enabled via RPC
        info = self.nodes[0].getblockchaininfo()
        assert_equal(info["pruned"], False)

        # Step 5 & 6: Restart with prune enabled, assert prune log present
        with self.nodes[0].assert_debug_log(['Prune configured to target']):
            self.restart_node(0, extra_args=["-prune=550"])

        # Step 7: Assert pruning is enabled via RPC
        info = self.nodes[0].getblockchaininfo()
        assert_equal(info["pruned"], True)

if __name__ == '__main__':
    FeaturePruneDebugLog(__file__).main()