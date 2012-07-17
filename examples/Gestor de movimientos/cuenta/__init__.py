from storm.locals import *


class Cuenta (object):
    
    __storm_table__ = "Cuentas"

    ide = Int(primary = True)
    nombre = Unicode()
    descripcion = Unicode()
    monto = Unicode()
    tipo = Unicode()
    
    def __init__(self,  unNombre, unaDescripcion, unTipo):
        self.nombre = unNombre
        self.descripcion = unaDescripcion
        self.tipo = unTipo
        
    def __str__(self):
        return self.nombre
    
