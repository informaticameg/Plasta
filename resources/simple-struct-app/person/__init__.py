#!/usr/bin/env python
# -*- coding: utf-8 -*-

from storm.locals import *


class Person(object):

    __storm_table__ = "person"

    ide = Int(primary = True)
    name = Unicode()

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name