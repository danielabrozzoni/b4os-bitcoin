#!/usr/bin/env python3
# Copyright (c) 2017-present The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test Ping Pong"""

from test_framework.test_framework import BitcoinTestFramework
from test_framework.p2p import P2PInterface
from test_framework.messages import msg_ping
from test_framework.util import assert_equal


class PingPongTest(BitcoinTestFramework):
    def set_test_params(self):
        self.num_nodes = 1

    def run_test(self):
        peer = self.nodes[0].add_p2p_connection(P2PInterface())

        peer.last_message.pop("pong")

        msg = msg_ping(nonce=1234)
        peer.send_without_ping(msg)

        peer.wait_until(lambda: "pong" in peer.last_message, timeout=5)
        assert_equal(peer.last_message["pong"].nonce, msg.nonce)


if __name__ == "__main__":
    PingPongTest(__file__).main()
