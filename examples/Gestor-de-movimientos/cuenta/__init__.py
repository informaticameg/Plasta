from storm.locals import *


class Cuenta (object):

    __storm_table__ = "Cuentas"

    ide = Int(primary = True)
    nombre = Unicode()
    descripcion = Unicode()
    monto = Unicode()
    tipo = Unicode()

    def __init__(self,  nombre, descripcion, tipo):
        self.nombre = nombre
        self.descripcion = descripcion
        self.tipo = tipo

    def __str__(self):
        return self.nombre

