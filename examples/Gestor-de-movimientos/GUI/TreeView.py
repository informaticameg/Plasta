#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2011 Emiliano Fernandez <emilianohfernandez@gmail.com>
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


from PyQt4 import QtGui,QtCore
class TreeView:

    def __init__(self, treeview,conector, metodo,iconSub=QtGui.QIcon(),iconRoot=QtGui.QIcon()):
        '''TODO:Buscar doc de esto'''
        self.__iconSub = iconSub
        self.__iconRoot = iconRoot
        self.__model = self.__crearmodelo()
        treeview.setModel(self.__model)
        SelectionModel = QtGui.QItemSelectionModel( self.__model,treeview)
        treeview.setSelectionModel(SelectionModel)
        conector(SelectionModel, QtCore.SIGNAL(
                    "currentChanged(const QModelIndex &, const QModelIndex &)"),metodo)
        self.widget = treeview
        
    def __getModel(self):
        return self.__model

    def __setModel(self, model = None):
        self.__model = model

    def __crearmodelo(self):
        model = QtGui.QStandardItemModel()
        return model

    def addItems(self,listaitems):
        u"""
        """
        self.__model.clear()
        dicDeRootQitems = {}
        for criterios in listaitems:
            if not (criterios[0] in dicDeRootQitems):#no hay raiz
                tempRootItem = self.__model.invisibleRootItem()#creo un Root item vacio
                #se crea un item y la agrega al diccionario local
                dicDeRootQitems[criterios[0]] = QtGui.QStandardItem(self.__iconRoot,QtCore.QString(criterios[0]))
                dicDeRootQitems[criterios[0]].setEditable(False)
                #agrego el item al root item(convirtiendolo en root)
                tempRootItem.appendRow(dicDeRootQitems[criterios[0]])
            subitem = QtGui.QStandardItem(self.__iconSub,QtCore.QString(criterios[1]))
            subitem.setEditable(False)
            #agrega el subitem al root_item correspondiente
            dicDeRootQitems[criterios[0]].appendRow(subitem)
        return str(len(listaitems))

    model = property(fget = __getModel, fset = __setModel)


def main():
    return 0

if __name__ == '__main__':
    main()

