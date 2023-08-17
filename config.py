import sys

DATABASE_PATH = "customers.csv"

if "pytest" in sys.argv[0]:
    DATABASE_PATH = "tests/customers_test.csv"
