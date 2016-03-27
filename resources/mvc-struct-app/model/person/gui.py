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
        self.ATRI_COMBO_BUSQUEDA = [
          {u'Name':Person.name},
          {u'Address':Person.address}
        ]

        # attributtes showed in the list
        self.ATRIBUTOSLISTA = [
          {u'#':Person.ide},
          {u'Name':Person.name},
          {u'Address':Person.address},
          {u'Birthday':Person.birthday},
          {u'Sex':Person.sex}
        ]

        self._start_operations()
