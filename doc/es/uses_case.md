# Casos de uso

* Crear un objeto que contenga referencias
* Pasar una referencia de un modelo a otro
* Cambiar el orden de los atributos mostrados en la lista
* Cambiar el nombre de los atributos mostrados en la lista
* Cambiar el atributo principal de la clase 'ide' por otro 
* Formateando atributos en la lista

## Crear un objeto que contenga referencias

En este ejemplo se muestra como el objeto `Province` posee una referencia al objeto `Country` a través del atributo `Province.country`

```python
from storm.locals import *
from country import Country

class Province (object):

    __storm_table__ = "states"

    ide = Int(primary = True)
	name = Unicode()
	country_id = Int()
	country = Reference(country_id, Country.ide)

```

## Pasar una referencia de un modelo a otro

Varias veces necesitaremos interactuar datos de un modelo con otro. Veamos un ejemplo:

```python
from book.manager import BookManager
from book.gui import BookGUI
from library.manager import LibraryManager
from library.gui import LibraryGUI

book_mgr = BookManager(store, reset)
library_mgr = LibraryManager(store, reset)

books_gui = BookGUI(manager = book_mgr)
# here is passed by reference 'books_gui' to 'library_gui'
library_gui = LibraryGUI(manager = library_mgr, managers = [books_gui])

```

## Cambiar el orden de los atributos mostrados en la lista

En el archivo `gui.py`, solamente al cambiar el orden de los elementos en la lista `self.ATRIBUTOSLISTA` ya se verán reflejados los cambios en la tabla.

```python
class PersonsGUI( BaseGUI ):
    
    def __init__(self, manager, managers = []):
        BaseGUI.__init__(self, manager, managers)
        
        [...]
        
        self.ATRIBUTOSLISTA = [ 
	        {u'#':Person.ide},
	        {u'Name':Person.name},
	        {u'Last name':Person.last_name},
	        {u'E-mail':Person.email},
        ]
        self._start_operations()  
```

## Cambiar el nombre de los atributos mostrados en la lista

Solamente renombrando las claves dentro de la lista de diccionarios `self.ATRIBUTOSLISTA`, ya se reflejarán los cambios en la tabla.

```python
self.ATRIBUTOSLISTA = [ 
	{u'#':Person.ide},
    {u'ChangeMe':Person.name}
]
```

## Cambiar el atributo principal de la clase 'ide' por otro 

Por defecto siempre se usa el atributo `ide` para identificar a los objetos en la base de datos. 

Veamos un ejemplo de como cambiar el atributo `ide` por `isbn` en el caso de un libro:

```python
# clase con attributo 'ide'
class Book (object):
	
	ide = Int(primary = True)

# clase con atributo cambiado 'isbn'
class Book (object):
	
	isbn = Unicode(primary = True)
```

## Formateando atributos en la lista

Algunas veces necesitaremos dar formato a los atributos mostrados en la lista.

Veamos un ejemplo de como:
* dar el formato 'dd/mm/yyyy' a la columna fecha
* agregar el signo '$' a la columna 'monto'


```python
self.ATRIBUTOSLISTA = [ 
    {u'Date':InvoiceRow.date},         # type date
    {u'Supplier':InvoiceRow.supplier}, # type unicode
    {u'Amount':InvoiceRow.amount},     # type float
]

def fnParseDate(row, value):
	return value.strftime("%d/%m/%Y")

def fnParseAmount(row, value):
	return "$ %8.2f" % value

self.fnsParseListAttrs = [
	[0, fnParseDate], # 0, is the index of attr in self.ATRIBUTOSLISTA list
	[2, fnParseAmount]
]

```

[Ir a > Inicio](https://github.com/informaticameg/Plasta/blob/master/doc/es/index.md) | [Ir a > Instalación](https://github.com/informaticameg/Plasta/blob/master/doc/es/install.md) | [Ir a > Como empezar](https://github.com/informaticameg/Plasta/blob/master/doc/es/getting_started.md) | [Ir a > Casos de uso](https://github.com/informaticameg/plasta/blob/master/doc/es/uses_case.md) | [Ir a > Aplicaciones de ejemplo](https://github.com/informaticameg/plasta/blob/master/doc/es/example_apps.md)