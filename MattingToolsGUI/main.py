from PyQt5 import QtWidgets, QtGui
from main_gui import MainUI
from openvino_test import Start
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    begin = Start()
    gui = MainUI(begin)
    gui.show()
    sys.exit(app.exec_())
