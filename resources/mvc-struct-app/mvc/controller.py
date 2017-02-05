#!/usr/bin/env python
# -*- coding: utf-8 -*-

from storm.locals import create_database, Store

class Controller :

    def __init__(self):
        self.DATABASE = None
        self.store = None

        self.openConnection()

    def openConnection(self):
        self.DATABASE = None
        self.store = None

        self.DATABASE = create_database('sqlite:data.db')
        self.store = Store(self.DATABASE)

    def closeConnection(self):
        self.store.commit()
        self.store.close()
