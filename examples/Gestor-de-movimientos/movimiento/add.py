from plasta.gui.add import BaseAdd
from PyQt4 import QtCore
from movimiento import Movimiento
from datetime import datetime
from balance import Balance
from plasta.utils.qt import centerOnScreen


class AddMovimiento(BaseAdd):

    def __init__(self,manager, itemToEdit = False, managers = []):
        BaseAdd.__init__(self, manager, itemToEdit, managers)
        self.loadUI('movimiento/uis/add.ui')

        self.linkToAttribute(self.cbCuentas, Movimiento.cuenta)
        self.linkToAttribute(self.dsbMonto, Movimiento.monto)
        self.linkToAttribute(self.leNroComprobante, Movimiento.nroComprobante)
        self.linkToAttribute(self.teDescripcion, Movimiento.descripcion)
        self.linkToAttribute(self.deFecha, Movimiento.fecha)
        self.linkToAttribute(self.leRazonSocial, Movimiento.razon_social)

        self.cuentasManager = managers[0].manager
        self.balance = Balance()
        self._start_operations()

    # REIMPLEMENTED
    def _start_operations(self):
        centerOnScreen(self)
        self.setValidators()
        self.btSave.setDefault(True)
        if self.itemToEdit:
            self.btSave.setText('Editar')
            self.setWindowTitle(u'Editar Ingreso')
            self._loadDataInWidgets()
        else:
            self.setWindowTitle(u"Agregar Ingreso")
        #self.lbTitle.setText(self.windowTitle())

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
        BaseAdd.on_btSave_clicked(self)
        self.leRazonSocial.clear()
        self.dsbMonto.setValue(0)
        self.teDescripcion.clear()
        self.leNroComprobante.clear()

    # REIMPLEMENTED
    def save(self, listadedatos):
        # obtenemos el objeto cuenta
        unaCuenta = listadedatos[0]
        listadedatos[1] = unicode(str(listadedatos[1]),'utf-8')
        listadedatos.append( unaCuenta.tipo )
        self.balance.actualizar(float(listadedatos[1]), unaCuenta.tipo)
        return BaseAdd.save(self, listadedatos)

    def edit(self, listadedatos):
        BaseAdd.edit(self, listadedatos)

