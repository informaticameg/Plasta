#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from gui.mainwindow import MainWindow

class Views :

    def __init__(self, models):
        self.managers = models

        app = QtGui.QApplication(sys.argv)
        window = MainWindow( self , self.managers)
        window.show()
        sys.exit(app.exec_())

    def instancePersons(self):
        from model.person.gui import PersonGUI
        self.persons = PersonGUI(self.managers.persons, self.managers)
        return self.persons

    def instanceClients(self):
        from model.client.gui import ClientGUI
        self.clients = ClientGUI(self.managers.clients, self.managers)
        return self.clients
