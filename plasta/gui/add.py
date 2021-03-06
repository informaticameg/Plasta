#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui, uic
from plasta import config
from plasta.utils.qt import sortListOfListObjs, centerOnScreen, loadUI


class BaseAdd(QtGui.QDialog):
    '''Base class to handle add/edit windows'''

    def __init__(self, manager, itemToEdit = False, managers = [], parent = None):
        QtGui.QDialog.__init__(self)
        self.manager = manager
        self.managers = managers
        self.itemToEdit = itemToEdit
        self.parent = parent

        # list of columns/attributes of the table
        # sintax: [{'showText', Object.attribute}, ...]
        self.ITEMLIST = []
        # name or path of ui to use
        self.FILENAME = 'add.ui'
        self.dict_referencias = {} # diccionario que contiene la instancia seleccionada en el buscador
        self.postSaveMethod = None # metodo que BaseGUI que se ejecuta luego de save()
        self._dictWidgetReferencias = {} # dictionary that contain the buttons widgets and the reference to wich belong
        self.develop = config.DEVELOP

        # add here the validators to execute before save/edit
        # available validators: unique | presence
        # sintax: {'nameField':'nameValidator', ...}
        # ej: {'codigo':'precence'}
        self.validators = {}

        # self.validatorCustom = {'myattr':myFnCustom}
        # la funcion recibe como parametros ({str} attr, {dict} allObjectValues)
        # debe retornar una tupla {bool} result, {str} errorMessage
        self.validatorCustom = {}

        # functions parsers to apply before save
        # sintax: {Class.attr:fnParse, ...}
        self.parsers = {}

        # references attributes to other models
        self.references = {}

        self.singleTitle = self.manager.getClassName()
        self.lang = config.LANG
        self.messages = {
            'es':{
                'newTitle':'Nuevo ',
                'editTitle':'Editar ',
                'newSuccefullSave':u" agregado correctamente",
                'editSuccefullSave':u" editado correctamente",
                'newErrorSave':u"No se pudo agregar el ",
                'editErrorSave':u"No se pudo editar el ",
                'savingTitle':u"Guardando",
                'validateUnique':u'Ya existe un elemento con el mismo nombre',
                'validatePresence':u'{field} no puede dejarse vacío'
            },
            'en':{
                'newTitle':'New ',
                'editTitle':'Edit ',
                'newSuccefullSave':u" added succefull",
                'editSuccefullSave':u" edited succefull",
                'newErrorSave':u"Can't be added ",
                'editErrorSave':u"Can't be edited ",
                'savingTitle':u"Saving",
                'validateUnique':u'Already exists a element with the same name',
                'validatePresence':u"{field} can't be empty value"
            }
        }

    def _start_operations(self):
        '''
        operaciones que se requieren para iniciar la ventana
        '''
        self.processEvents = QtGui.QApplication.processEvents
        centerOnScreen(self)
        self.setValidators()
        self.btSave.setDefault(True)
        self.processEvents()
        if self.itemToEdit:
            self.btSave.setText(self.getMsgByLang('editTitle'))
            self.setWindowTitle(self.getMsgByLang('editTitle') + ' ' + self.singleTitle.lower())
            self._loadDataInWidgets()
            self.processEvents()
        else:
            self.setWindowTitle(self.getMsgByLang('newTitle') + ' ' + self.singleTitle.lower())

        QtGui.QShortcut( QtGui.QKeySequence( "F9" ), self, self.on_btSave_clicked )
        QtGui.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_Escape ), self, self.close )

        for item in self.ITEMLIST:
            widget = item.keys()[0]
            value = item.values()[0]
            if str(type(value)) == "<class 'storm.references.Reference'>" and\
                str(type(widget)) == "<class 'PyQt4.QtGui.QComboBox'>":
                try:
                    cls = value.__dict__['_remote_key'][0].__dict__['cls']
                except TypeError, e:
                    cls = value.__dict__['_remote_key'].__dict__['cls']
                self.references[value] = {'cls':cls, 'fnParser':None,
                    'objs':None, 'useEmptyOption':False}

    def startOperations(self):
        self._start_operations()

