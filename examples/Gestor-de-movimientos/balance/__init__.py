#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

class Balance ():

    def __init__(self):
        pass

    def actualizar(self, unMonto, tipo):
        monto_actual = self.valor()
        balance = open("movimiento/data.dll",'w')
        monto_nuevo = 0
        if tipo == u'Ingreso' :
            monto_nuevo = monto_actual + unMonto
        else:
            monto_nuevo = monto_actual - unMonto
        balance.write(str(monto_nuevo))
        balance.close()

    def valor(self):
        if not os.path.exists("movimiento/data.dll") :
            balance = open("movimiento/data.dll",'w')
            balance.write("0")
            balance.close()
        balance = open("movimiento/data.dll",'r')
        try:
            monto_actual = float(balance.readline())
        except ValueError:
            monto_actual = 0
        balance.close()
        return monto_actual

    def cuentasIngreso(self, cuentas):
        balance = 0
        for cuenta in cuentas :
            balance += float( cuenta.monto )
        return balance

    def cuentasEgreso(self, cuentas):
        balance = 0
        for cuenta in cuentas :
            balance += float( cuenta.monto )
        return balance
