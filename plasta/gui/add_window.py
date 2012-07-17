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

from PyQt4 import QtCore, QtGui


class BaseAddWindow(QtGui.QDialog):
    '''
    Clase base para el manejo de la pantalla para dar de alta/modificar un registro.
    '''
    
    def __init__(self,unManager, itemaeditar = False, managers = []):
        QtGui.QDialog.__init__(self)        
        self.manager = unManager
        self.managers = managers
        self.EDITITEM = itemaeditar
        
        self.ITEMLIST = []        
        self.dict_referencias = {} # diccionario que contiene la instancia seleccionada en el buscador
        self.postSaveMethod = None # metodo que BaseGUI que se ejecuta luego de save() 
        self._dictWidgetReferencias = {} # diccionario que contiene los widget boton y la referencia a la cual pertenece
    
##########################
# METODOS DE LOS EVENTOS #
##########################    
    
    @QtCore.pyqtSlot()
    def on_btGuardar_clicked(self):
        resultado = False
        if self.validateConstraintsFields() :
            datos = self.getDataOfWidgets()
            resultado = self.save(datos) if not self.EDITITEM else self.edit(datos)
            if self.postSaveMethod :
                self.postSaveMethod()        
            self._showResultMessage(resultado)
            self.close()
        return resultado
    
    def _showResultMessage(self, resultado):
        if not self.EDITITEM:
            if resultado :            
                QtGui.QMessageBox.information(self, "Agregar "+self.getClassName(),self.getClassName()+u" agregado con éxito.")
            else:
                QtGui.QMessageBox.warning(self, "Agregar "+self.getClassName(),"No se pudo agregar el "+self.getClassName())
        else:
            if resultado :
                QtGui.QMessageBox.information(self, "Editar " +self.getClassName(),self.getClassName()+" editado con exito.")
            else:
                QtGui.QMessageBox.warning(self, "Editar "+self.getClassName(),"No se pudo edit el "+self.getClassName())        
        
    @QtCore.pyqtSlot()
    def on_btSalir_clicked(self):
        self.close()
        