###################
# EVENT FUNCTIONS #
###################

    @QtCore.pyqtSlot()
    def on_btSave_clicked(self):
        self.btSave.setText(self.getMsgByLang('savingTitle') + '...')
        self.btSave.setEnabled(False)
        self.processEvents()
        resultado = False
        datos = self.getDataOfWidgets()
        if self.validateConstraintsFields() :
            if self.validateCustomConstraints(datos):
                resultado = self.save(datos) if not self.itemToEdit else self.edit(datos)
                if self.postSaveMethod :
                    self.postSaveMethod()
                self._showResultMessage(resultado)
                self.close()
        return resultado

    @QtCore.pyqtSlot()
    def on_btExit_clicked(self):
        self.close()

#################
# AUX FUNCTIONS #
#################

    def loadUI(self, pathToFile = None):
        if pathToFile is None:
            pathToFile = self.FILENAME
        loadUI(self, pathToFile)

    def isEditing(self):
        return True if self.itemToEdit else False

    def getMsgByLang(self, msg):
        return self.messages[self.lang][msg]

    def _showResultMessage(self, resultado):
        if not self.itemToEdit:
            resultado = True if resultado is None else resultado
            if resultado :
                QtGui.QMessageBox.information(
                    self, self.getMsgByLang('newTitle') + self.singleTitle.lower(), self.singleTitle.capitalize()  + self.getMsgByLang('newSuccefullSave'))
            else:
                QtGui.QMessageBox.warning(
                    self, self.getMsgByLang('newTitle') + self.singleTitle.lower(), self.getMsgByLang('newErrorSave') + self.singleTitle.lower())
        else:
            if resultado :
                QtGui.QMessageBox.information(
                    self, self.getMsgByLang('editTitle') + self.singleTitle.lower(), self.singleTitle.capitalize() + self.getMsgByLang('editSuccefullSave'))
            else:
                QtGui.QMessageBox.warning(
                    self, self.getMsgByLang('editTitle') + self.singleTitle.lower(), self.getMsgByLang('editErrorSave') + self.singleTitle.lower())

    def setValidators(self):
        '''
        A partir de las restricciones de la clase, valida antes de ser guardado el
        nuevo registro, que cumplan con esas restricciones.
        '''
        infoclase = self.manager.getClassAttributesInfo()
        for dato in self.ITEMLIST:
            widget = dato.keys()[0]
            atributo_clase = dato.values()[0]
            nombrecolumnalabel = "lb" + [k for k, v in self.__dict__.iteritems() if v == widget][0][2:]
            if str(type(atributo_clase)) == "<class 'storm.references.Reference'>" :
                try:
                    #widget.setReadOnly(True)
                    # conecta el evento al boton de una referencia
                    nombreboton = "bt" + [k for k, v in self.__dict__.iteritems() if v == widget][0][2:]
                    widgetboton = self.__dict__[nombreboton]
                    self._dictWidgetReferencias[ widgetboton ] = atributo_clase
                    self.connect(widgetboton, QtCore.SIGNAL('clicked ()'), self.showSearcher)
                except Exception, msg:
                    pass
                    #print 'KeyError: Posiblemente no has agregado el boton para elegir una referencia.\nMensaje del error: ' + str(msg)
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
                        label.setText(label.text() + u' *')
                        # setea el color de fondo indicando que es una campo obligatorio
                        widget.setStyleSheet('background-color: rgb(223, 221, 255);')
                    except KeyError, msg:
                        #print 'ERROR al intentar validar las restricciones para <%s>' % nombrecolumnalabel
                        #print 'KeyError: Posiblemente el widget QLabel se llama de otra manera.'
                        #print 'SOLUCION: Debe llamarce de la misma manera que el atributo de la clase.'
                        pass

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
                if not str(type(item.values()[0])) == "<class 'storm.references.Reference'>" :
                    if self.manager.propertyToColumn(item.values()[0]) == atributo :
                        widget = item.keys()[0]

                        if type(widget) is QtGui.QLineEdit :
                            if widget.text().isEmpty() :
                                valido = False
                        elif type(widget) is QtGui.QTextEdit :
                            if widget.toPlainText().isEmpty() :
                                valido = False
                        elif type(widget) is QtGui.QDoubleSpinBox :
                            if widget.value() <= 0.0 :
                                valido = False
                        if not valido :
                            widget.setStyleSheet( color_rojo )

        return valido

    def validateCustomConstraints(self, datos):
        # {list} datos = valores cargados en los widgets
        # validadores establecidos por el usuario
        validatorsFns = {
        'presence':self._validatesPresenceOf,
        'unique':self._validatesUniquenessOf,
        }
        value = None
        if len(self.validators.keys()) > 0:

            attributesNames = []
            for item in self.ITEMLIST:
                attrName = self.manager.getPropertyName(item.values()[0])
                attributesNames.append(attrName)

            for attr in self.validators.keys():
                #try:
                nameValidators = self.validators[attr]
                if str(type(self.validators[attr])) == "<type 'str'>":
                    nameValidators = [self.validators[attr]]
                for validator in nameValidators:
                    if validator != 'custom':
                        if validator == 'unique':
                            idxValue = attributesNames.index(attr)
                            value = datos[idxValue]

                        result, msg = validatorsFns[validator](attr, value)
                    else:
                        result, msg = self.validatorCustom[attr](attr, datos)
                    if result is False:
                        msg = msg + u'\n\nCompruebe la situación indicada para continuar'
                        QtGui.QMessageBox.warning(self, "Error", msg)
                        return False
                #except KeyError, e:
                #    raise Exception("No existe un validador llamado: ", self.validators[attr])
        return True

    def getListAttributesNames(self):
        '''Retorna una lista con los nombres de los
        atributos existentes en self.ITEMLIST'''
        result = []
        for item in self.ITEMLIST:
            classAttr = item.values()[0]
            result.append(self.manager.getPropertyName(classAttr))
        return result

    def getKeyDictionary(self, dic, val):
        """return the key of dictionary dic given the value"""
        return [k for k, v in dic.iteritems() if v == val][0]

    def getDataOfWidgets(self, widgets = None):
        '''
        Obtiene los datos de las widget contenidos
         en las claves de ITEMLIST
        @return: lista de valores
        '''
        from PyQt4.QtGui import QIntValidator,QLineEdit,QComboBox,QLabel,QDateEdit,QTextEdit,QSpinBox,QDoubleSpinBox,QCheckBox
        from plasta.utils.qt import getDataOfWidgets as getDOW

        if widgets:
            return getDOW(widgets)

        values = []
        for dicci in self.ITEMLIST:
            widget = dicci.keys()[0]
            attribute = dicci.values()[0]

            if not str(type(attribute)) == "<class 'storm.references.Reference'>":
                if not(widget in self.dict_referencias):
                    valor = getDOW([widget])[0]
                else:
                    valor = self.dict_referencias[widget]
            else:
                idx = widget.currentIndex()
                if self.references[attribute]['useEmptyOption']:
                    idx = idx - 1

                try:
                    valor = self.references[attribute]['objs'][idx] if idx >= 0 else None
                except TypeError, e:
                    print e
                    valor = None
            values.append(valor) if valor != u'' else values.append(None) #@NoEffect
        return values

    def getDataInstance(self):
        '''
        Obtiene los datos de los atributos contenidos
        en los valores de ITEMLIST del obj EDITITEM
        @requires: usar storm
        @return: lista de datos [{nombreatributo,valor}] o false(si no hay EDITITEM)
        '''
        if not self.itemToEdit:
            return False
        listcolumns = []
        import storm
        for v in self.ITEMLIST:
            if type(v.values()[0]) == storm.references.Reference:
                self.dict_referencias[v.keys()[0]] = self.itemToEdit.__getattribute__(
                    self.manager.getReferenceName(v.values()[0]))
            listcolumns.append(v.values()[0])
        return self.manager.getDataObject(self.itemToEdit, listcolumns, rformat='list')

    def getClassName(self):
        '''
        @requires: usar storm
        @return: el nombre de la clase que maneja el manager
        '''
        return self.manager.getClassName().lower()

    def editProperties(self, datos=None):
        '''
        Obtiene los datos de EDITITEM y los de los widgets
        los compara y si son distintos edita el atributo del obj
        '''
        if not datos:
            datos = self.getDataOfWidgets()
        propiedadesvalues = self.getDataInstance()
        for i, dato in enumerate(datos):
            nombrepropiedad = propiedadesvalues[i].keys()[0]
            valor = propiedadesvalues[i].values()[0]
            if valor != dato:
                self.itemToEdit.__setattr__(nombrepropiedad, dato)
        return True

    def applyParsers(self, listData):
        if len(self.parsers.keys()) > 0:
            attrs = self.getListAttributesNames()
            for class_attr, fnParser in self.parsers.iteritems():
                stName = self.manager.getPropertyName(class_attr)
                idx = attrs.index(stName)
                if idx >= 0:
                    listData[idx] = fnParser(listData[idx])

    def save(self, listData):
        '''
        Metodo que automatiza el guardado de los datos.
        @param listData:lista de datos perteneciente al init de la clase que maneja
        '''
        #REIMPLEMENT
        self.applyParsers(listData)
        return self.manager.add(listData)

    def edit(self, listData):
        '''
        Metodo que automatiza el edit de los datos.
        @param listData:lista de datos perteneciente al init de la clase que maneja
        '''
        #REIMPLEMENT
        try:
            self.applyParsers(listData)
            self.editProperties(listData)
            self.manager.store.commit()
            return True
        except Exception,e:
            print e
            return False

    def getReferenceObject(self, referenceCombo):
        '''
        Return the current selected object in the combo
        '''
        referenceAttr = None
        for item in self.ITEMLIST:
            widget = item.keys()[0]
            value = item.values()[0]
            if widget is referenceCombo:
                referenceAttr = value

        index = referenceCombo.currentIndex()
        if index >= 0:
            if self.references[referenceAttr]['useEmptyOption']:
                index = index - 1
            return self.references[referenceAttr]['objs'][index]
        return None

    def loadReferencesCombos(self, sort=True, sortAttr='nombre'):
        '''
        Load all combos references
        '''
        for refAttr in self.references.keys():
            for attr in self.ITEMLIST:
                if refAttr is attr.values()[0]:
                    widget = attr.keys()[0]
            self.loadReferenceCombo(widget, refAttr, sort, sortAttr)

    def loadReferenceCombo(self,
            widget, refAttr, sort=True, sortAttr='nombre',
            objs=None, findParams=[],
            emptyOption=False, emptyOptionTxt='[Seleccionar]'):
        '''
        Load specified combo with reference items

        @param {QComboBox} widget = combo widget to load items
        @param {Storm.property} refAttr =
        @param {list} objs = items to be loaded
        @param {list} findParams = params to be pased to orm find
        @param {bool} emptyOption = if true, add a blank first item
        @param {bool} emptyOptionTxt = text caption to show
        '''

        cls = self.references[refAttr]['cls']
        if not objs:
            objs = [obj for obj in self.manager.almacen.find( cls, *findParams)]

        self.references[refAttr]['objs'] = sortListOfListObjs(objs, sortAttr) if sort else objs

        widget.clear()
        if emptyOption:
            widget.addItem(emptyOptionTxt)
            self.references[refAttr]['useEmptyOption'] = True

        items = []
        for obj in objs:
            fnParser = self.references[refAttr]['fnParser']
            if fnParser:
                items.append(fnParser(obj))
            else:
                items.append(obj.__str__())
        [widget.addItem(item) for item in items]

    def chainReferencesCombos(self, comboIn, refAttrIn, comboOut, refAttrOut, emptyOption=False, emptyOptionTxt='[Seleccionar]'):
        '''
        '''
        #TODO
        # def loadComboOut():
        #     self.loadReferenceCombo(comboOut, refAttrOut)
        # self.connect(comboIn, QtCore.SIGNAL('currentIndexChanged (int)'), loadComboOut)
        pass


    def _loadDataInWidgets(self):
        '''
        carga los datos de el obj EDITITEM en sus correspondientes
        widgets marcados por ITEMLIST
        '''
        import PyQt4
        for propnombre, propvalue in enumerate(self.getDataInstance()):
            widget = self.ITEMLIST[propnombre].keys()[0]
            dato = propvalue.values()[0]
            if not dato is  None :
                tipo = type(widget)
                if tipo is PyQt4.QtGui.QLineEdit :
                    try:
                        widget.setText(unicode(dato,'utf-8'))
                    except TypeError, e:
                        widget.setText(dato)
                elif tipo is PyQt4.QtGui.QComboBox:
                    try:
                        idx = widget.findText(dato)
                    except Exception, e:
                        idx = widget.findText(dato.__str__())
                    finally:
                        if idx != -1:
                            widget.setCurrentIndex(idx)
                elif tipo is PyQt4.QtGui.QLabel:
                    widget.setText(dato)
                elif tipo is PyQt4.QtGui.QTextEdit:
                    widget.setText(dato)
                elif tipo is PyQt4.QtGui.QSpinBox:
                    widget.setValue(int(dato))
                elif tipo is PyQt4.QtGui.QDoubleSpinBox:
                    widget.setValue(float(dato))
                elif tipo is PyQt4.QtGui.QDateEdit:
                    widget.setDate(QtCore.QDate(dato.year, dato.month, dato.day))
        return True

    def _toUnicode(self, MyQString):
        '''
        convierte un string a unicode
        @param MyQString:QString a convertir
        @return: unicode value
        '''
        return unicode(MyQString.toUtf8(),'utf-8')

    def showSearcher(self):
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
        for key in self.managers.__dict__.keys():
            unmanager = self.managers.__dict__[key]
            try:
                if atributo_remoto.__dict__['cls'] == unmanager.CLASS:
                    manager_que_busco = unmanager
            except AttributeError, e:
                pass
        # llamar a la ventana del buscador, pasandole el manager
        from buscador import BaseSearcher
        self.dict_referencias[ self.referenceToWidget(atributo) ] = None
        search = BaseSearcher(manager_que_busco, self.dict_referencias)
        search.exec_()

    def referenceToWidget(self, referencia):
        """
        A partir de una referencia, obtiene el widget correspondiente que es usado por esa referencia.
        """
        for dicti in self.ITEMLIST:
            if dicti.values()[0] is referencia :
                return dicti.keys()[0]

