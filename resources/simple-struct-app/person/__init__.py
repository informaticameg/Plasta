#!/usr/bin/env python
# -*- coding: utf-8 -*-

from storm.locals import *
from country import Country


class Person(object):

    __storm_table__ = "persons"

    id = Int(primary = True)
    name = Unicode()
    country_id = Int()
    country = Reference(country_id, Country.id)

    def __init__(self, name, country):
        self.name = name
        self.country = country

    def __str__(self):
        return self.name