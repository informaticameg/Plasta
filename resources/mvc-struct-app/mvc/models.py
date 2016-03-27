#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.person.manager import PersonManager
from model.client.manager import ClientManager

class Models:

    def __init__(self, controller):
        self.controller = controller

        store = controller.store

        self.persons = PersonManager(store, reset = True)
        self.clients = ClientManager(store, reset = True)