###############
# API TO VARS #
###############

    def linkToAttribute(self, widget, classAttribute):
        item = {}
        item[widget] = classAttribute
        self.ITEMLIST.append(item)

    def setParser(self, classAttr, fnParse, onlyAdd=True, onlyEdit=True):
        if not self.itemToEdit:
            if onlyAdd:
                self.parsers[classAttr] = fnParse
        else:
            if onlyEdit:
                self.parsers[classAttr] = fnParse

    def addValidator(self, field, validator):
        self.validators[field] = validator

    def addReferenceComboParser(self, attribute, fn):
        self.references[attribute]['fnParser'] = fn

###############################
# VALIDATORS USED TO ADD/EDIT #
###############################

    def _validatesPresenceOf(self, field, value = None):
        '''Valida que el campo indicado haya sido rellenado.
        {str} field = nombre del campo'''

        widget = None
        # get the widget
        for item in self.ITEMLIST:
            if self.manager.getPropertyName(item.values()[0]) == field:
                widget = item.keys()[0]

        value = self.getDataOfWidgets([widget])[0]
        infoClass = self.manager.getClassAttributesInfo()
        infoAttr = None
        for stormAttr in infoClass:
            if infoClass[stormAttr]['name'] == field:
                infoAttr = infoClass[stormAttr]
                pass
        checkByType = {
        'str':lambda value: len(value) > 0,
        'int':lambda value: True,
        'float':lambda value: True,
        'date':lambda value: True,
        }
        message = self.getMsgByLang('validatePresence').replace('{field}', field.capitalize())
        return checkByType[infoAttr['type']](value), message


    def _validatesUniquenessOf(self, field, value):
        '''Valida que no exista otro elemento en el modelo
        con el mismo valor asignado al campo <field>
        {str} field = nombre del campo
        {str} value = valor actual'''

        classInfo = self.manager.getClassAttributesInfo()
        idx_classInfo_by_name = {}
        for k in classInfo.keys():
            v = classInfo[k]
            idx_classInfo_by_name[v['name']] = v

        infoAttr = idx_classInfo_by_name[field]
        dataValues = [item.__getattribute__(field) for item in self.manager.getall()]
        if infoAttr['type'] == 'str':
            dataValues = [dataValue.lower() for dataValue in dataValues]
            value = value.lower()
        dataValues = list(set(dataValues))

        if self.itemToEdit:
            if value in dataValues:
                del dataValues[dataValues.index(value)]
        return not value in dataValues, self.getMsgByLang('validateUnique')
