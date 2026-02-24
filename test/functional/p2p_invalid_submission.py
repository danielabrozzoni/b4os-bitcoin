#!/usr/bin/env python3
"""Test that an invalid transaction is rejected over P2P."""

from test_framework.messages import CInv, MSG_TX, msg_getdata, msg_tx
from test_framework.p2p import P2PInterface
from test_framework.test_framework import BitcoinTestFramework
from test_framework.wallet import MiniWallet


class P2PInvalidSubmissionTest(BitcoinTestFramework):
    def set_test_params(self):
        self.num_nodes = 1

    def run_test(self):
        wallet = MiniWallet(self.nodes[0])
        peer = self.nodes[0].add_p2p_connection(P2PInterface())

        tx = wallet.create_self_transfer()["tx"]
        tx.vin[0].prevout.n = 15

        with self.nodes[0].assert_debug_log(["bad-txns"]):
            peer.send_and_ping(msg_tx(tx))

        assert tx.txid_hex not in self.nodes[0].getrawmempool()

        getdata = msg_getdata()
        getdata.inv.append(CInv(MSG_TX, tx.txid_int))
        peer.send_without_ping(getdata)

        peer.wait_until(lambda: "notfound" in peer.last_message)
        self.log.info("Node correctly rejected invalid transaction")


if __name__ == '__main__':
    P2PInvalidSubmissionTest(__file__).main()