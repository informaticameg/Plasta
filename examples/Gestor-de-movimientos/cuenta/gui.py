#!/usr/bin/env python
# -*- coding: utf-8 -*-
from plasta.gui import BaseGUI
from cuenta.add import AddCuenta
from cuenta import Cuenta
from PyQt4 import QtCore, QtGui


class CuentasGUI(BaseGUI):

    def __init__(self,manager, managers = []):
        BaseGUI.__init__(self, manager, managers)
        self.loadUI()

        self.addTableColumn(u' ', Cuenta.ide, alignment='C')
        self.addTableColumn(u'Nombre', Cuenta.nombre)
        self.addTableColumn(u'Tipo', Cuenta.tipo)
        self.addTableColumn(u'Descripcion', Cuenta.descripcion)

        self.DialogAddClass = AddCuenta

        self._start_operations()
        self.setWindowTitle('Cuentas')

    def _start_operations(self):
        self._makeTable()

    def _makeTable(self):
        if not self.ATRIBUTOSLISTA :
            columnasTablas = [p.capitalize() for p in self._get_attributes_names()]
        else:
            self.ATRIBUTOSLISTA_CLASSNAMES = [ self.manager.getAttributeName( p.values()[0] ) for p in self.ATRIBUTOSLISTA]
            columnasTablas = [p.keys()[0] for p in self.ATRIBUTOSLISTA]

    @QtCore.pyqtSlot()
    def on_btAgregar_clicked(self, postMethod = None):
        wAgregar = self.add()
        wAgregar.postSaveMethod = postMethod
        wAgregar.exec_()

    @QtCore.pyqtSlot()
    def on_btEditar_clicked(self, postMethod, obj):
        if obj:
            wEditar = self.edit(obj)
            wEditar.postSaveMethod = postMethod
            wEditar.exec_()

    @QtCore.pyqtSlot()
    def on_btEliminar_clicked(self, postMethod, obj):
        if obj:
            result = QtGui.QMessageBox.warning(self, u"Eliminar "+ self.manager.getClassName(),
                u"¿Esta seguro que desea eliminar?.\n\n",
                QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if result == QtGui.QMessageBox.Yes:
                self.delete(obj)
                postMethod()

