#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from GUI.mainwindow import MainWindow
from managers import Managers
from plasta.config import config

config.LANG = 'es'

app = QtGui.QApplication(sys.argv)
window = MainWindow( Managers() )
window.show()
sys.exit(app.exec_())