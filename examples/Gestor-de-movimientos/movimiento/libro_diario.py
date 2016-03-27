#!/usr/bin/env python
# -*- coding: utf-8 -*-
import locale
from plasta.gui import BaseGUI
from movimiento import Movimiento
from os.path import join,abspath,dirname
from PyQt4 import uic, QtCore, QtGui
from datetime import datetime
from movimiento.add import AddMovimiento
from balance import Balance


class LibroDiarioGUI(BaseGUI):

    def __init__(self,manager, managers = []):
        BaseGUI.__init__(self, manager, managers)
        self.FILENAME = join(abspath(dirname(__file__)),'uis/libro_diario.ui')

        self.DialogAddClass  = AddMovimiento
        self.ALINEACIONLISTA = ['C','L','L','L','R']

        self.ATRIBUTOSLISTA = [
            {u'Fecha':Movimiento.fecha},
            {u'Razon Social':Movimiento.razon_social},
            {u'Descripcion':Movimiento.descripcion},
            {u'Cuenta':Movimiento.cuenta},
            {u'Monto':Movimiento.monto}
        ]

        self.cuentasManager = managers[0].manager
        self.balance = Balance()
        locale.setlocale( locale.LC_ALL, '' )
        self._start_operations()

#===============================================================================
# LOGICA GUI Y EXTRAS
#===============================================================================

    def _obtenerValoresAtributos(self,obj):
        resultado = []
        atributos_objeto = self.manager.getClassAttributesValues(obj)
        if not self.ATRIBUTOSLISTA :
            return atributos_objeto
        else:
            atributos_clase = self.manager.getClassAttributes()
            atributos_ordenados = self.ATRIBUTOSLISTA_CLASSNAMES
            for atributo in atributos_ordenados:
                resultado.append( atributos_objeto[ atributos_clase.index( atributo ) ] )
            # formatea la fecha, de date -> str
            resultado[0] = resultado[0].strftime("%d/%m/%Y")
            # formatear el monto
            monto = locale.currency(float(resultado[4]), grouping = True)
            resultado[4] = unicode( monto )
            return resultado

    def _start_operations(self):
        u'''
        operaciones necesarias para levantar las ventanas
        '''
        uic.loadUi(self.FILENAME, self)
        self.setWindowTitle(self.TITULO)
        self._makeTable()

        self.loadTable()
        self._loadAppShortcuts()
        self.fullScreen = False

        self._centerOnScreen()

        self.deFechaMostradaDesde.setDate( datetime.today() )
        self.deFechaMostradaHasta.setDate( datetime.today() )
        self.cbTipoMovimiento.setCurrentIndex(1)
        self.cbTipoMovimiento.setCurrentIndex(0)
        self.cbCuentas.setCurrentIndex(0)

        self.actualizarLabelBalance()
        self.setWindowTitle("Libro Diario")

    def reloadList(self):
        desde = self.deFechaMostradaDesde.date().toPyDate()
        hasta = self.deFechaMostradaHasta.date().toPyDate()
        filtro = self.obtenerTipoMovimientoSeleccionado()
        cuenta = self.obtenerCuentaSeleccionada()
        movimientos = self.manager.obtenerMovimientosDesdeHasta(desde, hasta, filtro, cuenta)
        self.loadTable(movimientos)
        self.actualizarLabelBalance()

    def loadTable(self,listadeobj = None):
        if listadeobj == None:
            listadeobj = self.manager.getall()
        listadefilas = [self._obtenerValoresAtributos(obj) for obj in listadeobj]
        self.MyTabla.addItems(listadefilas)

    def obtenerTipoMovimientoSeleccionado(self):
        return unicode(self.cbTipoMovimiento.itemText(self.cbTipoMovimiento.currentIndex()).toUtf8(), 'utf-8')

    def obtenerCuentaSeleccionada(self):
        return unicode(self.cbCuentas.itemText(self.cbCuentas.currentIndex()).toUtf8(), 'utf-8')

    def cargarComboCuentas(self):
        filtro = self.obtenerTipoMovimientoSeleccionado()
        items = None
        if filtro == u'TODOS':
            items = self.cuentasManager.getall()
        elif filtro == u'INGRESOS':
            items = self.cuentasManager.cuentasDeIngreso()
        elif filtro == u'EGRESOS':
            items = self.cuentasManager.cuentasDeEgreso()

        self.cbCuentas.clear()
        self.cbCuentas.addItem("TODOS")
        nombres_cuentas = [cuenta.nombre for cuenta in items]
        nombres_cuentas.sort()
        [self.cbCuentas.addItem( nombre_cuenta ) for nombre_cuenta in nombres_cuentas ]

    def establecerMontoBalance(self, monto):
        style = '''QLabel {
        color: black;
        background-color: #BFBFBF;
        font: bold 18px;
        font-family: Ubuntu, Helvetica, sans-serif;
        border: 1px solid #BFBFBF;
        border-top-left-radius: 0px;border-top-right-radius: 0px;border-bottom-right-radius: 6px;border-bottom-left-radius: 6px;
        }'''
        self.lbBalance.setText( str(locale.currency( float(monto), grouping = True)) )
        if monto == 0 :
            self.lbBalance.setText("$ 00,00")
            self.lbBalance.setStyleSheet(style)
        elif monto > 0 :
            self.lbBalance.setStyleSheet( style.replace("color: black;","color: green;"))
        elif monto < 0 :
            self.lbBalance.setStyleSheet( style.replace("color: black;","color: red;"))

    def actualizarLabelBalance(self):
        self.establecerMontoBalance( self.balance.valor() )

#===============================================================================
# MOTODOS DE LAS SEÑALES
#===============================================================================

    @QtCore.pyqtSlot(int)
    def on_cbTipoMovimiento_currentIndexChanged(self , index):
        self.cargarComboCuentas()

    @QtCore.pyqtSlot(int)
    def on_cbCuentas_currentIndexChanged(self , index):
        self.reloadList()

    def on_deFechaMostradaDesde_dateChanged(self , date):
        if self.isVisible() :
            if date > self.deFechaMostradaHasta.date() :
                QtGui.QMessageBox.information(self, "Libro diario","La fecha <Desde> no puede ser mayor a <Hasta>.")
                self.deFechaMostradaDesde.setDate( datetime.today() )
            else:
                self.reloadList()

    def on_deFechaMostradaHasta_dateChanged(self , date):
        if self.isVisible() :
            if date < self.deFechaMostradaDesde.date() :
                QtGui.QMessageBox.information(self, "Libro diario","La fecha <Hasta> no puede ser mayor a <Desde>.")
                self.deFechaMostradaHasta.setDate( datetime.today() )
            else:
                self.reloadList()

