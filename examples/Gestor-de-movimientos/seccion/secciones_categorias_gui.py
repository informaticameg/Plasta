#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from PyQt4 import QtCore, uic , QtGui
from os.path import join,abspath,dirname
from plasta.gui.mytablewidget import MyTableWidget
# from plasta.gui.uis import images_rc

from GUI.TreeView import TreeView


class SeccionesCategoriasGUI(BaseGUI):

    def __init__(self,manager, managers = []):
        BaseGUI.__init__(self, manager, managers)
        self.FILENAME = join(abspath(dirname(__file__)),'secciones.ui')

        self.managerSecciones = managers[0].manager
        self.managerCuentas = managers[1].manager
        self.SeccionesGUI = managers[0]
        self.CategoriasGUI = managers[1]
        self._start_operations()

    def _start_operations(self):
        uic.loadUi(self.FILENAME, self)
        self.setWindowTitle(u"Categorías")
        self.loadShortcuts()
        self.fullScreen = False
        self.centerOnScreen()

        self.SeccionesGUI.DialogAddClass.postSaveMethod = self.recargarListaSecciones

        #self._makeTableSecciones()
        self._makeTreeCuentas()
        #self._makeTablaCuentasEnSecciones()

        #self.cargarTablaSecciones()
        self.cargarTreeCuentas()

#===============================================================================
# Metodos reimplementados : SECCIONES
#===============================================================================

    def _makeTableSecciones(self):
        if not self.ATRIBUTOSLISTA :
            columnasTablas = [p.capitalize() for p in self.SeccionesGUI._obtener_atributos_names()]
        else:
            self.ATRIBUTOSLISTA_CLASSNAMES = [ self.SeccionesGUI.manager.obtenerNombreAtributo( p.values()[0] ) for p in self.ATRIBUTOSLISTA]
            columnasTablas = [p.keys()[0] for p in self.ATRIBUTOSLISTA]

        self.SeccionesGUI.MyTabla = MyTableWidget(self.twDatosSeccion,columnasTablas)

    def _makeTablaCuentasEnSecciones(self):
        self.MyTablaCuentasSecciones = MyTableWidget(self.twDatosSeccionCategoria,["Cuenta"])

    def cargarTablaSecciones(self,listadeobj = None):
        '''
        carga la lista de objetos en la tabla
        @param listadeobj:if none carga todos, sino lo de la lista
        '''
        if listadeobj == None:
            listadeobj = self.managerSecciones.getall()
        listadefilas = [self.SeccionesGUI._obtenerValoresAtributos(obj) for obj in listadeobj]
        self.SeccionesGUI.MyTabla.addItems(listadefilas)
        self.lbCantidadItemsSeccion.setText( str(len(listadefilas)) + ' items(s) seleccionado(s)')

    def recargarListaSecciones(self):
        valor = ''
        campo = ''
        if self.ATRI_COMBO_BUSQUEDA :
            campo = [p[campo] for p in self.ATRI_COMBO_BUSQUEDA if campo in p ][0]
        else:
            if campo != '' : campo = self._obtaincolumnforname(campo)
        resultado = self.SeccionesGUI.search(campo,valor)
        self.cargarTablaSecciones(resultado)

    def cargarTablaCuentasEnUnaSeccion(self):
        cuentas = self.SeccionesGUI.obtenerCuentasDeLaSeccionSeleccionada()
        if cuentas :
            self.MyTablaCuentasSecciones.addItems( [[cuenta.nombre] for cuenta in cuentas] )

    @QtCore.pyqtSlot()
    def on_btAgregarSeccion_clicked(self):
        if len(self.managerCuentas.getall()) > 1 :
            self.SeccionesGUI.on_btAgregar_clicked( self.recargarListaSecciones )
        else:
            QtGui.QMessageBox.warning(self, "Agregar Seccion",u"Deben existir mas de <1> cuenta(s) para poder crear una sección.")

    @QtCore.pyqtSlot()
    def on_btEditarSeccion_clicked(self):
        self.SeccionesGUI.on_btEditar_clicked( self.recargarListaSecciones )

    @QtCore.pyqtSlot()
    def on_btEliminarSeccion_clicked(self):
        self.SeccionesGUI.on_btEliminar_clicked()
        self.recargarListaSecciones()
        self.MyTablaCuentasSecciones.fullClear()

    def on_twDatosSeccion_itemSelectionChanged(self):
        self.SeccionesGUI.on_twDatosSeccion_itemSelectionChanged( self.cargarTablaCuentasEnUnaSeccion )

