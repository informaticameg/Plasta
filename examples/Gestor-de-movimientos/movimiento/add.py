from plasta.gui.add_window import BaseAddWindow
from PyQt4 import uic, QtCore
from os.path import join,abspath,dirname
from movimiento import Movimiento
from datetime import datetime
from balance import Balance

class AddMovimiento(BaseAddWindow):

    def __init__(self,manager, itemToEdit = False, managers = []):
        BaseAddWindow.__init__(self, manager, itemToEdit, managers)
        FILENAME = 'uis/add.ui'
        uic.loadUi(join(abspath(dirname(__file__)),FILENAME), self)

        self.ITEMLIST = [
            {self.cbCuentas:Movimiento.cuenta},
            {self.dsbMonto:Movimiento.monto},
            {self.leNroComprobante:Movimiento.nroComprobante},
            {self.teDescripcion:Movimiento.descripcion},
            {self.deFecha:Movimiento.fecha},
            {self.leRazonSocial:Movimiento.razon_social}
        ]
        self.cuentasManager = managers[0].manager
        self.balance = Balance()
        self._start_operations()

    # REIMPLEMENTED
    def _start_operations(self):
        self._centerOnScreen()
        self.setValidators()
        self.btSave.setDefault(True)
        if self.EDITITEM:
            self.btSave.setText('Editar')
            self.setWindowTitle(u'Editar Ingreso')
            self._loadDataInWidgets()
        else:
            self.setWindowTitle(u"Agregar Ingreso")
        self.lbTitulo.setText(self.windowTitle())

        self.deFecha.setDate( datetime.today() )

    @QtCore.pyqtSlot()
    def on_btAgregarCategoria_clicked(self):
        self.managers[0].on_btAgregar_clicked()
        try:
            self.cargarComboCuentas()
        except AttributeError :
            pass

    @QtCore.pyqtSlot()
    def on_rbIngreso_clicked(self):
        self.cbCuentas.clear()
        items = self.managers[0].manager.cuentasDeIngreso()
        nombres_cuentas = [cuenta.nombre for cuenta in items]
        nombres_cuentas.sort()
        [self.cbCuentas.addItem( nombre_cuenta ) for nombre_cuenta in nombres_cuentas ]

    @QtCore.pyqtSlot()
    def on_rbEgreso_clicked(self):
        self.cbCuentas.clear()
        items = self.managers[0].manager.cuentasDeEgreso()
        nombres_cuentas = [cuenta.nombre for cuenta in items]
        nombres_cuentas.sort()
        [self.cbCuentas.addItem( nombre_cuenta ) for nombre_cuenta in nombres_cuentas ]

    @QtCore.pyqtSlot()
    def on_btSave_clicked(self):
        BaseAddWindow.on_btSave_clicked(self)
        self.leRazonSocial.clear()
        self.dsbMonto.setValue(0)
        self.teDescripcion.clear()
        self.leNroComprobante.clear()

    # REIMPLEMENTED
    def save(self, listadedatos):
        # obtenemos el objeto cuenta
        print listadedatos
        unaCuenta = listadedatos[0]
        #listadedatos[0] = unaCuenta
        listadedatos[1] = unicode(str(listadedatos[1]),'utf-8')
        listadedatos.append( unaCuenta.tipo )
        self.balance.actualizar(float(listadedatos[1]), unaCuenta.tipo)
        return BaseAddWindow.save(self, listadedatos)

    def edit(self, listadedatos):
        BaseAddWindow.edit(self, listadedatos)

