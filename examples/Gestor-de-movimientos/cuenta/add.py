from plasta.gui.add_window import BaseAddWindow
from PyQt4 import uic, QtCore
from os.path import join,abspath,dirname
from cuenta import Cuenta

class AddCuenta(BaseAddWindow):

    def __init__(self, manager, itemToEdit = False, managers = []):
        BaseAddWindow.__init__(self, manager, itemToEdit)
        uic.loadUi(join(abspath(dirname(__file__)),'add.ui'), self)

        self.ITEMLIST = [
            {self.leNombre:Cuenta.nombre},
            {self.teDescripcion:Cuenta.descripcion},
            {self.cbTipo:Cuenta.tipo}
        ]

        if manager :
            self._start_operations()
        self.leNombre.textEdited.connect(lambda text: self.leNombre.setText(text.toUpper()))

    @QtCore.pyqtSlot()
    def on_btSave_clicked(self):
        BaseAddWindow.on_btSave_clicked(self)
        self.leNombre.clear()
        self.teDescripcion.clear()
