#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from PyQt4 import QtCore, uic, QtGui
from seccion.add import AddSeccion
from seccion import Seccion

class SeccionesGUI(BaseGUI):

    def __init__(self,manager, managers = []):
        BaseGUI.__init__(self, manager, managers)
        self.loadUI()

        self.ATRIBUTOSLISTA = [
            {u' ':Seccion.ide},
            {u'Nombre':Seccion.nombre}
        ]
        self.MyTabla = None
        self.DialogAddClass = AddSeccion#la clase que invoca a los dialogos de agregar y editar
        self.cuentasManager = managers[0]

        self._start_operations()

    def _start_operations(self):
        u'''
        operaciones necesarias para levantar las ventanas
        '''
        self._makeTable()

    def _makeTable(self):
        if not self.ATRIBUTOSLISTA :
            columnasTablas = [p.capitalize() for p in self._obtener_atributos_names()]
        else:
            self.ATRIBUTOSLISTA_CLASSNAMES = [ self.manager.getAttributeName( p.values()[0] ) for p in self.ATRIBUTOSLISTA]
            listadeobjetosseleccionados = [p.keys()[0] for p in self.ATRIBUTOSLISTA]

    #REIMPLEMENTED
    def delete(self, obj):
        self.manager.delete(obj)
        cuentas = self.obtenerCuentasDeLaSeccionSeleccionada()
        self.cuentasManager.establecerSeccion(cuentas, None)

    def obtenerCuentasDeLaSeccionSeleccionada(self):
        if self.actual_rows_to_objects() :
            unaSeccion = self.actual_rows_to_objects()[0]
            return self.manager.obtenerCuentas( unaSeccion )

    @QtCore.pyqtSlot()
    def on_btAgregar_clicked(self, postMethod):
        wAgregar = self.add()
        wAgregar.postSaveMethod = postMethod
        wAgregar.exec_()

    @QtCore.pyqtSlot()
    def on_btEditar_clicked(self, postMethod):
        listadeobjetosseleccionados = self.actual_rows_to_objects()
        if listadeobjetosseleccionados:
            for obj in listadeobjetosseleccionados:
                wEditar = self.edit(obj)
                wEditar.postSaveMethod = postMethod
                wEditar.exec_()

    @QtCore.pyqtSlot()
    def on_btEliminar_clicked(self):
        listadeobjetosseleccionados = self.actual_rows_to_objects()
        if listadeobjetosseleccionados:
            for obj in listadeobjetosseleccionados:
                result = QtGui.QMessageBox.warning(self, u"Eliminar "+ self.manager.getClassName(),
                    u"¿Esta seguro que desea eliminar?.\n\n",
                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if result == QtGui.QMessageBox.Yes:
                    self.delete(obj)

    def on_twDatosSeccion_itemSelectionChanged(self, metodo_a_ejecutar):
        metodo_a_ejecutar()