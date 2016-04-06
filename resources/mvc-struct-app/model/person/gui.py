#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from model.person import Person
from model.person.add import AddPerson


class PersonGUI( BaseGUI ):

    def __init__(self, manager, managers = [], parent = None):
        BaseGUI.__init__(self, manager, managers, parent)

        # establece cual sera la ventana formulario para el agregar/editar
        self.DialogAddClass = AddPerson

        # attributtes wich load in combo of filters
        self.addFilter(u'Name', Person.name)
        self.addFilter(u'Address', Person.address)

        # attributtes showed in the list
        self.addTableColumn(u'#':Person, ide)
        self.addTableColumn(u'Name', Person.name)
        self.addTableColumn(u'Address', Person.address)
        self.addTableColumn(u'Birthday', Person.birthday)
        self.addTableColumn(u'Sex', Person.sex)

        self._start_operations()
