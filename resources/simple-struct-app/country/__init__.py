#!/usr/bin/env python
# -*- coding: utf-8 -*-

from storm.locals import *


class Country(object):

    __storm_table__ = "countries"

    id = Int(primary = True)
    code = Unicode()
    name = Unicode()

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        return self.name