import re
import os
import platform


def clean_screen() -> None:
    os.system("cls") if platform.system() == "Windows" else os.system("clear")


def show_options() -> None:
    print("========================")
    print("  Welcome to Manager ")
    print("========================")
    print("[1] Users List      ")
    print("[2] Find User       ")
    print("[3] Add User        ")
    print("[4] Modify User     ")
    print("[5] Delete User     ")
    print("[6] Close the Manager   ")
    print("========================")


def read_text(min_length: int = 0, max_length: int = 100, msg=None) -> str:
    print(msg) if msg else None
    while True:
        text = input("> ")
        if len(text) >= min_length and len(text) <= max_length:
            return text
        print(
            f"Error! The permitted length is (min){min_length} chars y (max){max_length} chars."
        )


def validate_dni(dni: str, users_list: list) -> bool:
    if not re.match("\d{8}[A-Z]$", dni):
        print("Incorrect DNI, must comply with the format.")
        return False
    for user in users_list:
        if user.dni == dni:
            print("DNI used by another user.")
            return False
    return True
