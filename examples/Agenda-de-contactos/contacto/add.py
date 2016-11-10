#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui.add import BaseAdd
from contacto import Contacto

class AddContacto( BaseAdd ):

    def __init__(self, manager, itemToEdit = False, managers = []):
        BaseAdd.__init__(self, manager, itemToEdit, managers)
        self.loadUI('contacto/add.ui')

        self.linkToAttribute(self.leNombre, Contacto.nombre)
        self.linkToAttribute(self.leApellido, Contacto.apellido)
        self.linkToAttribute(self.leNumero, Contacto.numero)
        self.linkToAttribute(self.leEmail, Contacto.email)

        self._start_operations()
