import csv
import config
from typing import List


class User:
    def __init__(self, dni, name, surname) -> None:
        self.dni = dni
        self.name = name
        self.surname = surname

    def __str__(self) -> str:
        return f"({self.dni}) {self.name} {self.surname}"

    def to_dict(self) -> dict:
        return {'dni': self.dni, 'name': self.name, 'surname': self.surname}


class Users:
    users_list: list = []
    with open(config.DATABASE_PATH, newline="\n") as file:
        reader = csv.reader(file, delimiter=";")
        for dni, name, surname in reader:
            user = User(dni, name, surname)
            users_list.append(user)

    @staticmethod
    def find(dni: str) -> User | None:
        for user in Users.users_list:
            if user.dni == dni:
                return user
        return None

    @staticmethod
    def create(dni: str, name: str, surname: str) -> User:
        user = User(dni, name, surname)
        Users.users_list.append(user)
        Users.save()
        return user

    @staticmethod
    def update(dni: str, name: str, surname: str) -> List[User] | None:
        for index, user in enumerate(Users.users_list):
            if user.dni == dni:
                Users.users_list[index].name = name
                Users.users_list[index].surname = surname
                Users.save()
                return Users.users_list[index]
        return None

    @staticmethod
    def delete(dni: str) -> List[User] | None:
        for index, user in enumerate(Users.users_list):
            if user.dni == dni:
                user = Users.users_list.pop(index)
                Users.save()
                return user
        return None

    @staticmethod
    def save() -> None:
        with open(config.DATABASE_PATH, "w", newline="\n") as file:
            writer = csv.writer(file, delimiter=";")
            for user in Users.users_list:
                writer.writerow((user.dni, user.name, user.surname))
