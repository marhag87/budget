#!/bin/env python
"""Main module for budget"""

from pathlib import Path
import pyodbc
from pyyamlconfig import (
    load_config,
    PyYAMLConfigError,
)


class Budget:
    """Main class for budget"""
    def __init__(self, config=None):
        if config is None:
            config = f'{Path.home()}/.config/budget.yaml'
        default_config = {
                'connectionstring': 'DRIVER={SQLite3};DATABASE=:memory:;',
            }
        try:
            self.config = load_config(config)
        except PyYAMLConfigError:
            pass
        self.config = {**self.config, **default_config}
        self.database = pyodbc.connect(self.config.get('connectionstring'))
        self.setup_database()

    def setup_database(self):
        cursor = self.database.cursor()
        cursor.execute(
            '''
            CREATE TABLE
                category (
                    id integer primary key autoincrement,
                    name text NOT NULL
                )
            '''
        )
        cursor.execute(
            '''
            CREATE TABLE
                title (
                    id integer primary key autoincrement,
                    name text NOT NULL
                )
            '''
        )
        cursor.execute(
            '''
            CREATE TABLE
                category_map (
                    id integer primary key autoincrement,
                    title_id integer,
                    category_id integer,
                    FOREIGN KEY(title_id) REFERENCES title(id),
                    FOREIGN KEY(category_id) REFERENCES category(id)
                )
            '''
        )
        cursor.execute(
            '''
            CREATE TABLE
                transaction (
                    id integer primary key autoincrement,
                    title_id integer NOT NULL,
                    date date NOT NULL,
                    amount integer NOT NULL,
                    balance integer NOT NULL
                )
            '''
        )
        self.database.commit()

    def get_category(self):
        cursor = self.database.cursor()
        cursor.execute('SELECT * FROM category')
        return cursor.fetchall()

    def get_transactions(self, year, month):
        """Example function for printing a set of transactions"""
        cursor = self.database.cursor()
        cursor.execute(f"SELECT * FROM transactions_for_month({year}, {month});")
        return cursor.fetchone()

    def insert_transactions(self, transactionfile='transactions.txt'):
        """Insert all the transactions found in the file provided"""
        cursor = self.database.cursor()
        with open(transactionfile) as file:
            lines = file.readlines()
            while lines:
                title = lines.pop(0).strip()
                cursor.execute(f"SELECT * FROM insert_title('{title}');")
                (title_id,) = cursor.fetchone()
                return title_id


if __name__ == '__main__':
    print(Budget().get_category())
