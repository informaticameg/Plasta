#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyQt4 import QtCore, QtGui, uic
from os.path import join, abspath, dirname


class MainWindow(QtGui.QMainWindow):

    def __init__(self, managers = None):
        QtGui.QMainWindow.__init__(self)
        FILENAME = 'mainwindow.ui'
        uifile = join(abspath(dirname(__file__)), FILENAME)
        uic.loadUi(uifile, self)
        self.__centerOnScreen()
        self.setWindowTitle("Simple Struct - Example Plasta App")

        self.managers = managers

    def __centerOnScreen (self):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    @QtCore.pyqtSlot()
    def on_actionList_Persons_triggered(self):
        from person.gui import PersonGUI
        self.wPerson = PersonGUI(self.managers['persons'], managers = self.managers)
        self.wPerson.show()