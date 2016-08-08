#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui

def loadUI(self, pathToFile=None):
    '''
    Read and load the screen indicate by <pathToFile>

    @param {str} pathToFile = path to .ui file
        If is None, look the ui in the location
        relative to the current folder
    '''
    from plasta.config import config
    from PyQt4 import uic
    from plasta.utils import pathtools
    if pathToFile is None:
       pathToFile = self.FILENAME
    if config.DEVELOP:
        mainFolder = pathtools.getPathProgramFolder()
        uic.loadUi(pathtools.convertPath(mainFolder + pathToFile), self)
    else:
        import cStringIO, uis
        uic.loadUi(cStringIO.StringIO(uis[pathToFile]), self)

def centerOnScreen(self):
    resolution = QtGui.QDesktopWidget().screenGeometry()
    self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
              (resolution.height() / 2) - (self.frameSize().height() / 2))

def parseDt2St(row, value):
    if value:
        return value.strftime("%d/%m/%Y")
    return u''

def parseAmount(row, value):
    if value:
        return "$ %8.2f" % float(value)
    return u'$ 0.00'

def parseBool(row, value):
    return 'SI' if value else 'NO'

def setStyle(self, style=''):
    from plasta.config import config
    path = 'plasta/gui/styles/{style}.css'
    if len(style) > 0:
        path_css = path.replace('{style}', style)
    elif len(config.STYLE) > 0:
        path_css = path.replace('{style}', config.STYLE)
    if (len(style) > 0) or (len(config.STYLE) > 0):
        curStyleSheet = toUnicode(self.styleSheet())
        self.setStyleSheet(open(path_css).read() + curStyleSheet)

def toUnicode(MyQString):
    '''
    convierte un qstring a unicode
    @param MyQString:QString a convertir
    @return: unicode value
    '''
    return unicode(MyQString.toUtf8(),'utf-8')

def getDataOfWidgets(widgets):
    '''
    Obtiene los datos de las widget contenidos
     en las claves de ITEMLIST
    @return: lista de valores
    '''
    from PyQt4.QtGui import QIntValidator,QLineEdit,QComboBox,QLabel,QDateEdit
    from PyQt4.QtGui import QTextEdit,QSpinBox,QDoubleSpinBox,QCheckBox

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
                    QDoubleSpinBox:isSpinBox,QCheckBox:isCheckBox}

    values = []
    for widget in widgets:
        valor = funcionwidget[type(widget)](widget)
        values.append(valor)
    return values