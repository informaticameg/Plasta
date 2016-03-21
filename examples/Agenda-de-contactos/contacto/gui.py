#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from contacto import Contacto
from contacto.add import AddContacto


class ContactosGUI( BaseGUI ):
    
    def __init__(self, manager, managers = []):
        BaseGUI.__init__(self, manager, managers)
        
        self.DialogAddClass  = AddContacto
        
        # elementos en el combo de filtros
        self.ATRI_COMBO_BUSQUEDA = [ 
        {u'Nombre':Contacto.nombre},
        {u'Apellido':Contacto.apellido},
        {u'Numero':Contacto.numero},
        {u'E-mail':Contacto.email},
        ]

        # alineacion de los atributos en la lista
        self.ALINEACIONLISTA = ['C','L','L','C','L']        
        
        # atributos mostrados en la lista
        self.ATRIBUTOSLISTA = [ 
        {u' ':Contacto.ide},
        {u'Nombre':Contacto.nombre},
        {u'Apellido':Contacto.apellido},
        {u'Numero':Contacto.numero},
        {u'E-mail':Contacto.email},
        ]
        self._start_operations()                
