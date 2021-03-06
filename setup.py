#!/bin/env python
"""
Setuptools file for budget
"""
from setuptools import (
    setup,
    find_packages,
)

setup(
    name='budget',
    author='marhag87',
    author_email='marhag87@gmail.com',
    url='https://github.com/marhag87/budget',
    version='0.1.0',
    packages=find_packages(),
    license='MIT',
    description='Keep track of your budget',
    long_description='A tool for keeping track of your budget',
    install_requires=[
        'psycopg2',
        'pyyamlconfig',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
    ],
    package_data={
        '': [
            'db/schema.sql',
            'tests/test_config.yaml',
        ],
    },
    scripts=[
        'tests/prepare_test_database.sh',
    ],
)
