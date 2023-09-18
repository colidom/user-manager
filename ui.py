import database as db
import helpers
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING

KEY_RELEASE = "<KeyRelease>"


class CenterWidgetMixin:
    def center(self):
        self.update()
        width = self.winfo_width()
        height = self.winfo_height()
        width_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x = int(width_screen / 2 - width / 2)
        y = int(height_screen / 2 - height / 2)
        self.geometry(f"{width}x{height}+{x}+{y}")


class CustomerCreationWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Create user")
        self.build()
        self.center()
        # Forcing the user to interact with the subwindow
        self.transient(parent)
        self.grab_set()

    def build(self):
        # Top frame
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        # Labels
        Label(frame, text="DNI (8 int 1 upper char)").grid(row=0, column=0)
        Label(frame, text="Name (2 to 30 chars)").grid(row=0, column=1)
        Label(frame, text="Surname (2 to 30 chars)").grid(row=0, column=2)

        # Entries
        dni = Entry(frame)
        name = Entry(frame)
        surname = Entry(frame)

        dni.grid(row=1, column=0)
        name.grid(row=1, column=1)
        surname.grid(row=1, column=2)

        dni.bind(KEY_RELEASE, lambda event: self.validate(event, 0))
        name.bind(KEY_RELEASE, lambda event: self.validate(event, 1))
        surname.bind(KEY_RELEASE, lambda event: self.validate(event, 2))

        # Bottom frame
        frame = Frame(self)
        frame.pack(pady=10)

        # Buttons
        create = Button(frame, text="Create", command=self.create_customer)
        create.configure(state=DISABLED)
        create.grid(row=0, column=0)
        Button(frame, text="Cancel", command=self.close).grid(row=0, column=1)

        self.validations = [0, 0, 0]
        self.create = create
        self.dni = dni
        self.name = name
        self.surname = surname

    def create_customer(self):
        self.master.treeview.insert(
            parent='',
            index='end',
            iid=self.dni.get(),
            values=(self.dni.get(), self.name.get(), self.surname.get()),
        )
        db.Users.create(self.dni.get(), self.name.get(), self.surname.get())
        print(
            f"User {self.name.get()} {self.surname.get()} width DNI {self.dni.get()} successfully created!"
        )
        self.close()

    def close(self):
        self.destroy()
        self.update()

    def validate(self, event, index):
        value = event.widget.get()
        # Validar el dni si es el primer campo o textual para los otros dos
        valid = (
            helpers.validate_dni(value, db.Users.users_list)
            if index == 0
            else (value.isalpha() and len(value) >= 2 and len(value) <= 30)
        )
        event.widget.configure({"bg": "Green" if valid else "Red"})
        # Change button status based on validations
        self.validations[index] = valid
        self.create.config(state=NORMAL if self.validations == [1, 1, 1] else DISABLED)


class CustomerEditWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Edit user")
        self.build()
        self.center()
        # Forcing the user to interact with the subwindow
        self.transient(parent)
        self.grab_set()

    def build(self):
        # Top frame
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        # Labels
        Label(frame, text="DNI (Not editable)").grid(row=0, column=0)
        Label(frame, text="Name (2 to 30 chars)").grid(row=0, column=1)
        Label(frame, text="Surname (2 to 30 chars)").grid(row=0, column=2)

        # Entries
        dni = Entry(frame)
        name = Entry(frame)
        surname = Entry(frame)

        dni.grid(row=1, column=0)
        name.grid(row=1, column=1)
        surname.grid(row=1, column=2)

        name.bind(KEY_RELEASE, lambda event: self.validate(event, 0))
        surname.bind(KEY_RELEASE, lambda event: self.validate(event, 1))

        user = self.master.treeview.focus()
        fields = self.master.treeview.item(user, 'values')
        dni.insert(0, fields[0])
        dni.config(state=DISABLED)
        name.insert(1, fields[1])
        surname.insert(2, fields[2])

        # Bottom frame
        frame = Frame(self)
        frame.pack(pady=10)

        # Buttons
        edit = Button(frame, text="Edit", command=self.edit_customer)
        edit.grid(row=0, column=0)
        Button(frame, text="Cancel", command=self.close).grid(row=0, column=1)

        self.validations = [1, 1]
        self.edit = edit
        self.dni = dni
        self.name = name
        self.surname = surname

    def edit_customer(self):
        user = self.master.treeview.focus()
        self.master.treeview.item(
            user, values=(self.dni.get(), self.name.get(), self.surname.get())
        )
        db.Users.update(self.dni.get(), self.name.get(), self.surname.get())
        print(f"User {user} edited!")
        self.close()

    def close(self):
        self.destroy()
        self.update()

    def validate(self, event, index):
        value = event.widget.get()
        # Validate the dni if it is the first field or textual for the other two fields
        valid = value.isalpha() and len(value) >= 3 and len(value) <= 30
        event.widget.configure({"bg": "Green" if valid else "Red"})

        # Change status based on validations
        self.validations[index] = valid
        self.edit.config(state=NORMAL if self.validations == [1, 1] else DISABLED)


class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()  # Inheritance of methods of class Tk
        self.title("Users Manager")
        self.build()
        self.center()

    def build(self):
        # Top Frame
        frame = Frame(self)
        frame.pack()

        # Treeview
        treeview = ttk.Treeview(frame)
        treeview["columns"] = ("DNI", "Name", "Surname")

        # Column format
        treeview.column("#0", width=0, stretch=NO)
        treeview.column("DNI", anchor=CENTER)
        treeview.column("Name", anchor=CENTER)
        treeview.column("Surname", anchor=CENTER)

        # Heading format
        treeview.heading("#0", anchor=CENTER)
        treeview.heading("DNI", text="DNI", anchor=CENTER)
        treeview.heading("Name", text="Name", anchor=CENTER)
        treeview.heading("Surname", text="Surname", anchor=CENTER)

        # Scrollbar
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        treeview["yscrollcommand"] = scrollbar.set

        for user in db.Users.users_list:
            treeview.insert(
                parent="",
                index="end",
                iid=user.dni,
                values=(user.dni, user.name, user.surname),
            )

        # Pack
        treeview.pack()

        # Bottom Frame
        frame = Frame(self)
        frame.pack(pady=20)

        # Buttons
        Button(frame, text="Create", command=self.create).grid(row=0, column=0)
        Button(frame, text="Modify", command=self.edit).grid(row=0, column=1)
        Button(frame, text="Delete", command=self.delete).grid(row=0, column=2)

        # Export treeview to the class
        self.treeview = treeview

    def delete(self):
        user = self.treeview.focus()
        if user:
            fields = self.treeview.item(user, "values")
            confirm = askokcancel(
                title="Confirmation",
                message=f"¿Are you sure you want to eliminate {fields[1]} {fields[2]}?",
                icon=WARNING,
            )
        if confirm:
            # remove the row
            self.treeview.delete(user)
            db.Users.delete(fields[0])
            print(f"User {user} deleted!")

    def create(self):
        CustomerCreationWindow(self)

    def edit(self):
        if self.treeview.focus():
            CustomerEditWindow(self)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
