from storm.locals import *


class Seccion (object):
    
    __storm_table__ = "Seccion"

    ide = Int(primary = True)
    nombre = Unicode(allow_none = True)    

    def __init__(self,  unNombre):
        self.nombre = unNombre        
