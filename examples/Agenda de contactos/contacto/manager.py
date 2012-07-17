from plasta.logic.manager import BaseManager
from contacto import Contacto

class ContactosManager( BaseManager ):
    
    def __init__(self, store, reset = False ):        
        BaseManager.__init__(self, store, reset)
        self.CLASS = Contacto
        self._start_operations()
