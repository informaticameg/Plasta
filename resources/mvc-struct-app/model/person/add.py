#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui.add import BaseAdd
from PyQt4 import uic
from os.path import join, abspath, dirname
from model.person import Person
from datetime import datetime as dt

class AddPerson( BaseAdd ):

    def __init__(self, manager, itemToEdit = False, managers = [], parent=None):
        BaseAdd.__init__(self, manager, itemToEdit, managers, parent)
        self.loadUI(join(abspath(dirname(__file__)), 'add.ui'))

        self.linkToAttribute(self.leName, Person.name)
        self.linkToAttribute(self.leAddress, Person.address)
        self.linkToAttribute(self.dtBirthday, Person.birthday)
        self.linkToAttribute(self.cbSex, Person.sex)

        self.setParser(Person.birthday, lambda (v): dt.strptime(v, '%d/%m'))
        self._start_operations()