#!/bin/bash

psql -U postgres -c 'DROP DATABASE IF EXISTS budget_test;'
psql -U postgres -c 'CREATE DATABASE budget_test;'
psql -U postgres budget_test -f db/schema.sql

psql -U postgres -c 'DROP USER IF EXISTS budget_test_ro;'
psql -U postgres -c "CREATE USER budget_test_ro PASSWORD 'c6EYEKPhxzh6D3GMYPXg7PGy';"
psql -U postgres -c 'GRANT CONNECT ON DATABASE budget_test TO budget_test_ro;'
psql -U postgres budget_test -c 'GRANT SELECT ON category, category_map, title, transaction TO budget_test_ro;'

psql -U postgres -c 'DROP USER IF EXISTS budget_test_rw;'
psql -U postgres -c "CREATE USER budget_test_rw PASSWORD 'UGVwZh3gdZqDXhVtQxaghvyP';"
psql -U postgres budget_test -c 'GRANT CONNECT ON DATABASE budget_test TO budget_test_rw;'
psql -U postgres budget_test -c 'GRANT SELECT, INSERT ON title TO budget_test_rw;'
psql -U postgres budget_test -c 'GRANT SELECT, USAGE ON title_id_seq TO budget_test_rw;'
