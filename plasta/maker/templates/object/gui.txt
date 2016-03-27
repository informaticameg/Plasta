#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from %object_name% import %Object_name%
from %object_name%.add import Add%Object_name%


class %Object_name%GUI( BaseGUI ):

    def __init__(self, manager, managers = []):
        BaseGUI.__init__(self, manager, managers)

        self.DialogAddClass = Add%Object_name%

        #self.ATRI_COMBO_BUSQUEDA = [
{attributes}
        #]

        #self.ATRIBUTOSLISTA = [
{attributes}
        #]

        self._start_operations()
