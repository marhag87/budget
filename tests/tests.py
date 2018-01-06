#!/bin/env python

import unittest
from budget import Budget
import psycopg2
from pyyamlconfig import load_config


class TestBudget(unittest.TestCase):
    @staticmethod
    def run_query(query):
        config = load_config('tests/test_config.yaml')
        with psycopg2.connect(
            dbname=config.get('database'),
            user=config.get('username'),
            password=config.get('password'),
            host=config.get('hostname'),
        ) as con:
            with con.cursor() as cur:
                cur.execute(query)
                return cur.fetchone()

    def test_works(self):
        Budget(config='tests/test_config.yaml').get_transactions(2017, 10)
        Budget().get_transactions(2017, 10)
        self.assertTrue(True)

    def test_insert_transactions_inserts(self):
        """Test that insert_transactions can insert data"""
        title_id = Budget(config='tests/test_config.yaml').insert_transactions(transactionfile='tests/test_transactions.txt')
        self.assertEqual(
            title_id,
            *self.run_query("SELECT id FROM title WHERE name='MING EXPRESS';")
        )


if __name__ == '__main__':
    unittest.main()
