from storm.locals import *
from cuenta import Cuenta


class Movimiento (object):

    __storm_table__ = "Movimiento"

    ide = Int(primary = True)
    fecha = Date(allow_none = False)
    monto = Unicode(allow_none = False)
    descripcion = Unicode(allow_none = False)
    nroComprobante = Unicode()
    tipo = Unicode(allow_none = False)
    cuenta_id = Int()
    cuenta = Reference(cuenta_id, Cuenta.ide)    
    razon_social = Unicode()
    
    def __init__(self, unaCuenta, unMonto, unNrocomprobante, unDescripcion, unaFecha, unaRazonSocial, unTipo):
        if type(unaFecha) is unicode :
            from datetime import datetime
            self.fecha = datetime.strptime(unaFecha, '%d/%m/%Y')
        else:
            self.fecha = unaFecha
        self.monto = unMonto
        self.cuenta = unaCuenta
        self.descripcion = unDescripcion
        self.nroComprobante = unNrocomprobante
        self.tipo = unTipo
        self.razon_social = unaRazonSocial

