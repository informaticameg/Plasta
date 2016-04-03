# Uses cases

* Create an object containing references
* Passing reference from one model to another
* Change the order of attributes displayed in the list
* Rename the attributes displayed in the list
* Change the main attribute of the class 'ide' by other
* Formatting attributes in the list

## Create an object containing references

In this example shown as `Province` object has a reference to the object` Country` through the attribute `Province.country`

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

## Passing reference from one model to another

Several times we need to interact with data from another model. Here is an example:

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

## Change the order of attributes displayed in the list

In the `gui.py`, only to change the order in which they are defined attributes list,  changes already be reflected in the table.

```python
class PersonsGUI( BaseGUI ):
    
    def __init__(self, manager, managers = []):
        BaseGUI.__init__(self, manager, managers)
        
        [...]
        
        self.addTableColumn(u'#', Person.ide)
        self.addTableColumn(u'Name', Person.name)
        self.addTableColumn(u'Last name', Person.last_name)
        self.addTableColumn(u'E-mail', Person.email)

        self._start_operations()  
```

## Rename the attributes displayed in the list

Only renaming the keys in the list of dictionaries `self.ATRIBUTOSLISTA`, and changes will be reflected in the table.

```python
...
self.addTableColumn(u'#', Person.ide)
self.addTableColumn(u'ChangeMe', Person.name)
...
```

## Change the main attribute of the class 'ide' by other

Always default `id` attribute to identify objects in the database is used.

Here is an example of how to change the attribute `ide` by `isbn` in the case of a book:

```python
# class with 'ide' attribute
class Book (object):
	
	ide = Int(primary = True)

# class with changed 'isbn' attribute
class Book (object):
	
	isbn = Unicode(primary = True)
```

## Formatting attributes in the list

Sometimes we need to format the attributes displayed in the list.

See an example of how:
* give the format 'dd/mm/yyyy' to date column
* add '$' sign to 'amount' column

Veamos un ejemplo de como:
* dar el formato 'dd/mm/yyyy' a la columna fecha
* agregar el signo '$' a la columna 'monto'


```python
def fnParseDate(self, row, value):
	return value.strftime("%d/%m/%Y")

def fnParseAmount(self, row, value):
	return "$ %8.2f" % value

self.addTableColumn(u'Date', InvoiceRow.date, fnParse=self.fnParseDate) # type date
self.addTableColumn(u'Supplier', InvoiceRow.supplier) # type unicode
self.addTableColumn(u'Amount', InvoiceRow.amount, fnParse=self.fnParse) # type float
```

[Go > Index](https://github.com/informaticameg/Plasta/blob/master/doc/en/index.md) | [Go > Install](https://github.com/informaticameg/Plasta/blob/master/doc/en/install.md) | [Go > Getting started](https://github.com/informaticameg/Plasta/blob/master/doc/en/getting_started.md) | [Go > Use cases](https://github.com/informaticameg/plasta/blob/master/doc/en/uses_cases.md) | [Go > Example Apps](https://github.com/informaticameg/plasta/blob/master/doc/en/example_apps.md)