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

from storm.locals import * #@UnusedWildImport
import storm
from storm.exceptions import OperationalError


class BaseManager( object ):
    '''
    Clase base para manager de una clase storm
    @param seachname: atributo por el cual buscara el metodo get()
    @param reset: si es true limpia y crea la bd
    '''

    def __init__( self, almacen, reset = False ):
        ''''''
        #@param CLASS: la clase que va a manipular ej:Cliente
        self.CLASS = None
        #@param CLASSATTRIBUTES: las columnas que va usar (DONTTOUCH)
        self.CLASSATTRIBUTES = []
        #@param searchname: lacolumna por la cual el metodo get hace la busqueda ej=Cliente.nombres
        self.searchname = None

        #@param almacen: el objeto STORE de storm
        self.almacen = almacen
        #@param reset: variable que determina si se va a resetear
        self.reset = reset
        # definir aqui referencias hacia otros modelos
        # será usado para la eliminacion por referencia
        # ej: [{'model':'Client', 'attr':'client', 'type':'id'}, ...]
        # types = id, json
        self.references = []

    def _start_operations( self ):
        '''
        operaciones que se requieren para iniciar el manager
        '''
        if self.reset:
            self._reset()
        print "Manager de %s levantado correctamente" % self.CLASS
        #@param CLASSid: la clave primaria de la clase ej:"ide"
        self.CLASSid = self.getClassIdString()

#=======================================================================
# Methods exclusive Plasta
#=======================================================================


    def _reset( self ):
        '''
        borra y vuelve a crear la tabla
        '''
        SQL = self._getTableSql()
        nombredetabla = self.CLASS.__storm_table__
        #ELIMINO LA TABLA
        try:
            self.almacen.execute( 'DROP TABLE ' + nombredetabla )
        except OperationalError, e:
            print e
        #CREO NUEVAMENTE LA TABLA
        self.almacen.execute( 'CREATE TABLE ' + nombredetabla + ' ' + SQL )
        self.almacen.commit()

    def getClassName( self ):
        '''
        devuelve el nombre de la clase que maneja
        @return: str
        '''
        return self.CLASS.__name__

    def getDataObject( self, obj, columns ):
        '''
        obtiene y devuelve una lista de los datos obtenidos a partir de las
        columnas y de los datos que maneja
        @param obj:objeto instancia a extrer ex:unCliente
        @param columns:storm columns :ex:[Cliente.ide,Cliente.nombres]
        @return: lista de dic: [{"ide":1},{"nombres":nombrecliente}]
        '''
        if isinstance( obj, self.CLASS ):
            listpropiertisvalues = []
            for propiedad in columns:
                nombreatributo = self.getAttributeName( propiedad )
                listpropiertisvalues.append( {nombreatributo:obj.__getattribute__( nombreatributo )} )
            return listpropiertisvalues
        else:
            raise Exception( "No se pudo obtener los valores debido a que no es una instancia correcta" )

    def getClassAttributesValues( self, obj ):
        '''
        obtiene los valores de el obj
        @param obj:a obj de type 
        @return: a list of values
        '''
        if isinstance( obj, self.CLASS ):
            return [obj.__getattribute__( p ) for p in self.getClassAttributes()]
        else:
            raise Exception( "no se pudo obtener los valores" )
        
#=======================================================================
# Generic Methods  
#=======================================================================

    def add( self, *params ):
        '''
        Crea y agrega un objeto al almacen
        @param *params: los parametros que recibe el init de self.CLASS
        @return: true o false, dependiendo si se completo la operacion
        '''
        try:
            obj = self.CLASS( *params )
            self.almacen.add( obj )
            self.almacen.flush()
            self.almacen.commit()
            return True
        except Exception, e:
            print e
            return False
        
    def delete( self, obj ):
        '''
        borra un objeto de la bd y de la ram
        @param obj:un objeto del tipo self.CLASS
        '''
        if isinstance( obj, self.CLASS ):
            self.almacen.remove( obj )#where o is the object representing the row you want to remove
            del obj#lo sacamos de la ram
            self.almacen.commit()
            return True
        return False

    def count( self ):
        '''
        obtiene la cantidad de objetos de este manager
        @return: int
        '''
        return len(self.getall())

    def getall( self ):
        '''
        obtiene todos los objetos de este manager
        @return: lista de objs
        '''
        return [obj for obj in self.almacen.find( self.CLASS )]

    def get( self, nombre ):
        '''
        obtiene los objetos donde "nombre" coincide con self.searchname
        @param nombre:str o int
        @return: list of obj
        '''
        if not self.searchname:
            self.searchname = self.CLASS.nombre
        return self.searchBy( self.searchname, nombre )

    def searchBy( self, column, nombre ):
        '''
        hace una busqueda e el atributo column por el valor nombre
        @param column:a storm column
        @param nombre:str o int
        @return: lista de objetos
        '''
        if type( column ) == storm.references.Reference:
            objs = self.getall()
            name = self._getReferenceName( column )
            return [obj for obj in objs if nombre in obj.__getattribute__( name ).__str__()]
        if nombre != "":
            import datetime
            if (type( nombre ) is unicode) or (type( nombre ) is str):
                return [obj for obj in self.almacen.find( self.CLASS, column.like( unicode( u"%" + nombre + u"%" ) ) )]
            elif type( nombre ) is int :
                return [obj for obj in self.almacen.find( self.CLASS, column == nombre )]
            elif ( type( nombre ) is datetime.datetime ) or ( type( nombre ) is datetime.date ):
                return [obj for obj in self.almacen.find( self.CLASS, column == nombre )]
            else:
                raise Exception, u"Exception:No se busco adecuadamente debido a que el tipo de criterio es: " + unicode( type( nombre ) )
        else:
            return self.getall()

#=======================================================================
# Inspection Methods
#=======================================================================

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
                    storm.properties.Float : 'float',
                    storm.properties.DateTime : 'datetime'
                }
                unainfo["type"] = types[ type(objcolumn) ]
            unainfo["name"] = name
            unainfo['primary'] = objcolumn.__dict__['_primary'] if "_primary" in objcolumn.__dict__ else False
            unainfo["null"] = objcolumn.__dict__['_variable_kwargs']["allow_none"] if "allow_none" in objcolumn.__dict__['_variable_kwargs'] else True
            unainfo["default"] = objcolumn.__dict__['_variable_kwargs']["value_factory"] if objcolumn.__dict__['_variable_kwargs']["value_factory"] == "Undef" else None
            resultado[objcolumn] = unainfo
        return resultado

    def _getPropertyName( self, propiedad ):
        '''
        devuelve el nombre de on objeto Property o false si no se encuentra
        @param aproperty:el objeto Property de storm
        '''
        #obtiene las columnas storm del dict de la clase
        try:
            propiedad_dict = propiedad.cls.__dict__
            stormcolumns = propiedad_dict["_storm_columns"]
        except AttributeError, e:
            propiedad_dict = propiedad._cls.__dict__
            stormcolumns = propiedad_dict["_storm_columns"]
        if not str(type(propiedad)) == "<class 'storm.references.Reference'>" :
            for key in stormcolumns:
                if stormcolumns[key] is propiedad:
                    for nombre in propiedad_dict:
                        if propiedad_dict[nombre] is key:
                            return nombre
        else:
            for nombre in propiedad_dict:
                if propiedad_dict[nombre] is propiedad:
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
        for elem in  reference.__dict__["_cls"].__dict__:
            if reference.__dict__["_cls"].__dict__[elem] is reference:
                return elem

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
            "bool":"INTEGER",
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
