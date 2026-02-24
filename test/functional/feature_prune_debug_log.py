#!/usr/bin/env python3
"""Test prune mode debug log messages."""

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal


class PruneDebugLogTest(BitcoinTestFramework):
    def set_test_params(self):
        self.num_nodes = 1

    def run_test(self):
        self.log.info("Restart without prune - check no prune log message")
        with self.nodes[0].assert_debug_log([], unexpected_msgs=["Prune configured to target"]):
            self.restart_node(0, extra_args=[])

        info = self.nodes[0].getblockchaininfo()
        assert_equal(info["pruned"], False)

        self.log.info("Restart with prune=550 - check prune log message")
        with self.nodes[0].assert_debug_log(["Prune configured to target"]):
            self.restart_node(0, extra_args=["-prune=550"])

        info = self.nodes[0].getblockchaininfo()
        assert_equal(info["pruned"], True)


if __name__ == '__main__':
    PruneDebugLogTest(__file__).main()
