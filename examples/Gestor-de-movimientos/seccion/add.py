#!/usr/bin/env python
# -*- coding: utf-8 -*-
from plasta.gui.add_window import BaseAddWindow
from PyQt4 import uic, QtCore
from os.path import join,abspath,dirname
from seccion import Seccion
import GUI.images_rc


class AddSeccion(BaseAddWindow):

    def __init__(self,manager, itemToEdit = False, managers = []):
        BaseAddWindow.__init__(self, manager, itemToEdit, managers)
        FILENAME = 'agregar.ui'
        uic.loadUi(join(abspath(dirname(__file__)),FILENAME), self)
        self.cuentasManager = managers[0]
        self.ITEMLIST = [{self.leNombre:Seccion.nombre}]

        self._operaciones_de_inicio()

        self.leNombre.textEdited.connect(lambda text: self.leNombre.setText(text.toUpper()))

    #===========================================================================
    # Metodos Reimplementados
    #===========================================================================

    def _operaciones_de_inicio(self):
        '''
        operaciones que se requieren para iniciar la ventana
        '''
        self._centerOnScreen()
        self.agregarValidadores()
        self.btGuardar.setDefault(True)
        if self.EDITITEM:
            self.btGuardar.setText('Editar')
            self.setWindowTitle(u'Editar '+self.manager.getClassName())
            self._cargarDatosinWidgets()
        else:
            self.setWindowTitle(u"Agregar " + self.manager.getClassName())

        self.cargarListaCuentas()

    #REIMPLEMENTED
    def guardar(self, listadedatos):
        nuevaSeccion = BaseAddWindow.guardar(self, listadedatos)
        nombres = self.obtenerNombresCuentas()
        self.manager.establecerSeccion(
                self.obtenerObjetosCuenta( self.obtenerNombresCuentas() ),
                nuevaSeccion)
        return nuevaSeccion

    # REIMPLEMENTED
    @QtCore.pyqtSlot()
    def on_btGuardar_clicked(self):
        resultado = False
        if self.validarRestriccionesCampos() :
            datos = self.obtenerDatosWidgets()
            resultado = self.guardar(datos) if not self.EDITITEM else self.editar(datos)
            if self.postSaveMethod :
                self.postSaveMethod()
            resultado = True if isinstance(resultado, Seccion) else False
            self._mostrarMensajeResultado(resultado)
            self.close()
        return resultado

    #===========================================================================
    # Metodos auxiliares
    #===========================================================================

    def cargarListaCuentas(self):
        # manager Cuentas
        cuentas = self.managers[0].getall()
        cuentas = filter(lambda cuenta : True if cuenta.seccion == None else False, cuentas)
        self.lwCategorias.addItems( [cuenta.nombre for cuenta in cuentas] )

    def incluir_excluir(self, lista_origen, lista_destino):
        """
        Incluye o excluye el item seleccionado de la lista.

        @param lista_origen : lista de donde se va a quitar el item
        @param lista_destino : lista donde se va a agergar el item

        NOTA: soportado solo para QListWidget
        """
        lista_destino.addItem( lista_origen.currentItem().text() )
        lista_origen.takeItem( lista_origen.row( lista_origen.currentItem()) )

    def obtenerNombresCuentas(self):
        """ Devuelve una lista de cadenas con los nombres de las cuentas seleccionadas para
        ser incluidas dentro de una seccion. """
        items = [self.lwNuevaSeccion.item(it).text() for it in xrange(self.lwNuevaSeccion.count())]
        return [unicode(item.toUtf8(),'utf-8') for item in items]

    def obtenerObjetosCuenta(self, nombres_cuenta):
        return [self.cuentasManager.get(nombre)[0] for nombre in nombres_cuenta]

    #===========================================================================
    # Metodos de eventos
    #===========================================================================

    @QtCore.pyqtSlot()
    def on_btIncluir_clicked(self):
        self.incluir_excluir(self.lwCategorias, self.lwNuevaSeccion)

    @QtCore.pyqtSlot()
    def on_btExcluir_clicked(self):
        self.incluir_excluir(self.lwNuevaSeccion, self.lwCategorias)

    def on_lwCategorias_doubleClicked(self , index):
        self.on_btIncluir_clicked()

    def on_lwNuevaSeccion_doubleClicked(self , index):
        self.on_btExcluir_clicked()


