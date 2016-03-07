#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Informática MEG <contacto@informaticameg.com>
#
# Written by 
#       Copyright 2012 Fernandez, Emiliano <emilianohfernandez@gmail.com>
#       Copyright 2012 Ferreyra, Jonathan <jalejandroferreyra@gmail.com>
#
# Plasta is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of
# the License, or (at your option) any later version.
#
# Plasta is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from os.path import join, abspath, dirname
from PyQt4 import QtCore, QtGui, uic
from plasta.gui.mytablewidget import MyTableWidget
from plasta.tools import pathtools
import uis.images_rc

class BaseGUI( QtGui.QMainWindow ):
    '''
    Clase base para el manejo de las operaciones de la pantalla ABM
    '''

    def __init__(self, manager, managers = None, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        # nombre del archivo ui de la interfaz
        self.FILENAME = join(abspath(dirname(__file__)),'uis/list.ui')
        # nombre del archivo del icono para la ventana
        ICONFILE = ''

        self.setWindowIcon( QtGui.QIcon( QtGui.QPixmap( join( abspath( dirname( __file__ ) ), ICONFILE ) ) ) )#
        self.manager = manager
        self.managers = managers
        
        # ATRIBUTOSLISTA: lista de diccionarios donde puedes indicar el orden y formato
        # en que se deben mostrar los atributos en la lista. Siendo la clave del diccionario, 
        # el texto en Unicode del texto que tendra la cabecera de la columna. Y el valor contenido
        # en el mismo elemento, el atributo de la clase que se mostrara en esa columna
        # Ejemplo:
        # self.ATRIBUTOSLISTA = [
        #    {u'Nombres':Cliente.Nombres},                    
        #    {u'Domicilio':Cliente.Domicilio}] 
        self.ATRIBUTOSLISTA = None
        # ATRI_COMBO_BUSQUEDA: lista de diccionarios donde puedes indicar el orden de como
        # quieres que se muestren y vean los atributos en el combo de los filtros
        # El formato es el mismo que <ATRIBUTOSLISTA>
        self.ATRI_COMBO_BUSQUEDA = []#el orden y la cantidad de atributos en str que quieras

        self.ALINEACIONLISTA = []#la alinecion de cada atributo en la fila
        # DialogAddClass: referencia a la clase que se instanciara para manejar la
        # ventana del dialogo abrir/editar
        self.DialogAddClass = None
        self.TITULO = self.manager.getClassName()
        self.pluralTitle = self.manager.getClassName()

    def _start_operations( self ):
        u'''
        Operaciones necesarias para levantar las ventanas
        '''
        uic.loadUi( self.FILENAME, self )
        self.setWindowTitle( self.TITULO )
        self.lbTitulo.setText( self.manager.getClassName() )
        self._makeTable()
        
        self.loadCombobox()
        self.loadTable()
        self._loadAppShortcuts()
        self.fullScreen = False
        
        self._centerOnScreen()
        self.btEditar.setVisible(False)
        self.btEliminar.setVisible(False)
        self.lbTitulo.setText(self.pluralTitle)
        self.setWindowTitle(self.pluralTitle)

    def _toogleFullScreen( self ):
        ''' '''
        if not self.fullScreen :
            self.showFullScreen()
        else:
            self.showNormal()
        self.fullScreen = not self.fullScreen

    def _loadAppShortcuts( self ):
        u""" Load shortcuts used in the application. """
        self._atajo_salir = QtGui.QShortcut( QtGui.QKeySequence( "Ctrl+Q" ), self, self.close )
        self._atajo_fullscreen = QtGui.QShortcut( QtGui.QKeySequence( "F11" ), self, self._toogleFullScreen )
        QtGui.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_Escape ), self, self.close )
        
        QtGui.QShortcut( QtGui.QKeySequence( QtCore.Qt.CTRL | QtCore.Qt.Key_N ), self, self.on_btAgregar_clicked )
        QtGui.QShortcut( QtGui.QKeySequence( QtCore.Qt.CTRL | QtCore.Qt.Key_M ), self, self.on_btEditar_clicked )
        QtGui.QShortcut( QtGui.QKeySequence( "Del" ), self, self.on_btEliminar_clicked )
        
    def _get_attributes_names( self ):
        '''
        Obtiene los atributos de la clase que maneja self.manager
        '''
        return self.ATRIBUTOSLISTA_CLASSNAMES if self.ATRIBUTOSLISTA else self.manager.getClassAttributes()
        
    def _makeTable( self ):
        '''
        Crea la estructura de la tabla ( columnas )
        '''
        if not self.ATRIBUTOSLISTA :
            columnasTablas = [p.capitalize() for p in self._get_attributes_names()]
        else:
            self.ATRIBUTOSLISTA_CLASSNAMES = [ self.manager.getAttributeName( p.values()[0] ) for p in self.ATRIBUTOSLISTA]
            columnasTablas = [p.keys()[0] for p in self.ATRIBUTOSLISTA]

        self.MyTabla = MyTableWidget( self.twDatos, columnasTablas, self.ALINEACIONLISTA)
        # conecta el menu contextual a la tabla
        self.connect( self.MyTabla.widget, QtCore.SIGNAL( 'customContextMenuRequested(const QPoint&)' ), self.on_context_menu )
 
    def _getAttributesValues( self, obj ):
        '''
        Devuelve en una lista los atributos de un objetos, ordenados 
        segun lo indicado en self.ATRIBUTOSLISTA
        '''
        
        resultado = []
        atributos_objeto = self.manager.getClassAttributesValues( obj )
        if not self.ATRIBUTOSLISTA :            
            return atributos_objeto
        else:
            atributos_clase = self.manager.getClassAttributes()
            atributos_ordenados = self.ATRIBUTOSLISTA_CLASSNAMES
            for atributo in atributos_ordenados:
                resultado.append( atributos_objeto[ atributos_clase.index( atributo ) ] )
            return resultado
    
    def _obtainColumnForName(self, columnname):
        '''
        A partir de un string obtiene la columna de storm
        @param columnname:nombre del atributo en str
        @return: 
        '''
        #MAGIC###################
        busqueda = self.manager.CLASS.__dict__[columnname]
        if str( type( busqueda ) ) != "<class 'storm.references.Reference'>" :
            try:
                campo = self.manager.CLASS.__dict__['_storm_columns'][busqueda]
            except:
                print "no tengo idea del error gui-_obtainColumnForName"
                campo = busqueda
        else:
            campo = busqueda
        #END MAGIC###############
        return campo

    def _find( self ):
        '''
        Reliza la busqueda y carga la tabla
        '''
        # obtiene el valor cargado en la barra de busqueda
        valor = unicode(self.leBusqueda.text().toUtf8(),'utf-8')
        # carga la lista segun el estado de la barra de busqueda
        self.reloadList() if valor != u'' else self.loadTable()

    def _setSearchColor(self, widget, resultados_busqueda):
        color_rojo = 'background-color: rgb(255, 178, 178);'
        try:
            if self.myStyleSheetBlanco == '' :
                if not widget.styleSheet().isEmpty() :
                    style = widget.styleSheet()
                    self.myStyleSheetBlanco = widget.styleSheet()

                    pos1 = style.indexOf( 'QLineEdit' )
                    pos2 = style.indexOf( '}', pos1 )
                    style = style.replace( pos2, 1, color_rojo + '}' )
                    self.myStyleSheetRojo = style
                else:
                    self.myStyleSheetRojo = color_rojo

            if not widget.text().isEmpty() :
                if len( resultados_busqueda ) == 0 :
                    widget.setStyleSheet( self.myStyleSheetRojo )
                else:
                    widget.setStyleSheet( self.myStyleSheetBlanco )
            else:
                widget.setStyleSheet( self.myStyleSheetBlanco )
        except:
            self.myStyleSheetBlanco = ''
            self.myStyleSheetRojo = ''
            self._setSearchColor( widget, resultados_busqueda )

    def reloadList( self ):
        '''
        Vuelve a cargar la lista a partir de los valores actuales en 
        la barra de busqueda y el filtro seleccionado.
        '''        
        valor = unicode( self.leBusqueda.text().toUtf8(), 'utf-8' )
        campo = unicode( self.cbCampos.itemText( 
                    self.cbCampos.currentIndex() ).toUtf8() )    
        if self.ATRI_COMBO_BUSQUEDA :
            campo = [p[campo] for p in self.ATRI_COMBO_BUSQUEDA if campo in p ][0]
        else:
            campo = self._obtainColumnForName( campo )     
        resultado = self.search( campo, valor )
        self.loadTable( resultado )
        self._setSearchColor( self.leBusqueda, resultado )
        
    def loadCombobox( self ):
        '''
        Carga el combobox de campos
        '''
        self.cbCampos.clear()
        if not self.ATRI_COMBO_BUSQUEDA :
            atributos = self.manager.getClassAttributes()
            for atributo in atributos:
                self.ATRI_COMBO_BUSQUEDA.append( {atributo:self._obtainColumnForName( atributo )} )
        map( self.cbCampos.addItem, [p.keys()[0] for p in self.ATRI_COMBO_BUSQUEDA] )
            
    def loadTable( self, listadeobj = None ):
        '''
        Carga la lista de objetos en la tabla
        @param listadeobj:if none carga todos, sino lo de la lista
        '''        
        if listadeobj == None:            
            listadeobj = self.manager.getall()
        listadefilas = [self._getAttributesValues( obj ) for obj in listadeobj]
        self.MyTabla.addItems( listadefilas )
        self.setItemsCount( len( listadeobj ) )
        
    def search( self, camponame, valor ):
        '''
        @param camponame:el nombre del campo en string
        @param valor:el valor de el campo(soporta los tipos de datos de searchBy)
        @return: lista de obj
        '''
        return self.manager.searchBy( camponame, valor )

    def on_context_menu( self, point ):
        mypoint = QtCore.QPoint( point.x() + 10, point.y() + 30 )
        self.popMenu = QtGui.QMenu( self )
        self.popMenu.addAction("Nuevo",self.on_btAgregar_clicked ,QtGui.QKeySequence("Ctrl+N"))
        self.popMenu.addAction("Modificar",self.on_btEditar_clicked ,QtGui.QKeySequence("Ctrl+M"))
        self.popMenu.addAction("Eliminar",self.on_btEliminar_clicked ,QtGui.QKeySequence("Del"))
        
        self.popMenu.exec_(self.MyTabla.widget.mapToGlobal(mypoint) )
 
    def actual_rows_to_objects( self ):
        '''
        Obtiene los objetos seleccionados en la tabla
        @return: un objeto del tipo que maneja self.manager
        '''
        listadelistastring = self.MyTabla.getListSelectedRows()
        atributos_names = self._get_attributes_names()
        classid = self.manager.CLASSid
        listadeobjetos = []
        if listadelistastring != []:
            # obtiene el tipo de dato de la clave del objeto
            for value in self.manager.getClassAttributesInfo().values() :
                if value['primary'] == True :
                    primary_type = value['type'] 
            
            for lista in listadelistastring:
                posicion_ide = atributos_names.index( classid )
                if primary_type is 'int' :
                    valor_ide = int( lista[posicion_ide] )
                else:
                    valor_ide = lista[posicion_ide]   
                                      
                listadeobjetos.append( self.manager.searchBy( self._obtainColumnForName( self.manager.CLASSid ), valor_ide )[0] )
            return listadeobjetos
        return None
    
