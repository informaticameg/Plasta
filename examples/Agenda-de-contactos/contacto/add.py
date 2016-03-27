from plasta.gui.add import BaseAdd
from PyQt4 import uic
from os.path import join,abspath,dirname
from contacto import Contacto

class AddContacto( BaseAdd ):

    def __init__(self, unManager, itemaeditar = False, managers = []):
        BaseAdd.__init__(self, unManager, itemaeditar, managers)
        FILENAME = 'add.ui'
        uic.loadUi(join(abspath(dirname(__file__)),FILENAME), self)

        self.ITEMLIST = [
             {self.leNombre:Contacto.nombre},
             {self.leApellido:Contacto.apellido},
             {self.leNumero:Contacto.numero},
             {self.leEmail:Contacto.email},
        ]

        self._start_operations()
