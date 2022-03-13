#!/usr/bin/env python3

import sys
from PySide6 import QtCore, QtGui, QtWidgets
from . import DataCollection

app = QtWidgets.QApplication(sys.argv)
DataCollectionWindow = QtWidgets.QMainWindow()
window = DataCollection(app)
window.show()
sys.exit(app.exec())