from tkinter import Tk, Button


class MainWindow(Tk):
    def __init__(self):
        super().__init__()  # Inheritance of methods of class Tk
        self.title("Customers Manager")
        self.build()

    def build(self):
        button = Button(self, text="Hello", command=self.hello)
        button.pack()

    def hello(self):
        print("hello")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
