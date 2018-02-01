#!/bin/env python
import unittest
from budget import Budget


class TestBudget(unittest.TestCase):
    def test_works(self):
        Budget(config='tests/test_config.yaml').get_transactions(2017, 10)
        Budget().get_transactions(2017, 10)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