##############################
# METODOS PARA REIMPLEMENTAR #
##############################

    def add( self ):
        #REIMPLEMENT
        return self.DialogAddClass( self.manager, itemaeditar = False, managers = self.managers )
    
    def edit( self, obj ):
        #REIMPLEMENT
        return self.DialogAddClass( self.manager, itemaeditar = obj, managers = self.managers )

    def delete( self, obj ):
        #REIMPLEMENT
        self.manager.delete( obj )

##########################
# METODOS DE LOS EVENTOS #
########################## 

    def setItemsCount( self, valor ):
        '''
        Establece en el label la cantidad de elementos listados.
        '''
        self.lbCantidadItems.setText( str( valor ) + ' items(s) seleccionado(s)' )
        
    def on_leBusqueda_textChanged( self, cadena ):
        self._find()
        
    @QtCore.pyqtSlot( int )
    def on_cbCampos_currentIndexChanged ( self, entero ):
        if not self.leBusqueda.text().isEmpty() :
            self._find()
    
    @QtCore.pyqtSlot()
    def on_btAgregar_clicked( self ):
        wAgregar = self.add()
        wAgregar.setWindowIcon(self.windowIcon())
        wAgregar.postSaveMethod = self.reloadList
        wAgregar.exec_()
    
    @QtCore.pyqtSlot()
    def on_btEditar_clicked( self ):
        listadeobjetosseleccionados = self.actual_rows_to_objects()
        if listadeobjetosseleccionados:
            for obj in listadeobjetosseleccionados:
                wEditar = self.edit( obj )
                wEditar.setWindowIcon(self.windowIcon())
                wEditar.postSaveMethod = self.reloadList
                wEditar.exec_()

    @QtCore.pyqtSlot()
    def on_btEliminar_clicked( self ):
        listadeobjetosseleccionados = self.actual_rows_to_objects()
        if listadeobjetosseleccionados:
            for obj in listadeobjetosseleccionados:
                result = QtGui.QMessageBox.warning( self, u"Eliminar",
                    u"¿Esta seguro que desea eliminar?.\n\n",
                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No )
                if result == QtGui.QMessageBox.Yes:
                    self.delete( obj )
                    self._find()

    def on_twDatos_itemSelectionChanged(self):
        self.btEditar.setVisible(False)
        self.btEliminar.setVisible(False)
        items = self.MyTabla.getListSelectedRows()
        if items  :
            self.btEditar.setVisible(True)
            self.btEliminar.setVisible(True)

#########
# OTROS #
#########

    def _centerOnScreen ( self ):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move( ( resolution.width() / 2 ) - ( self.frameSize().width() / 2 ),
                  ( resolution.height() / 2 ) - ( self.frameSize().height() / 2 ) )
