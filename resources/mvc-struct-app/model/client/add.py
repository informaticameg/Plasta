#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui.add import BaseAdd
from PyQt4 import uic
from os.path import join, abspath, dirname
from model.client import Client

class AddClient( BaseAdd ):

    def __init__(self, manager, itemToEdit = False, managers = [], parent=None):
        BaseAdd.__init__(self, manager, itemToEdit, managers, parent)
        self.loadUI(join(abspath(dirname(__file__)), 'add.ui'))

        self.linkToAttribute(self.leName, Client.name)
        self.linkToAttribute(self.leAddress, Client.address)
        self.linkToAttribute(self.lePhone, Client.phone)

        self._start_operations()