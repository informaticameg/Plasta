from plasta.gui.add import BaseAdd
from PyQt4 import uic
from os.path import join, abspath, dirname
from contacto import Contacto

class AddContacto( BaseAdd ):

    def __init__(self, manager, itemToEdit = False, managers = []):
        BaseAdd.__init__(self, manager, itemToEdit, managers)
        self.loadUI(join(abspath(dirname(__file__)),'add.ui'))

        self.linkToAttribute(self.leNombre, Contacto.nombre)
        self.linkToAttribute(self.leApellido, Contacto.apellido)
        self.linkToAttribute(self.leNumero, Contacto.numero)
        self.linkToAttribute(self.leEmail, Contacto.email)

        self._start_operations()
