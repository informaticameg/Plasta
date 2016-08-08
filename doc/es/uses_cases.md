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

    id = Int(primary = True)
	name = Unicode()
	country_id = Int()
	country = Reference(country_id, Country.id)

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

En el archivo `gui.py`, solamente al cambiar el orden en que son definidos los atributos de la lista, ya se verán reflejados los cambios en la tabla.

```python
class PersonsGUI( BaseGUI ):

    def __init__(self, manager, managers = []):
        BaseGUI.__init__(self, manager, managers)

        [...]

        self.addTableColumn(u'#', Person.id)
        self.addTableColumn(u'Name', Person.name)
        self.addTableColumn(u'Last name', Person.last_name)
        self.addTableColumn(u'E-mail', Person.email)

        self._start_operations()
```

## Cambiar el nombre de los atributos mostrados en la lista

Solamente renombrando las claves en la llamada a la función 'addTableColumn', ya se reflejarán los cambios en la tabla.

```python
...
self.addTableColumn(u'#', Person.id)
self.addTableColumn(u'ChangeMe', Person.name)
...
```

## Cambiar el atributo principal de la clase 'id' por otro

Por defecto siempre se usa el atributo `id` para identificar a los objetos en la base de datos.

Veamos un ejemplo de como cambiar el atributo `id` por `isbn` en el caso de un libro:

```python
# clase con attributo 'ide'
class Book (object):

	id = Int(primary = True)

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
def fnParseDate(self, row, value):
	return value.strftime("%d/%m/%Y")

def fnParseAmount(self, row, value):
	return "$ %8.2f" % value

# usando la opción 'fnParse'
self.addTableColumn(u'Date', InvoiceRow.date, fnParse=self.fnParseDate) # type date
self.addTableColumn(u'Supplier', InvoiceRow.supplier) # type unicode
self.addTableColumn(u'Amount', InvoiceRow.amount, fnParse=self.fnParse) # type float
```
¿Como centramos una columna?
- 'C' para centrar
- 'L' para izquierda
- 'R' para derecha

```python
# usando la opción 'alignment'
self.addTableColumn(u'Amount', InvoiceRow.amount, alignment='C')
```

[Ir a > Inicio](https://github.com/informaticameg/Plasta/blob/master/doc/es/index.md) | [Ir a > Instalación](https://github.com/informaticameg/Plasta/blob/master/doc/es/install.md) | [Ir a > Como empezar](https://github.com/informaticameg/Plasta/blob/master/doc/es/getting_started.md) | [Ir a > Casos de uso](https://github.com/informaticameg/plasta/blob/master/doc/es/uses_cases.md) | [Ir a > Aplicaciones de ejemplo](https://github.com/informaticameg/plasta/blob/master/doc/es/example_apps.md)