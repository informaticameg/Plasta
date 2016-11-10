#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from country import Country
from country.add import AddCountry


class CountryGUI( BaseGUI ):

    def __init__(self, manager, managers = [], parent = None):
        BaseGUI.__init__(self, manager, managers, parent)
        self.DialogAddClass = AddCountry
        self.loadUI()

        self.addFilter(u'Name', Country.name)
        self.addFilter(u'Code', Country.code)

        # attributtes showed in the list
        self.addTableColumn(u'Code', Country.code, alignment='C')
        self.addTableColumn(u'Name', Country.name)

        self.plurarTitle = u'Countries'
        self._start_operations()
        self.disableWidgets(['btNew', 'btEdit', 'btDelete'])
