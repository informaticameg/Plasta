#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import os
from PyQt4 import QtCore, QtGui, uic
import images_rc #@UnusedImport
from os.path import join,abspath,dirname
from movimiento.libro_diario import LibroDiarioGUI
from seccion.secciones_categorias_gui import SeccionesCategoriasGUI
from seccion.gui import SeccionesGUI
from cuenta.gui import CuentasGUI

from modulos import Modulos

class AllModules(QtGui.QMainWindow):
    
    def __init__(self, managers = None):
        FILENAME = 'all_modules.ui'
        QtGui.QMainWindow.__init__(self)
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        ICONFILE = join(abspath(dirname(__file__)),'images_rc/logo.png')              
        uic.loadUi(uifile, self)
        self.__centerOnScreen()
        self.setWindowTitle("Mi sistema")
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.close)
        
        self.managers = managers
       
        
    def __centerOnScreen (self):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))            
                
    @QtCore.pyqtSlot()
    def on_btLibroDiario_clicked(self):
        self.libro = LibroDiarioGUI(self.managers.movimientos, managers = [CuentasGUI(self.managers.cuentas)])
        self.libro.setWindowIcon( self.btLibroDiario.icon() )
        self.libro.show() 
           
    @QtCore.pyqtSlot()
    def on_btSecciones_clicked(self):
        self.secciones = SeccionesCategoriasGUI(
                    self.managers.secciones, 
                    managers = [
                                SeccionesGUI(self.managers.secciones, managers = [self.managers.cuentas]),
                                CuentasGUI(self.managers.cuentas)])
        self.secciones.setWindowIcon( self.btSecciones.icon() )
        self.secciones.show()
        
