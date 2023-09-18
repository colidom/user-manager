import sys

DATABASE_PATH = "users.csv"

if "pytest" in sys.argv[0]:
    DATABASE_PATH = "tests/users_test.csv"
