#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui.add_window import BaseAddWindow
from PyQt4 import uic
from os.path import join, abspath, dirname
from model.client import Client

class AddClient( BaseAddWindow ):

    def __init__(self, manager, itemToEdit = False, managers = []):
        BaseAddWindow.__init__(self, manager, itemToEdit, managers)
        self.loadUI(join(abspath(dirname(__file__)), 'add.ui'))

        self.linkToAttribute(self.leName, Client.name)
        self.linkToAttribute(self.leAddress, Client.address)
        self.linkToAttribute(self.lePhone, Client.phone)

        self._start_operations()