#===============================================================================
# Metodos reimplementados : CUENTAS
#===============================================================================

    def _makeTreeCuentas(self):
        self.treeCuentas = TreeView(
            self.treeCuentas,
            self.connect,
            self.on_treeCuentas_selectedItem,
            QtGui.QIcon(':/newPrefix/Book.png'),
            QtGui.QIcon(':/newPrefix/kwikdisk.png'))

    def cargarTreeCuentas(self,listadeobj = None):
        '''
        carga la lista de objetos en la tabla
        @param listadeobj:if none carga todos, sino lo de la lista
        '''
        if listadeobj == None:
            listadeobj = self.managerCuentas.getall()

        listadefilas = [self.CategoriasGUI._getAttributesValues(obj) for obj in listadeobj]
        cuentas_ingresos, cuentas_egresos, items = [], [], []
        for fila in listadefilas :
            if fila[2] == u'Ingreso' :
                cuentas_ingresos.append( fila[1] )
            else:
                cuentas_egresos.append( fila[1] )

        cuentas_ingresos.sort()
        cuentas_egresos.sort()
        map(lambda item: items.append( [u'CUENTAS DE INGRESOS',item] ), cuentas_ingresos)
        map(lambda item: items.append( [u'CUENTAS DE EGRESOS',item] ), cuentas_egresos)
        self.treeCuentas.addItems(items)
        self.treeCuentas.widget.expandAll()
        self.lbCantidadItemsCategoria.setText( str(len(items)) + ' items(s) seleccionado(s)')

    def recargarListaCuentas(self):
        valor = ''
        campo = ''
        resultado = self.CategoriasGUI.search(campo,valor)
        self.cargarTreeCuentas(resultado)

    @QtCore.pyqtSlot()
    def on_btAgregarCategoria_clicked(self):
        self.CategoriasGUI.on_btAgregar_clicked( self.cargarTreeCuentas )

    @QtCore.pyqtSlot()
    def on_btEditarCategoria_clicked(self):
        try:
            cuenta = self.CategoriasGUI.manager.get( self.hijo )[0]
            self.CategoriasGUI.on_btEditar_clicked( self.cargarTreeCuentas, cuenta)
        except:
            pass


    @QtCore.pyqtSlot()
    def on_btEliminarCategoria_clicked(self):
        try:
            cuenta = self.CategoriasGUI.manager.get( self.hijo )[0]
            self.CategoriasGUI.on_btEliminar_clicked( self.cargarTreeCuentas , cuenta)
        except:
            pass

    @QtCore.pyqtSlot(int)
    def on_cbFiltro_currentIndexChanged(self , index):
        filtro = unicode(self.cbFiltro.itemText(self.cbFiltro.currentIndex()).toUtf8(),'utf-8')
        cuentas = None
        if filtro == "Todos" :
            cuentas = self.managerCuentas.getall()
        elif filtro == "Ingreso" :
            cuentas = self.managerCuentas.cuentasDeIngreso()
        elif filtro == "Egreso" :
            cuentas = self.managerCuentas.cuentasDeEgreso()
        self.cargarTreeCuentas( cuentas )

    def on_treeCuentas_selectedItem(self,indice,b):
        if indice.parent().row() != -1:
            self.padre =  unicode(indice.parent().data().toString().toUtf8(),'utf-8')
            self.hijo =  unicode(indice.data().toString().toUtf8(),'utf-8')


