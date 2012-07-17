from plasta.gui.add_window import BaseAddWindow
from PyQt4 import uic, QtCore
from os.path import join,abspath,dirname 
from cuenta import Cuenta

class AddCuenta(BaseAddWindow):

    def __init__(self,unManager,itemaeditar = False, managers = []):
        BaseAddWindow.__init__(self, unManager, itemaeditar)
        FILENAME = 'agregar.ui'
        uic.loadUi(join(abspath(dirname(__file__)),FILENAME), self)
        
        self.ITEMLIST = [{self.leNombre:Cuenta.nombre},
                         {self.teDescripcion:Cuenta.descripcion},
                         {self.cbTipo:Cuenta.tipo}]
        
        if unManager : self._start_operations()        
        self.leNombre.textEdited.connect(lambda text: self.leNombre.setText(text.toUpper()))        
        self.lbTitulo.setText('Agregar Cuenta')
        
    @QtCore.pyqtSlot()
    def on_btGuardar_clicked(self):
        BaseAddWindow.on_btGuardar_clicked(self)
        self.leNombre.clear()
        self.teDescripcion.clear()
