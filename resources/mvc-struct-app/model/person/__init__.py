#!/usr/bin/env python
# -*- coding: utf-8 -*-

from storm.locals import *


class Person(object):

    __storm_table__ = "person"

    ide = Int(primary = True)
    name = Unicode()
    address = Unicode()
    birthday = Date()
    sex = Unicode()

    def __init__(self, name, address, birthday, sex):
        self.name = name
        self.address = address
        self.birthday = birthday
        self.sex = sex

    def __str__(self):
        return self.name