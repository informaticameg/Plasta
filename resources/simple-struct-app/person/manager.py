#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.logic.manager import BaseManager
from person import Person

class PersonManager( BaseManager ):

    def __init__(self, store, reset = False ):
        BaseManager.__init__(self, store, reset)
        # set the class model wich controlling
        self.CLASS = Person

        self._start_operations()
