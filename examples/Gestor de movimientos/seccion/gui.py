#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from PyQt4 import QtCore, uic, QtGui
#from os.path import join,abspath,dirname
from seccion.add import AddSeccion
from seccion import Seccion

class SeccionesGUI(BaseGUI):
    """La ventana principal de la aplicación."""
    
    def __init__(self,manager, managers = []):
        BaseGUI.__init__(self, manager, managers)
        self.ATRIBUTOSLISTA = [
        {u' ':Seccion.ide},
        {u'Nombre':Seccion.nombre}] 
        self.MyTabla = None         
        self.DialogAddClass = AddSeccion#la clase que invoca a los dialogos de agregar y editar
        self.cuentasManager = managers[0]
        self._operaciones_de_inicio()
        
    def _operaciones_de_inicio(self):
        u'''
        operaciones necesarias para levantar las ventanas
        '''
        self._makeTable()
        
    def _makeTable(self):
        if not self.ATRIBUTOSLISTA :
            columnasTablas = [p.capitalize() for p in self._obtener_atributos_names()]
        else:
            self.ATRIBUTOSLISTA_CLASSNAMES = [ self.manager.obtenerNombreAtributo( p.values()[0] ) for p in self.ATRIBUTOSLISTA]
            listadeobjetosseleccionados = [p.keys()[0] for p in self.ATRIBUTOSLISTA]
    
    #REIMPLEMENTED
    def eliminar(self, obj):        
        self.manager.delete(obj)
        cuentas = self.obtenerCuentasDeLaSeccionSeleccionada()
        self.cuentasManager.establecerSeccion(cuentas, None)
        
    def obtenerCuentasDeLaSeccionSeleccionada(self):
        if self.actual_rows_to_objects() :
            unaSeccion = self.actual_rows_to_objects()[0]        
            return self.manager.obtenerCuentas( unaSeccion )
    
    @QtCore.pyqtSlot()
    def on_btAgregar_clicked(self, postMethod):
        wAgregar = self.agregar()        
        wAgregar.postSaveMethod = postMethod
        wAgregar.exec_()

    @QtCore.pyqtSlot()
    def on_btEditar_clicked(self, postMethod):
        listadeobjetosseleccionados = self.actual_rows_to_objects()
        if listadeobjetosseleccionados:
            for obj in listadeobjetosseleccionados:
                wEditar = self.editar(obj)
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
                    self.eliminar(obj)            
                    
    def on_twDatosSeccion_itemSelectionChanged(self, metodo_a_ejecutar):
        metodo_a_ejecutar()
        
