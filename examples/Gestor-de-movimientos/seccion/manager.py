#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.logic.manager import BaseManager
from seccion import Seccion
from cuenta import Cuenta

class SeccionesManager(BaseManager):

    def __init__(self, store, reset = False, managers = []):
        BaseManager.__init__(self, store, reset)
        self.CLASS = Seccion
        self.searchname = self.CLASS.nombre
        self.managers = managers
        self.cuentasManager = managers.cuentas
        self._start_operations()

    def add(self,*params):
        try:
            obj = self.CLASS(*params)
            self.store.add(obj)
            self.store.flush()
            self.store.commit()
            return obj
        except Exception, e:
            print e
            return False

    def obtenerCuentas(self, unaSeccion):
        """ Devuelve las cuentas incluidas en una seccion """
        #return self.cuentasManager.searchBy(Cuenta.seccion, unaSeccion.nombre)
        return [obj for obj in self.cuentasManager.almacen.find(Cuenta, Cuenta.seccion_id == unaSeccion.ide)]

    def establecerSeccion(self, cuentas, unaSeccion):
        """
        Establece al conjunto de cuentas la seccion indicada.
        """
        for unaCuenta in cuentas :
            unaCuenta.seccion = unaSeccion
        self.almacen.commit()


