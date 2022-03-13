#!/usr/bin/env python3

import pkgutil
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QMetaObject
from PySide6.QtCore import QBuffer, QIODevice

class UiLoader(QUiLoader):
    def __init__(self, base_instance):
        QUiLoader.__init__(self, base_instance)
        self.base_instance = base_instance

    def createWidget(self, class_name, parent=None, name=''):
        if parent is None and self.base_instance:
            return self.base_instance
        else:
            # create a new widget for child widgets
            widget = QUiLoader.createWidget(self, class_name, parent, name)
            if self.base_instance:
                setattr(self.base_instance, name, widget)
            return widget

def load_res_file(filename: str) -> bytes:
    return pkgutil.get_data(__name__, filename)

def load_res_file_as_QBuffer(filename: str) -> QBuffer:
    ans = QBuffer()
    ans.open(QIODevice.ReadWrite)
    ans.write(load_res_file(filename))
    ans.seek(0)
    return ans

def load_ui(ui_file, base_instance=None):
    loader = UiLoader(base_instance)
    widget = loader.load(load_res_file_as_QBuffer(ui_file))
    QMetaObject.connectSlotsByName(widget)
    return widget