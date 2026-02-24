#!/usr/bin/env python3
"""b4os functional test."""

from test_framework.test_framework import BitcoinTestFramework


class B4osTest(BitcoinTestFramework):
      def set_test_params(self):
          self.num_nodes = 1

      def run_test(self):
          self.log.info("b4os")


if __name__ == '__main__':
      B4osTest(__file__).main()