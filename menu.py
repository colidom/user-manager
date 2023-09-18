import helpers, database as db

CUSTOMER_NOT_FOUND = "User not found❌"
DNI_LENGTH = "DNI (8 int 1 char)"


def launch() -> None:
    while True:
        helpers.clean_screen()
        helpers.show_options()

        opcion = input("> ")
        helpers.clean_screen()

        match opcion:
            case "6":
                print("Leaving...\n")
                break
            case "1":
                print("Listing users...\n", *db.Users.users_list, sep="\n")
            case "2":
                find_customer()
            case "3":
                add_customer()
            case "4":
                modify_customer()
            case "5":
                delete_customer()
            case _:
                print("Please choose one of the menu options...\n")
        input("\nPress ENTER to continue...")


def find_customer() -> None:
    print("Looking for a user...\n")
    dni = helpers.read_text(9, 9, DNI_LENGTH).upper()
    user = db.Users.find(dni)
    print(user) if user else print(CUSTOMER_NOT_FOUND)


def add_customer() -> None:
    print("Adding a user...\n")
    dni = helpers.read_text(9, 9, DNI_LENGTH).upper()
    if helpers.validate_dni(dni, db.Users.users_list):
        name = helpers.read_text(2, 30, "Name (2 int 30 char)").capitalize()
        surname = helpers.read_text(2, 30, "Surname (2 int 30 char)").capitalize()
        db.Users.create(dni, name, surname)
        print("User added ✅")


def modify_customer() -> None:
    print("Modifying a user...\n")
    dni = helpers.read_text(9, 9, DNI_LENGTH).upper()
    user = db.Users.find(dni)
    if user:
        modify_existing_customer(user)
    else:
        print(CUSTOMER_NOT_FOUND)


def modify_existing_customer(user: db.User) -> None:
    name = helpers.read_text(2, 30, f"New name for {user.name}: ").capitalize()
    surname = helpers.read_text(2, 30, f"New surname for {user.surname}: ").capitalize()
    db.Users.update(user.dni, name, surname)
    print("User modified ✅")


def delete_customer() -> None:
    print("Deleting a user...\n")
    dni = helpers.read_text(9, 9, DNI_LENGTH).upper()
    print("User successfully deleted ✅") if db.Users.delete(dni) else print(
        CUSTOMER_NOT_FOUND
    )
