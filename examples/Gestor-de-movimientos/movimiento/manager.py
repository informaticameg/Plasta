from plasta.logic.manager import BaseManager
from movimiento import Movimiento
from datetime import datetime
from cuenta.manager import CuentasManager
from cuenta import Cuenta

class MovimientosManager(BaseManager):
    """"""
    def __init__(self,almacen,reset = False):
        ''''''
        BaseManager.__init__(self,almacen,reset)
        self.CLASS = Movimiento
        self.searchname = self.CLASS.ide
        self._start_operations()

    def obtenerMovimientosDeUnaCuenta(self, unaCuenta):
        return [obj for obj in self.almacen.find(self.CLASS, Movimiento.cuenta_id == unaCuenta.ide)]       

    def obtenerMovimientosDelDia(self,unaFecha,unTipo):
        return [obj for obj in self.getall() if obj.fecha == unaFecha ]         
    
    def obtenerMovimientosDesdeHasta(self, fecha_desde, fecha_hasta, tipo_cuenta, cuenta):
        if (tipo_cuenta != u'TODOS') and (cuenta != u'TODOS') :
            cm = CuentasManager(self.almacen, False)
            unaCuenta = cm.get(cuenta)[0]
            resultado = self.almacen.find(
                Movimiento, 
                Movimiento.fecha >= fecha_desde,
                Movimiento.fecha <= fecha_hasta,                
                Movimiento.cuenta_id == unaCuenta.ide             
            )
            return [obj for obj in resultado]
        else:
            resultado = self.almacen.find(
                Movimiento, 
                Movimiento.fecha >= fecha_desde,
                Movimiento.fecha <= fecha_hasta)
            movimientos = [obj for obj in resultado]
            return self.filtrarMovimientos(movimientos, tipo_cuenta, cuenta)
    
    def filtrarMovimientos(self, movimientos, tipo_cuenta, cuenta):
        if (tipo_cuenta == u'TODOS') and (cuenta == u'TODOS'):
            return movimientos
        elif (tipo_cuenta == u'INGRESOS') and (cuenta == u'TODOS'):
            return [movimiento for movimiento in movimientos if movimiento.tipo == u"Ingreso"]
        
        elif (tipo_cuenta == u'EGRESOS') and (cuenta == u'TODOS'):
            return [movimiento for movimiento in movimientos if movimiento.tipo == u"Egreso"]
        elif (cuenta != u'TODOS'):
            return [movimiento for movimiento in movimientos if movimiento.cuenta == cuenta]
            
