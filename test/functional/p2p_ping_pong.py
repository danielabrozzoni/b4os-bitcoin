#!/usr/bin/env python3
"""Test P2P ping/pong message exchange."""

from test_framework.test_framework import BitcoinTestFramework
from test_framework.p2p import P2PInterface
from test_framework.messages import msg_ping


class P2PPingPongTest(BitcoinTestFramework):
    def set_test_params(self):
        self.num_nodes = 1

    def run_test(self):
        peer = self.nodes[0].add_p2p_connection(P2PInterface())

        nonce = 12345
        peer.send_without_ping(msg_ping(nonce=nonce))

        peer.wait_until(lambda: "pong" in peer.last_message and peer.last_message["pong"].nonce ==
   nonce)

        self.log.info("Pong received with matching nonce")


if __name__ == '__main__':
    P2PPingPongTest(__file__).main()