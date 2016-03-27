#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mvc.controller import Controller
from mvc.models import Models
from mvc.views import Views


class Main :

    def __init__(self):
        self.controller = Controller()
        self.models = Models( self.controller )
        self.views = Views( self.models )


