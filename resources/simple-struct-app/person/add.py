#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui.add import BaseAdd
from person import Person

class AddPerson(BaseAdd):

    def __init__(self, manager, itemToEdit = False, managers = []):
        BaseAdd.__init__(self, manager, itemToEdit, managers)
        self.loadUI('/person/add.ui')

        self.linkToAttribute(self.leName, Person.name)
        self.linkToAttribute(self.cbCountry, Person.country)

        self._start_operations()
        self.loadReferenceCombo(self.cbCountry, Person.country, sortAttr='name')

        if itemToEdit:
            # set the country in combobox
            idx = self.references[Person.country]['objs'].index(itemToEdit.country)
            self.cbCountry.setCurrentIndex(idx)

