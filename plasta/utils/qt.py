#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from plasta import config


def loadUI(self, pathToFile=None):
    '''
    Read and load the screen indicate by <pathToFile>

    @param {str} pathToFile = path to .ui file
        If is None, look the ui in the location
        relative to the current folder
    '''
    import cStringIO
    import os
    from uis import ui
    from PyQt4 import uic
    from plasta.utils import pathtools
    if pathToFile is None:
        pathToFile = self.FILENAME
    if config.DEVELOP:
        mainFolder = pathtools.getPathProgramFolder()
        uic.loadUi(pathtools.convertPath(mainFolder + pathToFile), self)
    else:
        pathToFile = pathtools.convertPath(pathToFile)
        if os.name == 'nt':
            pathToFile = '\\' + pathToFile
        uic.loadUi(cStringIO.StringIO(ui[pathToFile]), self)


def centerOnScreen(self):
    resolution = QtGui.QDesktopWidget().screenGeometry()
    self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
              (resolution.height() / 2) - (self.frameSize().height() / 2))


def processEvents():
    QtGui.QApplication.processEvents()


def parseDt2St(row, value):
    if value:
        return value.strftime("%d/%m/%Y")
    return u''


def parseDtTm2St(row, value):
    if value:
        return value.strftime("%d/%m/%Y %H:%M")
    return u''


def parseFN(row, value):
    from datetime import datetime
    if type(value) in [str, unicode]:
        return datetime.strptime(value, '%d/%m/%Y')
    if str(type(value)) == "<type 'datetime.date'>":
        return value.strftime("%d/%m/%Y")
    return ''


def parseAmount(row, value):
    try:
        osLocale = ''
        if os.name == 'posix':
            osLocale = 'es_US.utf8'
        elif os.name == 'nt':
            osLocale = 'English_United States.1252'
        locale.setlocale(locale.LC_ALL, osLocale)
        if value:
            return u"$ %s" % locale.format("%.2f", value, grouping=True)
    except Exception as e:
        return "$ %8.2f" % float(value)
    return u'$ 0.00'


def parseBool(row, value):
    return 'SI' if value else 'NO'


def getParsed(value, force=None):
    if force:
        value = force(value)

    if type(value) is float:
        return parseAmount('', value)
    elif type(value) is int:
        return str(value)
    elif type(value) is bool:
        return parseBool('', value)
    elif type(value) is datetime.date:
        return parseDt2St('', value)
    elif type(value) is datetime.datetime:
        return parseDtTm2St('', value)
    else:
        return value


def toUnicode(MyQString):
    '''
    convierte un qstring a unicode
    @param MyQString:QString a convertir
    @return: unicode value
    '''
    return unicode(MyQString.toUtf8(), 'utf-8')


def getDataOfWidgets(widgets):
    '''
    Obtiene los datos de las widget contenidos
     en las claves de ITEMLIST
    @return: lista de valores
    '''
    from PyQt4.QtGui import QIntValidator, QLineEdit, QComboBox, QLabel, QDateEdit
    from PyQt4.QtGui import QTextEdit, QSpinBox, QDoubleSpinBox, QCheckBox

    def textToUnicode(dato):
        return unicode(dato.toUtf8(), 'utf-8')

    def isCheckBox(widget):
        return widget.isChecked()

    def isSpinBox(widget):
        return widget.value()

    def isTextEdit(widget):
        return textToUnicode(widget.toPlainText())

    def isLineedit(widget):
        if type(widget.validator()) == QIntValidator:
            if not widget.text().isEmpty():
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

    funcionwidget = {QLineEdit: isLineedit, QComboBox: isCombobox, QLabel: isLabel,
                     QDateEdit: isDateEdit, QTextEdit: isTextEdit, QSpinBox: isSpinBox,
                     QDoubleSpinBox: isSpinBox, QCheckBox: isCheckBox}

    values = []
    for widget in widgets:
        valor = funcionwidget[type(widget)](widget)
        values.append(valor)
    return values


def sortListOfListObjs(lista, campo='name', index=0, fnParse=None):
    """Ordena la lista por el metodo burbuja mejorado.
    Recibe una lista de listas y un numero de campo,
    ordenando por el campo indicado.

    AVISO: solo soporta objetos storm
    """
    intercambios = 1
    pasada = 1
    while pasada < len(lista) and intercambios == 1:
        intercambios = 0
        for i in range(0, len(lista) - pasada):
            itemA = lista[i]
            itemB = lista[i + 1]
            if fnParse:
                itemA = fnParse(itemA)
                itemB = fnParse(itemB)
            if type(itemA) is dict:
                conditional = itemA[campo] > itemB[campo]
            elif type(itemA) in [list, tuple]:
                conditional = itemA[index] > itemB[index]
            else:
                conditional = itemA.__getattribute__(
                    campo) > itemB.__getattribute__(campo)
            if conditional:
                lista[i], lista[i + 1] = lista[i + 1], lista[i]
                intercambios = 1
        pasada += 1
    return lista


def obtenerNombreDia(nroDia):
    return {
        1: u'Lunes', 2: u'Martes',
        3: u'Miércoles', 4: u'Jueves',
        5: u'Viernes', 6: u'Sábado',
        7: u'Domingo'}[nroDia]


def getSingleLineCSSFile(filename):
    text = open(filename).read()
    return text.replace('\n', '').replace(' ', '')


def pprint(to_show):
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(to_show)