######################
# METODOS AUXILIARES #
######################  

    def setValidators(self):
        '''
        A partir de las restricciones de la clase, valida antes de ser guardado el 
        nuevo registro, que cumplan con esas restricciones.
        '''
        
        infoclase = self.manager.getClassAttributesInfo()
        for dato in self.ITEMLIST:
            widget = dato.keys()[0]
            atributo_clase = dato.values()[0]
            nombrecolumnalabel = "lb"+[k for k, v in self.__dict__.iteritems() if v == widget][0][2:]  
            if str(type(atributo_clase)) == "<class 'storm.references.Reference'>" : 
                try:
                    widget.setReadOnly(True)
                    # conecta el evento al boton de una referencia
                    nombreboton = "bt" + [k for k, v in self.__dict__.iteritems() if v == widget][0][2:]
                    widgetboton = self.__dict__[nombreboton]
                    self._dictWidgetReferencias[ widgetboton ] = atributo_clase
                    self.connect(widgetboton, QtCore.SIGNAL('clicked ()'),self.mostrarBuscador)
                except KeyError, msg:
                    print 'KeyError: Posiblemente no has agregado el boton para elegir una referencia.\nMensaje del error: ' + str(msg)
            else:
                columnastorm = self.manager.propertyToColumn(atributo_clase)
                if infoclase[columnastorm]["type"] == 'str':
                    pass
                elif infoclase[columnastorm]["type"] == 'int':
                    if type(widget) is QtGui.QLineEdit :
                        widget.setValidator(QtGui.QIntValidator())
                
                if infoclase[columnastorm]["null"] == False:
                    try:
                        label = self.__dict__[nombrecolumnalabel]
                        label.setText(label.text()+u'*')
                        # setea el color de fondo indicando que es una campo obligatorio
                        widget.setStyleSheet('background-color: rgb(223, 221, 255);')
                    except KeyError, msg:
                        print 'ERROR al intentar validar las restricciones para <%s>' % nombrecolumnalabel
                        print 'KeyError: Posiblemente el widget QLabel se llama de otra manera.'
                        print 'SOLUCION: Debe llamarce de la misma manera que el atributo de la clase.'
                    
                if infoclase[columnastorm]["default"] != None:
                    #NEXT:poner valor por defecto
                    pass
                
                if infoclase[columnastorm]["primary"] == True:
                    label = self.__dict__[nombrecolumnalabel]
                    label.setText(label.text()+u'*')
                    #NEXT:not null
                    # setea el color de fondo indicando que es una campo obligatorio
                    widget.setStyleSheet('background-color: rgb(223, 221, 255);')

    def validateConstraintsFields(self):
        """
        Comprueba que los campos que son <primary key> y <allow none = False>, 
        no esten vacios a la hora de save(). 
        """
        
        valido = True 
        color_rojo = 'background-color: rgb(255, 178, 178);'
        
        # 1° obtener la informacion de los atributos
        # 2° obtener a partir de los atributos, los properties 
        # 3° a partir de los properties obtener los widgets
        def filerAttributes(informacion):
            info_que_necesito = filter( 
                    lambda atributo : True if ((atributo['primary'] == True) or (atributo['null'] == False)) else False,
                    informacion.values())
            return map(lambda atri : self.getKeyDictionary(informacion, atri), info_que_necesito)
            
        # obtiene los atributos que poseen restricciones
        attributes = filerAttributes( self.manager.getClassAttributesInfo() ) 
        # obtiene los widgets y ya setea el color en cas
        for atributo in attributes :
            for item in self.ITEMLIST :                
                if self.manager.propertyToColumn(item.values()[0]) == atributo :
                    widget = item.keys()[0]
        
                    if type(widget) is QtGui.QLineEdit :
                        if widget.text().isEmpty() :
                            valido = False
                            widget.setStyleSheet( color_rojo )
                    elif type(widget) is QtGui.QTextEdit :
                        if widget.toPlainText().isEmpty() :
                            valido = False
                            widget.setStyleSheet( color_rojo )
        return valido
        
    def getKeyDictionary(self, dic, val):
        """return the key of dictionary dic given the value"""
        return [k for k, v in dic.iteritems() if v == val][0]
    
    def getDataOfWidgets(self):
        '''
        Obtiene los datos de las widget contenidos
         en las claves de ITEMLIST
        @return: lista de valores
        '''
        from PyQt4.QtGui import QIntValidator,QLineEdit,QComboBox,QLabel,QDateEdit,QTextEdit,QSpinBox,QCheckBox
        
        def textToUnicode(dato):
            return unicode(dato.toUtf8(),'utf-8')
        
        def isCheckBox(widget):
            return widget.isChecked()
            
        def isSpinBox(widget):
            return widget.value()
            
        def isTextEdit(widget):
            return textToUnicode( widget.toPlainText() )
        
        def isLineedit(widget):
            if type(widget.validator()) == QIntValidator:
                if not widget.text().isEmpty() :                    
                    value = int(isLabel(widget))
                else:
                    value = None
            else:
                value = isLabel(widget)
            return value

        def isDateEdit(widget):
            return textToUnicode(widget.date().toString(widget.displayFormat()))

        def isCombobox(widget):
            return textToUnicode(widget.itemText(widget.currentIndex()))
                
        def isLabel(widget):
            return textToUnicode(widget.text())
        
        funcionwidget = {QLineEdit:isLineedit,QComboBox:isCombobox,QLabel:isLabel,
                        QDateEdit:isDateEdit,QTextEdit:isTextEdit,QSpinBox:isSpinBox,
                        QCheckBox:isCheckBox}

        values = []
        for dicci in self.ITEMLIST:
            widget = dicci.keys()[0]
            if not(widget in self.dict_referencias):
                valor = funcionwidget[type(widget)](widget)
            else:
                valor = self.dict_referencias[widget]
            
            values.append(valor) if valor != u'' else values.append(None) #@NoEffect
        return values
    
    def getDataInstance(self):
        '''
        Obtiene los datos de los atributos contenidos
        en los valores de ITEMLIST del obj EDITITEM
        @requires: usar storm
        @return: lista de datos [{nombreatributo,valor}] o false(si no hay EDITITEM)
        '''
        if not self.EDITITEM:
            return False
        listcolumns = []
        import storm
        for v in self.ITEMLIST:
            if type(v.values()[0]) == storm.references.Reference:
                self.dict_referencias[v.keys()[0]] = self.EDITITEM.__getattribute__(
                    self.manager._getReferenceName(v.values()[0]))
            listcolumns.append(v.values()[0])
        return self.manager.getDataObject(self.EDITITEM,listcolumns)
        
    def getClassName(self):
        '''
        @requires: usar storm
        @return: el nombre de la clase que maneja el manager
        '''
        return self.manager.getClassName()

    def editProperties(self):
        '''
        Obtiene los datos de EDITITEM y los de los widgets
        los compara y si son distintos edita el atributo del obj
        '''
        datos = self.getDataOfWidgets()
        propiedadesvalues = self.getDataInstance()
        for i,dato in enumerate(datos):
            nombrepropiedad = propiedadesvalues[i].keys()[0]
            valor = propiedadesvalues[i].values()[0]
            if valor != dato:
                self.EDITITEM.__setattr__(nombrepropiedad,dato) 
        return True       

    def save(self, listadedatos):
        '''
        Metodo que automatiza el guardado de los datos.
        @param listadedatos:lista de datos perteneciente al init de la clase que maneja
        '''
        #REIMPLEMENT
        return self.manager.add(*listadedatos)
    
    def edit(self, listadedatos):
        '''
        Metodo que automatiza el edit de los datos.
        @param listadedatos:lista de datos perteneciente al init de la clase que maneja
        '''
        #REIMPLEMENT
        try:
            self.editProperties()
            self.manager.almacen.commit()
            return True
        except Exception,e:
            print e
            return False
 
    def _start_operations(self):
        '''
        operaciones que se requieren para iniciar la ventana
        '''

        self._centerOnScreen()
        self.setValidators()
        self.btGuardar.setDefault(True)
        if self.EDITITEM:
            self.btGuardar.setText('Editar')
            self.setWindowTitle(u'Editar ' + self.manager.getClassName())
            self._loadDataInWidgets()
        else:
            self.setWindowTitle(u"Agregar " + self.manager.getClassName())
    
    def _loadDataInWidgets(self):
        '''
        carga los datos de el obj EDITITEM en sus correspondientes
        widgets marcados por ITEMLIST
        '''
        import PyQt4
        for propnombre,propvalue in enumerate(self.getDataInstance()):
            widget = self.ITEMLIST[propnombre].keys()[0]
            dato = propvalue.values()[0]
            if not dato is  None :
                tipo = type(widget)            
                if tipo is PyQt4.QtGui.QLineEdit :
                    widget.setText(unicode(str(dato),'utf-8'))
                elif tipo is PyQt4.QtGui.QComboBox:
                    widget.addItem(dato)
                elif tipo is PyQt4.QtGui.QLabel:
                    widget.setText(dato)
                elif tipo is PyQt4.QtGui.QTextEdit:
                    widget.setText(dato)
                elif tipo is PyQt4.QtGui.QSpinBox:
                    widget.setValue(int(dato))
                elif tipo is PyQt4.QtGui.QDateEdit:
                    widget.setDate(QtCore.QDate(dato.year, dato.month, dato.day))
        return True
            
    def _centerOnScreen (self):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
                  
    def _toUnicode(self, MyQString):
        '''
        convierte un string a unicode
        @param MyQString:QString a convertir
        @return: unicode value
        '''
        return unicode(MyQString.toUtf8(),'utf-8')
        
    def showSearch(self):
        """        
        """
        atributo = self._dictWidgetReferencias[self.sender()]
        # obtener el atributo remoto al que pertenece <atributo>
        all_info = self.manager.getClassAttributesInfo()
        for info_atributo in all_info :            
            if all_info[info_atributo]['reference'] != False :  #@attention: DON'T TOUCH 
                if all_info[info_atributo]['reference']['reference_instance'] is atributo :
                    atributo_remoto = all_info[info_atributo]['reference']['remote_key']
        # obtener el manager al que pertenece <atributo_remoto>
        manager_que_busco = None
        for unmanager in self.managers:        
            if atributo_remoto.__dict__['cls'] == unmanager.CLASS:
                manager_que_busco = unmanager
        # llamar a la ventana del buscador, pasandole el manager        
        from buscador import BaseBuscador
        self.dict_referencias[ self.referenceToWidget(atributo) ] = None
        search = BaseBuscador(manager_que_busco, self.dict_referencias)
        search.exec_()        
         
    def referenceToWidget(self, referencia):
        """
        A partir de una referencia, obtiene el widget correspondiente que es usado por esa referencia.
        """
        for dicti in self.ITEMLIST:
            if dicti.values()[0] is referencia :
                return dicti.keys()[0]
