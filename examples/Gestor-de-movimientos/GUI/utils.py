#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2012 Ferreyra, Jonathan <jalejandroferreyra@gmail.com>
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
from PyQt4 import QtGui, QtCore


class Utils :
    
    def convertToDict(self, columnas, datos):
        resultado = {}
        for columna, valor in zip(columnas, datos) :
            resultado[columna] = valor
        return resultado

    def getFechaHoyString(self):
        from datetime import datetime
        hoy = datetime.today().strftime('%d-%m-%Y %H:%M:%S')
        return unicode(hoy,'utf-8')
        
    def normalizarBlancos(self, lista):
        """
        Reemplaza los espacios por un guion medio.
        """
        return map(lambda elemento : elemento if elemento != '' else '-',lista) 
    
    def getTextWidgets(self, * widgets):
        """
        Devuelve una lista con el valor cargado segun el widget
        """
        import PyQt4
        values = []
        for widget in widgets :
            if type(widget) is PyQt4.QtGui.QLineEdit :
                values.append(
                    unicode(widget.text().toUtf8(),'utf-8'))
            elif type(widget) is PyQt4.QtGui.QComboBox:
                values.append(
                    unicode(
                        widget.itemText(widget.currentIndex()).toUtf8(),
                        'utf-8'))
            elif type(widget) is PyQt4.QtGui.QLabel:
                values.append(
                    unicode(widget.text().toUtf8(),'utf-8'))
            elif type(widget) is PyQt4.QtGui.QDateEdit:
                values.append(
                    unicode(
                        widget.date().toString(widget.displayFormat()).toUtf8(),
                        'utf-8'))
            elif type(widget) is PyQt4.QtGui.QTextEdit:
                values.append(
                    unicode(widget.toPlainText().toUtf8(),'utf-8'))
            elif type(widget) is PyQt4.QtGui.QSpinBox:
                values.append(
                    unicode(str(widget.value()),'utf-8')
                    )
            # hack solo para esta situacion
            elif type(widget) is PyQt4.QtGui.QCheckBox :
                if widget.isChecked() is True :
                    values.append('SI')
                else:
                    values.append('NO')
                    
        return values
    
    def cargarWidgets(self,datos, widgets):
        import PyQt4        
        
        for dato, widget in zip(datos,widgets):
            if dato == '-':
                dato = ''            
            if type(widget) is PyQt4.QtGui.QLineEdit :
                widget.setText(dato)
            elif type(widget) is PyQt4.QtGui.QComboBox:                 
                widget.setCurrentIndex(
                    widget.findText(dato))
            elif type(widget) is PyQt4.QtGui.QLabel:
                widget.setText(dato)
            elif type(widget) is PyQt4.QtGui.QTextEdit:
                widget.setText(dato)
            elif type(widget) is PyQt4.QtGui.QDateEdit:                
                if len(dato) == 4 :
                    widget.setDate(PyQt4.QtCore.QDate(int(dato),1,1))
                elif len(dato) == 10 :
                    widget.setDate(PyQt4.QtCore.QDate(
                        int(dato[6:]),int(dato[3:5]),int(dato[:2])))
            elif type(widget) is PyQt4.QtGui.QSpinBox:    
                widget.setValue(int(dato))
            elif type(widget) is PyQt4.QtGui.QCheckBox:
                if dato == 'SI' :
                    widget.setChecked(True)
                else:
                    widget.setChecked(False)

    def validarCampos(self, * widgets):
        """
        Verifica que los widgets indicados no esten vacios.
        Devuelve True si todos los widgets estan cargados.
        """
        import PyQt4
        valido = True
        color_style_sheet = 'background-color: rgb(255, 155, 155);'
        for widget in widgets :
            if type(widget) is PyQt4.QtGui.QLineEdit :
                if widget.text().isEmpty() :
                    valido = False
                    widget.setStyleSheet(color_style_sheet)
            elif type(widget) is PyQt4.QtGui.QTextEdit:
                if widget.toPlainText().isEmpty() :
                    valido = False
                    widget.setStyleSheet(color_style_sheet)
            elif type(widget) is PyQt4.QtGui.QSpinBox:
                if widget.value() == 0 :
                    valido = False
                    widget.setStyleSheet(color_style_sheet)
            elif type(widget) is PyQt4.QtGui.QTimeEdit:
                if widget.dateTime().toString('HH:mm') == '00:00':
                    valido = False
                    widget.setStyleSheet(color_style_sheet)
        return valido

    def addDaysToCurrentDate(self, dias):
        from datetime import date, timedelta
        return date.today() + timedelta(days = dias)
         
#def main():
#   Utils()
#    
#if __name__ == '__main__':
#    main()
