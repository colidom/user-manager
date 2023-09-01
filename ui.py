import database as db
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING


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


class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()  # Inheritance of methods of class Tk
        self.title("Customers Manager")
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

        for customer in db.Customers.customers_list:
            treeview.insert(
                parent="",
                index="end",
                iid=customer.dni,
                values=(customer.dni, customer.name, customer.surname),
            )

        # Pack
        treeview.pack()

        # Bottom Frame
        frame = Frame(self)
        frame.pack(pady=20)

        # Buttons
        Button(frame, text="Create", command=None).grid(row=0, column=0)
        Button(frame, text="Modify", command=None).grid(row=0, column=1)
        Button(frame, text="Delete", command=self.delete).grid(row=0, column=2)

        # Export treeview to the class
        self.treeview = treeview

    def delete(self):
        customer = self.treeview.focus()
        if customer:
            fields = self.treeview.item(customer, "values")
            confirm = askokcancel(
                title="Confirmation",
                message=f"¿Are you sure you want to eliminate {fields[1]} {fields[2]}?",
                icon=WARNING,
            )
        if confirm:
            # remove the row
            self.treeview.delete(customer)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
