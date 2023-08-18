from tkinter import Tk, Button


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
        button = Button(self, text="Hello", command=self.hello)
        button.pack()

    def hello(self):
        print("hello")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
