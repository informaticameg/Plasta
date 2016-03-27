#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui.add_window import BaseAddWindow
from PyQt4 import uic
from os.path import join, abspath, dirname
from %object_name% import %Object_name%

class Add%Object_name%( BaseAddWindow ):

    def __init__(self, unManager, itemaeditar = False, managers = []):
        BaseAddWindow.__init__(self, unManager, itemaeditar, managers)
        FILENAME = 'add.ui'
        uic.loadUi(join(abspath(dirname(__file__)), FILENAME), self)

        self.ITEMLIST = [
{attributes}
        ]

        self._start_operations()
