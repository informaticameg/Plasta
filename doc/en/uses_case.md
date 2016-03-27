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

In the `gui.py`, file only to change the order of items in the list `self.ATRIBUTOSLISTA` changes already be reflected in the table.

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

## Rename the attributes displayed in the list

Only renaming the keys in the list of dictionaries `self.ATRIBUTOSLISTA`, and changes will be reflected in the table.

```python
self.ATRIBUTOSLISTA = [ 
	{u'#':Person.ide},
    {u'ChangeMe':Person.name}
]
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