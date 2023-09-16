import ui
import sys
import menu

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        menu.launch()
    elif len(sys.argv) > 1 and sys.argv[1] == "-i":
        app = ui.MainWindow()
        app.mainloop()
    else:
        print(
            """
Wrong parameter use it as below:
    python run.py -<arg>
    -t Terminal version
    -i Interface version
"""
        )
