from plasta.gui.add import BaseAdd
from PyQt4 import uic, QtCore
from os.path import join,abspath,dirname
from cuenta import Cuenta

class AddCuenta(BaseAdd):

    def __init__(self, manager, itemToEdit = False, managers = []):
        BaseAdd.__init__(self, manager, itemToEdit)
        self.loadUI('cuenta/add.ui')

        self.linkToAttribute(self.leNombre, Cuenta.nombre)
        self.linkToAttribute(self.teDescripcion, Cuenta.descripcion)
        self.linkToAttribute(self.cbTipo, Cuenta.tipo)

        if manager :
            self._start_operations()
        self.leNombre.textEdited.connect(lambda text: self.leNombre.setText(text.toUpper()))

    @QtCore.pyqtSlot()
    def on_btSave_clicked(self):
        BaseAdd.on_btSave_clicked(self)
        self.leNombre.clear()
        self.teDescripcion.clear()
