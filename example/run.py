import sys

from PyQt5.QtWidgets import *

from ui.Main_windows import Main_windows

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Main_windows()
    main_window.show()
    app.exec_()