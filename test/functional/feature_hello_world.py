#!/usr/bin/env python3
# Copyright (c) 2017-present The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""My first test
"""

from test_framework.test_framework import BitcoinTestFramework

class HelloWorldTest(BitcoinTestFramework):
    def run_test(self):
        """Hello Test"""
        self.log.info("Hello Tests!")
    
    def set_test_params(self):
        """Hello Test params"""
        self.num_nodes = 1

if __name__ == '__main__':
    HelloWorldTest(__file__).main()
