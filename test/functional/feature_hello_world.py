#!/usr/bin/env python3
"""A very minimalistic Hello World test!
"""
from collections import defaultdict
from test_framework.test_framework import BitcoinTestFramework


class ExampleTest(BitcoinTestFramework):
    def set_test_params(self):
        self.setup_clean_chain = True
        self.num_nodes = 1

    def run_test(self):
        """Main test logic"""

        self.log.info("Hello Brazil!")


if __name__ == '__main__':
    ExampleTest(__file__).main()
