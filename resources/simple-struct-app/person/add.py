#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui.add_window import BaseAddWindow
from PyQt4 import uic
from os.path import join, abspath, dirname
from person import Person

class AddPerson( BaseAddWindow ):

    def __init__(self, manager, itemToEdit = False, managers = []):
        BaseAddWindow.__init__(self, manager, itemToEdit, managers)
        uic.loadUi(join(abspath(dirname(__file__)), 'add.ui'), self)

        self.linkToAttribute(self.leName, Person.name)

        self._start_operations()