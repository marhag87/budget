#!/bin/env python
"""Main module for budget"""

from pathlib import Path
import pyodbc
from pyyamlconfig import (
    load_config,
    PyYAMLConfigError,
)
from pprint import pprint


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
            self.config = {}
        self.config = {**default_config, **self.config}
        self.database = pyodbc.connect(
            self.config.get('connectionstring'),
            autocommit=True,
        )
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
                event (
                    id integer primary key autoincrement,
                    title_id integer NOT NULL,
                    date date NOT NULL,
                    amount integer NOT NULL,
                    balance integer NOT NULL,
                    FOREIGN KEY(title_id) REFERENCES title(id)
                )
            '''
        )

    def get_categories(self):
        cursor = self.database.cursor()
        cursor.execute('SELECT * FROM category')
        return cursor.fetchall()

    def get_titles(self):
        cursor = self.database.cursor()
        cursor.execute('SELECT * FROM title')
        return cursor.fetchall()

    def get_events(self, year, month):
        """Example function for printing a set of events"""
        cursor = self.database.cursor()
        cursor.execute(
            f'''
            SELECT
                title.name as title,
                date,
                amount,
                balance,
                category.name as category
            FROM
                event
            JOIN
                title
            ON
                title.id = event.title_id
            JOIN
                category_map
            ON
                title.id = category_map.title_id
            JOIN
                category
            ON
                category_map.category_id = category.id
            WHERE
                date BETWEEN '{year}-{month:02}-01' AND '{year}-{month:02}-31'
            ORDER BY
                category.name,
                event.id DESC
            '''
        )
        return cursor.fetchall()

    def create_category(self, category):
        cursor = self.database.cursor()
        cursor.execute(
            f'''
            SELECT
                id
            FROM
                category
            WHERE
                name = "{category}"
            '''
        )
        category_id = cursor.fetchone()
        if category_id is None:
            cursor.execute(
                f'''
                INSERT INTO
                    category (
                        name
                    )
                VALUES (
                    "{category}"
                )
                '''
            )
            cursor.execute(
                f'''
                SELECT
                    id
                FROM
                    category
                WHERE
                    name = "{category}"
                '''
            )
            category_id = cursor.fetchone()
        return category_id

    def set_category(self, title_id, category_id):
        cursor = self.database.cursor()
        cursor.execute(
            f'''
            INSERT INTO
                category_map (
                    title_id,
                    category_id
                )
            VALUES (
                {title_id},
                {category_id}
            )
            '''
        )

    def insert_events(self, eventfile='events.txt'):
        """Insert all the transactions found in the file provided"""
        cursor = self.database.cursor()
        with open(eventfile) as file:
            lines = file.readlines()
            while lines:
                title = lines.pop(0).strip()
                date = lines.pop(0).strip()
                amount = lines.pop(0).strip()
                amount = int(amount.replace(',', '').replace(' ', ''))
                balance = lines.pop(0).strip()
                balance = int(balance.replace(',', '').replace(' ', ''))
                cursor.execute(
                    f'''
                    SELECT
                        id
                    FROM
                        title
                    WHERE
                        name = "{title}"
                    '''
                )
                try:
                    (title_id,) = cursor.fetchone()
                except TypeError:
                    title_id = None
                if title_id is None:
                    cursor.execute(
                        f'''
                        INSERT INTO
                            title (
                                name
                            )
                        VALUES (
                            "{title}"
                        );
                        '''
                    )
                    cursor.execute(
                        f'''
                        SELECT
                            id
                        FROM
                            title
                        WHERE
                            name = "{title}"
                        '''
                    )
                    (title_id,) = cursor.fetchone()

                cursor.execute(
                    f'''
                    INSERT INTO
                        event (
                            title_id,
                            date,
                            amount,
                            balance
                        )
                    VALUES (
                        {title_id},
                        "{date}",
                        {amount},
                        {balance}
                    )
                    '''
                )


if __name__ == '__main__':
    budget = Budget()
    budget.insert_events()
    budget.create_category('Groceries')
    budget.create_category('Electronics')
    budget.create_category('Games')
    budget.set_category(1, 1)
    budget.set_category(3, 2)
    budget.set_category(19, 3)
    pprint(budget.get_events(2018, 1))
    #pprint(budget.get_titles())
