#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyQt4 import QtCore, QtGui
from plasta.utils.qt import centerOnScreen, loadUI


class MainWindow(QtGui.QMainWindow):

    def __init__(self, views, managers = None):
        QtGui.QMainWindow.__init__(self)
        loadUI(self, '/gui/mainwindow.ui')
        centerOnScreen(self)
        self.setWindowTitle("MVC Struct - Example Plasta App")

        self.views = views
        self.managers = managers

    @QtCore.pyqtSlot()
    def on_actionList_Persons_triggered(self):
        window = self.views.instancePersons()
        window.show()

    @QtCore.pyqtSlot()
    def on_actionList_Clients_triggered(self):
        window = self.views.instanceClients()
        window.show()