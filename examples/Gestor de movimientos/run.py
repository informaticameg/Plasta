#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from PyQt4 import QtGui
from GUI.allmodules import AllModules
from managers import Managers


app = QtGui.QApplication(sys.argv)
window = AllModules( Managers() )
window.show()
sys.exit(app.exec_())
