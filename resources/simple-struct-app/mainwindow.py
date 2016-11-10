#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyQt4 import QtCore, QtGui
from plasta.utils.qt import loadUI, centerOnScreen

class MainWindow(QtGui.QMainWindow):

    def __init__(self, managers = None):
        QtGui.QMainWindow.__init__(self)
        loadUI(self, 'mainwindow.ui')
        centerOnScreen(self)
        self.setWindowTitle("Simple Struct - Example Plasta App")

        self.managers = managers

    @QtCore.pyqtSlot()
    def on_actionList_Persons_triggered(self):
        from person.gui import PersonGUI
        self.wPerson = PersonGUI(self.managers['persons'], managers = self.managers)
        self.wPerson.show()