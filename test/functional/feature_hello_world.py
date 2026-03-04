#!/usr/bin/env python3
# Copyright (c) 2017-present The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Hello from Floripa! :)"""
from test_framework.test_framework import BitcoinTestFramework


class HelloTest(BitcoinTestFramework):
    def set_test_params(self):
        self.num_nodes = 1
        
  
    def run_test(self):
        self.log.info("Hello Brazil!")


if __name__ == "__main__":
    HelloTest(__file__).main()
