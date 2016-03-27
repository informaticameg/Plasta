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

    def __init__(self, cuenta, monto, nroComprobante, descripcion, fecha, razonSocial, tipo):
        if type(fecha) is unicode :
            from datetime import datetime
            self.fecha = datetime.strptime(fecha, '%d/%m/%Y')
        else:
            self.fecha = fecha
        self.monto = monto
        self.cuenta = cuenta
        self.descripcion = descripcion
        self.nroComprobante = nroComprobante
        self.tipo = tipo
        self.razon_social = razonSocial

