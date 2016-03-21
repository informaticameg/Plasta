#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.logic.manager import BaseManager
from %object_name% import %Object_name%

class %Object_name%Manager( BaseManager ):

    def __init__(self, store, reset = False ):
        BaseManager.__init__(self, store, reset)
        self.CLASS = %Object_name%
        self._start_operations()
