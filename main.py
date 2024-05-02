import sys
import os
import shutil
from PyQt5 import QtWidgets
from ui.MainWindow import MainWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()  # Create an instance of MainWindow
    mainWindow.show()  # Show the main window
    sys.exit(app.exec_())  # Start the event loop

if __name__ == "__main__":
    main()
