#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, config
from PyQt4 import QtCore, QtGui
from plasta.utils.qt import centerOnScreen, loadUI


class MainWindow(QtGui.QMainWindow):

    def __init__(self, views, managers = None):
        QtGui.QMainWindow.__init__(self)
        loadUI(self, '/gui/mainwindow.ui')
        centerOnScreen(self)
        self.setWindowTitle(config.MAIN_TITLE)

        self.views = views
        self.managers = managers