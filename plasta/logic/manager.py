#!/usr/bin/env python
# -*- coding: utf-8 -*-

from storm.locals import * #@UnusedWildImport
import storm
from storm.exceptions import OperationalError
from plasta.config import config


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
        self.store = almacen
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
            self.store.execute('DROP TABLE IF EXISTS %s;' % nombredetabla, noresult=True)
        except OperationalError, e:
            print e
        #CREO NUEVAMENTE LA TABLA
        self.store.execute('CREATE TABLE ' + nombredetabla + ' ' + SQL )
        self.store.commit()

    def getClassName( self ):
        '''
        devuelve el nombre de la clase que maneja
        @return: str
        '''
        return self.CLASS.__name__

    def getDataObject( self, obj, columns, rformat='dict'):
        '''
        obtiene y devuelve una lista de los datos obtenidos a partir de las
        columnas y de los datos que maneja
        @param obj:objeto instancia a extrer ex:unCliente
        @param columns:storm columns :ex:[Cliente.ide,Cliente.nombres]
        @param format: dict | list
        @return: lista de dic: [{"ide":1},{"nombres":nombrecliente}]
        '''
        if isinstance( obj, self.CLASS ):
            values = {} if rformat == 'dict' else []
            for propiedad in columns:
                nombreatributo = self.getAttributeName( propiedad )
                if rformat == 'dict':
                    values[nombreatributo] = obj.__getattribute__( nombreatributo )
                else:
                    values.append( {nombreatributo:obj.__getattribute__( nombreatributo )} )
            return values
        else:
            raise Exception( "No se pudo obtener los valores debido a que no es una instancia correcta" )

    def getClassAttributesValues( self, obj, rformat='list'):
        '''
        obtiene los valores del obj
        @param obj:a obj de type
        @param rformat: formato a retornar el valor > list | dict
        @return: list o dict
        '''
        if isinstance( obj, self.CLASS ):
            if rformat == 'list':
                return [obj.__getattribute__( p ) for p in self.getClassAttributes()]
            elif rformat == 'dict':
                result = {}
                for p in self.getClassAttributes():
                    result[p] = obj.__getattribute__( p )
                return result
        else:
            raise Exception( "no se pudo obtener los valores" )

    def checkIfExists(self, obj):
        '''
        Comprueba que el objeto indicado exista en la base de datos
        '''
        result = self.getById(obj.id)
        return result is not None, result


#=======================================================================
# Generic Methods
#=======================================================================

    def add( self, params, commit=True):
        '''
        Crea y agrega un objeto al almacen
        @param *params: los parametros que recibe el init de self.CLASS
        @return: true o false, dependiendo si se completo la operacion
        '''
        try:
            if type(params) is list:
                obj = self.CLASS( *params )
            elif type(params) is dict:
                obj = self.CLASS( **params )
            obj = self.store.add( obj )
            if commit:
                self.store.flush()
                self.store.commit()
            return obj
        except Exception, e:
            print e
            return False

    def delete( self, obj ):
        '''
        borra un objeto de la bd y de la ram
        @param obj:un objeto del tipo self.CLASS
        '''
        if isinstance( obj, self.CLASS ):
            self.store.remove( obj )#where o is the object representing the row you want to remove
            del obj#lo sacamos de la ram
            self.store.commit()
            return True
        return False

    def count( self ):
        '''
        obtiene la cantidad de objetos de este manager
        @return: int
        '''
        query = 'select count(*) from %s' % self.CLASS.__storm_table__
        return [o for o in self.store.execute(query)][0][0]

    def getall( self ):
        '''
        obtiene todos los objetos de este manager
        @return: lista de objs
        '''
        return [obj for obj in self.store.find( self.CLASS )]

    def get( self, nombre ):
        '''
        obtiene los objetos donde "nombre" coincide con self.searchname
        @param nombre:str o int
        @return: list of obj
        '''
        if not self.searchname:
            self.searchname = self.CLASS.nombre
        return self.searchBy( self.searchname, nombre )

    def getById(self, ide):
        '''
        Retorna el objeto segun el <ide> indicado
        '''
        return self.store.find(self.CLASS, self.CLASS.id == ide).one()

    def searchBy( self, column, nombre ):
        '''
        Realiza una busqueda por column segun el valor nombre
        @param column:a storm column
        @param nombre:str o int
        @return: lista de objetos
        '''
        if type( column ) == storm.references.Reference:
            objs = self.getall()
            value = self._getReferenceName( column )
            return [obj for obj in objs if obj.__getattribute__(value).__str__().lower().find(value) != -1]
        if nombre != "":
            import datetime
            if (type( nombre ) is unicode) or (type( nombre ) is str):
                return [obj for obj in self.store.find( self.CLASS, column.like( unicode( u"%" + nombre + u"%" ) ) )]
            elif type( nombre ) in [int, datetime.datetime, datetime.date] :
                return [obj for obj in self.store.find( self.CLASS, column == nombre )]
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

    def _getTableSql( self, engine=None):
        """Crea el string SQL dinamicamente"""

        # for more info of database types see:
        # https://storm.canonical.com/Manual#Table_of_properties_vs._python_vs._database_types
        from plasta.config import config
        db = config.DB_ENGINE
        if engine:
            db = engine
        possiblesvaluestype = {
            'sqlite':{
                "str":"VARCHAR",
                "int":"INTEGER",
                "reference":"INTEGER",
                "date":"VARCHAR",
                "datetime":"VARCHAR",
                "bool":"INTEGER",
                "float":"FLOAT"
            },
            'mysql':{
                "str":"TEXT",
                "int":"INT",
                "reference":"INT",
                "date":"DATE",
                "datetime":"DATETIME",
                "bool":"TINYINT(1)",
                "float":"FLOAT"
            },
            'postgres':{
                "str":"VARCHAR",
                "int":"INT",
                "reference":"INT",
                "date":"DATE",
                "datetime":"TIMESTAMP",
                "bool":"BOOL",
                "float":"FLOAT"
            }
        }
        possiblesvaluesprimary = {False:""}
        if db in ['sqlite', 'postgres']:
            possiblesvaluesprimary[True] = "PRIMARY KEY"
        else: #mysql
            possiblesvaluesprimary[True] = "PRIMARY KEY AUTO_INCREMENT"
        possiblevaluesnull = {False:"NOT NULL", True:""}

        info = self.getClassAttributesInfo()
        #CREA EL SQL DINAMICAMENTE
        tablestring = "("
        for columna in info:
            name = info[columna]["name"] if info[columna]["reference"] is False else info[columna]["name"] + "_id"
            elemento = ( name + " " +
                possiblesvaluestype[db][info[columna]["type"]] + " " +
                possiblesvaluesprimary[info[columna]["primary"]] +
                possiblevaluesnull[info[columna]["null"]] + ",\n" )
            tipo = possiblesvaluestype[db][info[columna]["type"]]
            if (db == 'mysql') and (name == 'id') and (tipo == possiblesvaluestype[db]['str']):
                elemento = elemento.replace('AUTO_INCREMENT', '')
                elemento = elemento.replace('TEXT', 'VARCHAR(10)')
            tablestring += elemento
        tablestring = tablestring[:-2] + ")"
        return tablestring
