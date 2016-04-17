#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui

def centerOnScreen(self):
  resolution = QtGui.QDesktopWidget().screenGeometry()
  self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
    (resolution.height() / 2) - (self.frameSize().height() / 2))

def parseDt2St(row, value):
    return value.strftime("%d/%m/%Y")

def parseAmount(row, value):
    return "$ %8.2f" % float(value)

def setStyle(self, style=''):
    import config
    path = 'plasta/gui/styles/{style}.css'
    if len(style) > 0:
        path_css = path.replace('{style}', style)
    else:
        path_css = path.replace('{style}', config.STYLE)
    self.setStyleSheet(open(path_css).read())

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