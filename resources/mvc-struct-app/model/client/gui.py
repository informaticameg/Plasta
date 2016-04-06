#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from model.client import Client
from model.client.add import AddClient


class ClientGUI( BaseGUI ):

    def __init__(self, manager, managers = [], parent = None):
        BaseGUI.__init__(self, manager, managers, parent)

        self.DialogAddClass = AddClient

        self.addFilter(u'Name', Client.name)

        self.addTableColumn(u'#', Client.ide)
        self.addTableColumn(u'Name', Client.name)
        self.addTableColumn(u'Address', Client.address)
        self.addTableColumn(u'Phone', Client.phone)

        self.pluralTitle = "Clients"
        self._start_operations()
