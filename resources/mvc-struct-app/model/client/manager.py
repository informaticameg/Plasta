#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.logic.manager import BaseManager
from model.client import Client

class ClientManager( BaseManager ):

    def __init__(self, store, reset = False ):
        BaseManager.__init__(self, store, reset)

        self.CLASS = Client

        self._start_operations()
