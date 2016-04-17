#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from contacto import Contacto
from contacto.add import AddContacto


class ContactosGUI( BaseGUI ):

    def __init__(self, manager, managers = []):
        BaseGUI.__init__(self, manager, managers)
        self.DialogAddClass  = AddContacto
        self.loadUI()

        # elementos en el combo de filtros
        self.addFilter(u'Nombre', Contacto.nombre)
        self.addFilter(u'Apellido', Contacto.apellido)
        self.addFilter(u'Numero', Contacto.numero)
        self.addFilter(u'E-mail', Contacto.email)

        # atributos mostrados en la lista
        self.addTableColumn(u' ', Contacto.ide, alignment='C')
        self.addTableColumn(u'Nombre', Contacto.nombre)
        self.addTableColumn(u'Apellido', Contacto.apellido)
        self.addTableColumn(u'Numero', Contacto.numero, alignment='C')
        self.addTableColumn(u'E-mail', Contacto.email, fnParse=self.parseEmail)

        self.pluralTitle = "Contactos"
        self.lang = 'en'
        self._start_operations()

    def parseEmail(self, row, currentValue):
        # example use parse attribute
        return currentValue.upper()