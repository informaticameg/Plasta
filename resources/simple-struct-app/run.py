#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from storm.locals import create_database, Store
from PyQt4 import QtGui
from mainwindow import MainWindow

from person.manager import PersonManager
from country.manager import CountryManager

# configure and instance database
DATABASE = create_database('sqlite:data.db')
store = Store(DATABASE)

# instances of managers classess
managers = {
  'persons': PersonManager(store, reset = True),
  'countries': CountryManager(store, reset = True)
}

managers['countries'].insertCountries()

# running the app
app = QtGui.QApplication(sys.argv)
window = MainWindow( managers )
window.show()
sys.exit(app.exec_())