#!/usr/bin/env python3
# Copyright (c) 2017-present The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""https://github.com/exd02/b4os-bitcoin-core-materials/blob/master/learning-bitcoin-core-functional-tests/exercises/02-easy-node-args-debug-log.md
"""

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal

class HelloWorldTest(BitcoinTestFramework):
    def run_test(self):
        """Ensure that prune mode start is working properly"""

        self.log.info("Restarting node with default args...")
        # Prune should be disabled by default
        with self.nodes[0].assert_debug_log([], unexpected_msgs=["Setting NODE_NETWORK in prune mode"]):
            self.restart_node(0)
        
        # assert that get blockchaininfo has the field pruned set to false
        assert_equal(self.nodes[0].getblockchaininfo()["pruned"], False)

        self.log.info("Restarting node with args -prune=550...")

        with self.nodes[0].assert_debug_log([], unexpected_msgs=["Setting NODE_NETWORK in non-prune mode"]):
            self.restart_node(0, extra_args=["-prune=550"])

        # assert that get blockchaininfo has the field pruned set to true
        assert_equal(self.nodes[0].getblockchaininfo()["pruned"], True)
        
    def set_test_params(self):
        """We only need one node to test prune mode"""
        self.num_nodes = 1

if __name__ == '__main__':
    HelloWorldTest(__file__).main()
