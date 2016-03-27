#!/usr/bin/env python
# -*- coding: utf-8 -*-

from storm.locals import *


class Client(object):

    __storm_table__ = "client"

    ide = Int(primary = True)
    name = Unicode()
    address = Unicode()
    phone = Unicode()

    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

    def __str__(self):
        return self.name