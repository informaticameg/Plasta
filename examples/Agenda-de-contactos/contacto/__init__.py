from storm.locals import *


class Contacto (object):
    
    __storm_table__ = "contacto"

    # list of object attributes  
    ide = Int(primary = True)
    nombre = Unicode(allow_none = False)
    apellido = Unicode()
    numero = Unicode(allow_none = False)
    email = Unicode()
 
    
    def __init__(self, nombre, apellido, numero, email):
        self.nombre = nombre
        self.apellido = apellido
        self.numero = numero
        self.email = email
        
    def __str__(self):
        if self.apellido :
            return '%s, %s' % (self.nombre,self.apellido)
        else:
            return self.nombre
