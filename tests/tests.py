#!/bin/env python

import unittest
from budget import Budget


class TestBudget(unittest.TestCase):
    def test_works(self):
        Budget().get_transactions(2017, 10)
        Budget().insert_transactions()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
