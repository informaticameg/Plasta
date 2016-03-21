from plasta.gui.add_window import BaseAddWindow
from PyQt4 import uic
from os.path import join,abspath,dirname
from contacto import Contacto

class AddContacto( BaseAddWindow ):

    def __init__(self, unManager, itemaeditar = False, managers = []):
        BaseAddWindow.__init__(self, unManager, itemaeditar, managers)
        FILENAME = 'agregar.ui'
        uic.loadUi(join(abspath(dirname(__file__)),FILENAME), self)

        self.ITEMLIST = [
             {self.leNombre:Contacto.nombre},
             {self.leApellido:Contacto.apellido},
             {self.leNumero:Contacto.numero},
             {self.leEmail:Contacto.email},
        ]

        self._start_operations()
