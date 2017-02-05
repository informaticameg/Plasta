#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from person import Person
from person.add import AddPerson


class PersonGUI( BaseGUI ):

    def __init__(self, manager, managers = [], parent = None):
        BaseGUI.__init__(self, manager, managers, parent)
        # establece cual sera la ventana formulario para el agregar/editar
        self.DialogAddClass = AddPerson
        self.loadUI()

        # attributtes wich load in combo of filters
        self.addFilter(u'Name', Person.name)

        # attributtes showed in the list
        self.addTableColumn(u'#', Person.id, alignment='C')
        self.addTableColumn(u'Name', Person.name)
        self.addTableColumn(u'Country', Person.country)

        self.pluralTitle = u'Persons'
        self._start_operations()
