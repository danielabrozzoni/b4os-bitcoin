#!/usr/bin/env python3
# Copyright (c) 2017-present The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test Prune debug log"""

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_not_equal, assert_equal

class PruneDebugLogTest(BitcoinTestFramework):
    def set_test_params(self):
        self.num_nodes = 1

    def setup_network(self):
        self.setup_nodes()

    def run_test(self):
        with self.nodes[0].assert_debug_log([], ["Prune configured to target"]):
            self.restart_node(0)
            
        is_pruned = self.nodes[0].getblockchaininfo()["pruned"]
        assert_not_equal(is_pruned, True)
        
        with self.nodes[0].assert_debug_log(["Prune configured to target"], []):
            self.restart_node(0, extra_args=["-prune=550"])
            
        is_pruned = self.nodes[0].getblockchaininfo()["pruned"]
        assert_equal(is_pruned, True)
        


if __name__ == "__main__":
    PruneDebugLogTest(__file__).main()
