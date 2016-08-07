#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Informática MEG <contacto@informaticameg.com>
#
# Written by
#       Copyright 2012 Fernandez, Emiliano <emilianohfernandez@gmail.com>
#       Copyright 2012 Ferreyra, Jonathan <jalejandroferreyra@gmail.com>
#
# MIT Licence
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from PyQt4 import QtCore, QtGui


class MyTableWidget():

    def __init__(self, TW, listadecolumnas, listadealineaciones = [], fnParseItem=None):
        self.__widget = TW
        #self.__widget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        #quitAction = QtGui.QAction("Quit", self.__widget)
        #self.__widget.addAction(quitAction)
        self.__widget.horizontalHeader().setDefaultSectionSize(150)
        #NEXT:que divida los campos en la tabla y que ponga bien los numeros
        self.__widget.horizontalHeader().setResizeMode(0)#maximiza los campos en la tabla
        self.__widget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.__widget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        #self.__widget.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )

        self.__columns = listadecolumnas
        self.fnParseItem = fnParseItem

        if listadealineaciones :
            alineaciones = {
                'L':QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                'C':QtCore.Qt.AlignCenter,
                'R':QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
            }
            self.__columns_align = [alineaciones[ali] for ali in listadealineaciones]
        else:
            self.__columns_align = [QtCore.Qt.AlignCenter] * len(listadecolumnas)

        self.__widget.setColumnCount(len(self.__columns))
        for i in xrange(self.__widget.columnCount()):  # set horizontal headers
            item = QtGui.QTableWidgetItem(self.__columns[i].capitalize())# the text
            item.setTextAlignment(QtCore.Qt.AlignCenter)# the alignment
            self.__widget.setHorizontalHeaderItem(i, item)

    def appendItem(self,listadedatos):
        alineaciones = self.__columns_align
        def aux(x, cell):
            item = QtGui.QTableWidgetItem(unicode(cell))# the text
            if self.fnParseItem:
                item = self.fnParseItem(y, x, item, cell)
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable )
            item.setTextAlignment( alineaciones[x] )# the alignment
            widget.setItem(y, x, item)
        widget = self.__widget
        y = widget.rowCount()
        if listadedatos != None:
            listadedatos = map(lambda valor : '' if valor is None else valor, listadedatos)
            widget.setRowCount(y+1)
            [ aux(x, cell) for x,cell in enumerate(listadedatos)]

    def addItems(self, DATA):
        """
        DATA debe ser una lista de listas
        """
        alineaciones = self.__columns_align
        def addOneItem(listadedatos, y):
            def aux(x, cell):
                item = QtGui.QTableWidgetItem(unicode(cell))# the text
                if self.fnParseItem:
                    item = self.fnParseItem(y, x, item, cell)
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable )
                try:
                    item.setTextAlignment( alineaciones[x] ) # the alignment
                except Exception, e:
                    raise Exception('The alignment for the %sth column is not defined' % (x+1))
                widget.setItem(y, x, item)
            listadedatos = ['' if dato is None else dato for dato in listadedatos ]
            [ aux(x, cell) for x,cell in enumerate(listadedatos)]

        if DATA != None:
            widget = self.__widget
            self.widget.setUpdatesEnabled(False)
            self.fullClear()
            widget.setRowCount(len(DATA))
            [addOneItem(data, indice) for indice, data in enumerate(DATA)]
            self.widget.setUpdatesEnabled(True)

    def getRowString(self, item = 'null'):
        """Devuelve una tupla con los datos de el tablewidget en la fila seleccionada
        devuelve los datos en unicode"""
        tablewidget = self.__widget
        tamano = tablewidget.columnCount()
        try:
            if item != 'null':
                x = item
            else:
                x = tablewidget.currentItem().row()
            datos=[]
            for num in range(tamano):
                qs = tablewidget.item(x,num).text()
                datos.append(unicode(qs.toUtf8(),'utf-8'))
            return tuple(datos)
        except Exception :
            return None

    def getListSelectedRows(self):
        seleccionados = self.__widget.selectionModel().selectedRows()
        rows = [self.getRowString(idx.row()) for idx in  seleccionados]
        return rows

    def getAllItems(self):
        tamano = self.__widget.rowCount()
        allitemstring = [self.getRowString(y) for y in range(tamano)]
        return allitemstring

    def fullClear(self):
        self.widget.setRowCount(0)
#        [self.__widget.removeRow(i) for i in range( self.__widget.rowCount() )[::-1]]

    def __get_widget(self):
        return self.__widget

    def __set_widget(self, value):
        self.__widget = value

    widget = property(__get_widget, __set_widget, "widget's docstring")




def main():

    return 0

if __name__ == '__main__':
    main()

