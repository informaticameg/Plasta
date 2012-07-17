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

import storm


class Inspection :
    
    def __init__(self, oneClass):
        #@param CLASS: la clase que va a manipular ej:Cliente
        self.CLASS = oneClass 
        #@param CLASSATTRIBUTES: las columnas que va usar (DONTTOUCH)
        self.CLASSATTRIBUTES = []  
    
    def getClassAttributes( self ):
        '''
        Obtiene los atributos de la clase que maneja self.manager
        @return: una lista con los atributos de la clase en string
        '''
        if not self.CLASSATTRIBUTES:
            #lista de altributos que no tienen importancia
            itemAexcluir = ( '__storm_table__', '__module__',
               '__storm_class_info__', '__weakref__',
               '_storm_columns', '__dict__',
               '__doc__', '__init__', 'SQLTABLE', '__str__' )
            allAtributes = self.CLASS.__dict__
            for key in allAtributes:
                if not( key in itemAexcluir ) and key [-3:] != "_id":
                    #excluye a los identificadores de referencias EX: cliente_id
                    self.CLASSATTRIBUTES.append( key )
        return self.CLASSATTRIBUTES
    
    def getClassAttributesInfo( self ):
        '''
        Devuelve un diccionario con los tipos de datos de la clase
        @requires: storm
        @return:un diccionario clave:la columna, valor otro diccionario:
        ex:{<storm.properties.Unicode object at 0x9e87b0c>: {'name':'un_atributo','default': None, 'null': True, 'type': 'str', 'primary': False,'reference':False}}
        '''
        resultado = {}
        todelete = []
        for name in self.getClassAttributes(): #obtengo los nombe de atributos validos
            objcolumn = self.CLASS.__dict__[name]
            objcolumn_dict = objcolumn.__dict__
            unainfo = {}
            if type( objcolumn ) == storm.references.Reference:
                unainfo["type"] = 'reference'
                todelete.append( objcolumn )#eliminar _id
                try:#Fix para cuando sale una tupla en vez de un column (no tengo idea por que es)
                    unainfo["reference"] = {"remote_key":objcolumn_dict["_remote_key"][0], "reference_instance":objcolumn}
                    objcolumn = self.propertyToColumn( objcolumn_dict["_local_key"][0] )#dar los demas datos de ID
                except:
                    unainfo["reference"] = {"remote_key":objcolumn_dict["_remote_key"], "reference_instance":objcolumn}
                    objcolumn = objcolumn_dict["_local_key"]#dar los demas datos de ID
                
            else:
                unainfo["reference"] = False
                types = {
                    storm.properties.Unicode : 'str',
                    storm.properties.Int : 'int',
                    storm.properties.Bool : 'bool',
                    storm.properties.Date : 'date',
                    storm.properties.Float : 'float'
                }
                unainfo["type"] = types[ type(objcolumn) ]
            unainfo["name"] = name
            unainfo['primary'] = objcolumn_dict['_primary'] if "_primary" in objcolumn.__dict__ else False
            unainfo["null"] = objcolumn_dict['_variable_kwargs']["allow_none"] if "allow_none" in objcolumn_dict['_variable_kwargs'] else True
            unainfo["default"] = objcolumn_dict['_variable_kwargs']["value_factory"] if objcolumn_dict['_variable_kwargs']["value_factory"] == "Undef" else None
            resultado[objcolumn] = unainfo
        return resultado
        
    def _getPropertyName( self, aproperty ):
        '''
        devuelve el nombre de on objeto Property o false si no se encuentra
        @param aproperty:el objeto Property de storm
        '''
        #obtiene las columnas storm del dict de la clase
        stormcolumns = aproperty.cls.__dict__["_storm_columns"]
        dict_mother = aproperty.cls.__dict__
        for key in stormcolumns:
            #revisa que el valor sea igual al parametro
            if stormcolumns[key] is aproperty:
                #revisa dentro del parametro buscando la key
                for nombre in dict_mother:
                    if dict_mother[nombre] is key:
                        return nombre
        return False
    
    def getClassIdString( self ):
        '''
        @return: valor del id(ex:ide) en string
        '''
        atributes_info = self.getClassAttributesInfo().values()
        return [ atributo['name'] for atributo in atributes_info if atributo['primary'] == True][0]
    
    def _getReferenceName( self, reference ):
        '''
        devuelve el nombre de on objeto Reference o false si no se encuentra
        @param reference:el objeto Reference de storm
        '''
        dict_mother = reference.__dict__["_cls"].__dict__
        for elem in dict_mother :
            if dict_mother[elem] is reference:
                return elem
        return False
    
    def getAttributeName( self, property_or_reference ):
        """
        Obtiene el nombre en string de un property/reference.
        """        
        if type( property_or_reference ) == storm.references.Reference:
            return self._getReferenceName( property_or_reference )
        else:
            return self._getPropertyName( property_or_reference )
        
        
    def propertyToColumn( self, propiedad ):
        '''
        a partir de un propierty devuelve el column correspondiente
        @param propiedad:la propyerty
        '''
        nombreatributo = self._getPropertyName( propiedad )
        return self.CLASS.__dict__[nombreatributo]
    
    def _getTableSql( self ):
        """Crea el string SQL dinamicamente"""
        #puede haber algun problema ya que reference no tiene por que ser integer
        possiblesvaluestype = {
            "str":"VARCHAR",
            "int":"INTEGER",
            "reference":"INTEGER",
            "date":"VARCHAR",
            "float":"FLOAT"
        }
        possiblesvaluesprimary = {False:"", True:"PRIMARY KEY"}
        possiblevaluesnull = {False:"NOT NULL", True:""}
        
        info = self.getClassAttributesInfo()
        #CREA EL SQL DINAMICAMENTE
        tablestring = "("
        for columna in info:
            name = info[columna]["name"] if info[columna]["reference"] is False else info[columna]["name"] + "_id"
            elemento = ( name + " " + 
                possiblesvaluestype[info[columna]["type"]] + " " + 
                possiblesvaluesprimary[info[columna]["primary"]] + 
                possiblevaluesnull[info[columna]["null"]] + ",\n" )
            tablestring += elemento
        tablestring = tablestring[:-2] + ")"
        return tablestring
    