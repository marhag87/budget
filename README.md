Budget
======
A module for keeping track of your budget

Testing
=======
Add access rules in tou pg_hba.conf:
`host    budget_test     budget_test_ro  127.0.0.1/32            md5`
`host    budget_test     budget_test_rw  127.0.0.1/32            md5`
Install requirements:
`pip install -r requirements.txt`
Run tox:
`tox`
