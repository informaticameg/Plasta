#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from plasta.utils.qt import centerOnScreen
from movimiento import Movimiento
from PyQt4 import QtCore, QtGui
from datetime import datetime
from movimiento.add import AddMovimiento
from balance import Balance


class LibroDiarioGUI(BaseGUI):

    def __init__(self,manager, managers = []):
        BaseGUI.__init__(self, manager, managers)
        self.DialogAddClass  = AddMovimiento
        self.loadUI('movimiento/uis/libro_diario.ui')

        self.addTableColumn(u'Fecha', Movimiento.fecha, alignment='C', fnParse=self.parseFecha)
        self.addTableColumn(u'Razon Social', Movimiento.razon_social)
        self.addTableColumn(u'Descripcion', Movimiento.descripcion)
        self.addTableColumn(u'Cuenta', Movimiento.cuenta)
        self.addTableColumn(u'Monto', Movimiento.monto, alignment='R', fnParse=self.parseMonto)

        self.cuentasManager = managers[0].manager
        self.balance = Balance()
        self._start_operations()

#===============================================================================
# LOGICA GUI Y EXTRAS
#===============================================================================

    def parseFecha(self, row, value):
        return value.strftime("%d/%m/%Y")

    def parseMonto(self, row, value):
        return "$ %8.2f" % float(value)

    def _start_operations(self):
        u'''
        operaciones necesarias para levantar las ventanas
        '''
        self.setWindowTitle(self.pluralTitle)
        self.makeTable()
        self.loadTable()
        self.loadShortcuts()
        self.fullScreen = False

        centerOnScreen(self)
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
        listadefilas = [self._getAttributesValues(obj) for obj in listadeobj]
        self.tableItems.addItems(listadefilas)

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
        self.lbBalance.setText( "$ %8.2f" % float(monto))
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

    def on_twItems_itemSelectionChanged(self):
        pass