#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import images_rc
from PyQt4 import QtCore, QtGui
from plasta.utils.qt import loadUI, centerOnScreen
from movimiento.libro_diario import LibroDiarioGUI
from seccion.secciones_categorias_gui import SeccionesCategoriasGUI
from seccion.gui import SeccionesGUI
from cuenta.gui import CuentasGUI

class MainWindow(QtGui.QMainWindow):

    def __init__(self, managers = None):
        QtGui.QMainWindow.__init__(self)
        loadUI(self, '/GUI/mainwindow.ui')
        centerOnScreen(self)
        self.setWindowTitle("Gestor de movimientos")
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.close)

        self.managers = managers

    def __centerOnScreen (self):
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    @QtCore.pyqtSlot()
    def on_btLibroDiario_clicked(self):
        self.libro = LibroDiarioGUI(self.managers.movimientos, managers = [CuentasGUI(self.managers.cuentas)])
        self.libro.setWindowIcon( self.btLibroDiario.icon() )
        self.libro.show()

    @QtCore.pyqtSlot()
    def on_btCuentas_clicked(self):
        self.secciones = SeccionesCategoriasGUI(
                    self.managers.secciones,
                    managers = [
                                SeccionesGUI(self.managers.secciones, managers = [self.managers.cuentas]),
                                CuentasGUI(self.managers.cuentas)])
        self.secciones.setWindowIcon( self.btCuentas.icon() )
        self.secciones.show()

