import copy
import csv
import config
import unittest
import helpers
import database as db


class TestDatabase(unittest.TestCase):
    def setUp(self):
        db.Users.users_list = [
            db.User("00000000T", "Martha", "Smith"),
            db.User("11111111T", "Jhon", "Doe"),
            db.User("33333333T", "Tim", "Berners-Lee"),
        ]

    def test_find_customer(self):
        existing_customer = db.Users.find("00000000T")
        unexisting_customer = db.Users.find("66666666T")
        self.assertIsNotNone(existing_customer)
        self.assertIsNone(unexisting_customer)

    def test_create_customer(self):
        new_customer = db.Users.create("444444444T", "Carlos", "Oliva")
        self.assertEqual(len(db.Users.users_list), 4)
        self.assertEqual(new_customer.dni, "444444444T")
        self.assertEqual(new_customer.name, "Carlos")
        self.assertEqual(new_customer.surname, "Oliva")

    def test_update_customer(self):
        user = copy.copy(db.Users.find("00000000T"))
        modified_customer = db.Users.update("00000000T", "Steve", "Jobs")
        self.assertEqual(user.name, "Martha")
        self.assertEqual(modified_customer.name, "Steve")

    def test_delete_customer(self):
        deleted_customer = db.Users.delete("00000000T")
        find_customer = db.Users.find("00000000T")
        self.assertNotEqual(deleted_customer, find_customer)

    def test_validate_dni(self):
        self.assertTrue(helpers.validate_dni("88888888T", db.Users.users_list))
        self.assertFalse(helpers.validate_dni("33333333T", db.Users.users_list))
        self.assertFalse(helpers.validate_dni("0000000T", db.Users.users_list))
        self.assertFalse(helpers.validate_dni("T0000000", db.Users.users_list))

    def test_write_csv(self):
        db.Users.update("00000000T", "Steve", "Jobs")
        db.Users.delete("11111111T")
        db.Users.delete("33333333T")

        dni, name, surname = None, None, None
        with open(config.DATABASE_PATH, newline="\n") as file:
            reader = csv.reader(file, delimiter=";")
            dni, name, surname = next(reader)

        self.assertEqual(dni, "00000000T")
        self.assertEqual(name, "Steve")
        self.assertEqual(surname, "Jobs")


if __name__ == "__main__":
    unittest.main()
