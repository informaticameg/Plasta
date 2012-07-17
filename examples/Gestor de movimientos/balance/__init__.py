#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

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
    