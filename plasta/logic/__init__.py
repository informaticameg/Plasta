#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.utils import getModel


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class PlastaStore(object):
    __metaclass__ = Singleton

    store = None


class BaseObject(object):

    def getStore(self):
        return PlastaStore.store

    def save(self):
        store = self.getStore()
        store.flush()
        store.commit()

    def getModel(self, class_name, model=None, package='model'):
        '''
        Retorna la clase del modelo indicado

        Uso:
            getModel('Person')
            getModel('OtherName', model='other_name')
        '''
        return getModel(class_name, model, package)

    def find(self, class_name, params=[]):
        '''
        Find generico para busqueda de objetos
        '''
        store = self.getStore()
        return [obj for obj in store.find(class_name, *params)]
