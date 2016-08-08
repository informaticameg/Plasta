# Getting started

## Creating the first package Plasta

## Structure of a CRUD

Each CRUD is made up of a Python package, that contains the follow structure:
* Object Class (e.g.: Client).
* Manager Class (e.g.: ClientsManager)
* Main Class of the CRUD (e.g.: ClientsGUI)
* Adding a Record Class (e.g.: AddClient)
* Qt's .ui File for <add client> screen.

Then the resulting package would be something like this:
```
/client
|--- __init__.py
|--- manager.py
|--- gui.py
|--- add.py
|--- add.ui
```

**Below is detailed as each consist of the package files:**

**1. Creating the __init__.py file**

Continuing with the example of "Client", the first thing we do is create a Python package for the Client object: create the `/client` folder and within it, create the file` __init __ py`.

The code for the file would look something like:

```python
from storm.locals import *

class Client (object):

	# table name in the database for this object
	__storm_table__ = "client"

	# attributes of the class
	ide = Int(primary = True)
	names = Unicode(allow_none = False)
	phone = Unicode()
	address = Unicode()
	zone = Int()

  	def __init__(self, names, phone, address, zone):
      self.names = names
      self.phone = phone
      self.address = address
      self.zone = zone

	# value to be displayed when you invoke this function
	def __str__(self):
		return self.names
```

While wearing Storm as ORM, Plasta will adjust to how this technology
behave.

**2. Creating the manager.py file**

Once the Client object made, we create the controller class
for this object.

By convention we use the name `CustomersManager`. Would look something like:

```python
from plasta.logic.manager import BaseManager
from client import Client

class ClientsManager( BaseManager ):

	def __init__( self, store, reset = False ):
		BaseManager.__init__( self, store, reset )
		# object to be handled by this controller
		self.CLASS = Client
		self._start_operations()

```

This would be the basic structure of a class manager. The only thing that would change each case is the class name and the object that controls (self.CLASS).

Up to this point we have the two list of the “logic” It is needed to perform operations to add, edit, delete and search.

Now we will see how we connect this with the graphical interface.

**3. Creating the gui.py file**

Create the gui.py file and rename the class to “ClientsGUI”:

```python
from plasta.gui import BaseGUI
from client import Client
from client.add import AddClient

class ClientsGUI(BaseGUI):

	def __init__(self, manager, managers = []):
		# calls the base class constructor
		BaseGUI.__init__(self, manager, managers)
		# class display to add and edit dialogs
		self.DialogAddClass = AddClient
        # read and get up ui file information
        self.loadUI()

		# attributes used as filters
        self.addFiler(u'Names', Client.names)
        self.addFiler(u'Phone', Client.phone)
        self.addFiler(u'Address', Client.address)
        self.addFiler(u'Zone', Client.zone)

        # columns / attributes shown in the list
        self.addTableColumn(u'#', Cliente.ide, alignment='C')
        self.addTableColumn(u'Names', Client.names)
        self.addTableColumn(u'Phone', Client.phone)
        self.addTableColumn(u'Address', Client.address)
        self.addTableColumn(u'Zone', Client.zone, alignment='C')

		# performs operations start to lift the window
		self._start_operations()
```

**4. Creating the add.py file**

Finally create the add.py file, and its contents would be this:

```python
from plasta.gui.add import BaseAdd
from client import Client

class AddClient(BaseAdd):

	def __init__(self, manager, itemToEdit = False, managers = []):
		# base class constructor
		BaseAdd.__init__(self, manager, itemToEdit)
		# read and get up ui file information
		self.loadUI('client/add.ui')

    # here indicate what interface widget
    # it corresponds to an attribute of the class
		self.linkToAttribute(self.leNames, Cliente.names)
		self.linkToAttribute(self.lePhone, Cliente.phone)
		self.linkToAttribute(self.leAddress, Cliente.address)
		self.linkToAttribute(self.leZone, Cliente.zone)

		self._start_operations()
```

Importantly, with the `self.linkToAttribute` function indicate how widget will correspond to the class attribute are handling.
To that adding a record, the value in the widget, it is established in that attribute of the object.

**Is necessary** the order in which items are indicated it corresponds to the order of the parameters in the constructor of the class of object you are working with.

Using the Plasta generator to create this package, the command would be:

`$ python plastagen g crud client names phone address zone`


**5. Creating the run.py file**

Finally we will create the file that runs the application:

```python
import sys
from PyQt4 import QtGui
from storm.locals import create_database, Store

from client.manager import ClientsManager
from client.gui import ClientsGUI

# object Store of Storm
DATABASE = create_database('sqlite: test.db')
store = Store(DATABASE)

# manager instance of ClientsGUI
cm = ClientsManager(store, reset = True)

# displaying the window
app = QtGui.QApplication(sys.argv)
window = ClientsGUI( manager = cm, managers = [] )
window.show()
sys.exit(app.exec_())

```

[Go > Index](https://github.com/informaticameg/Plasta/blob/master/doc/en/index.md) | [Go > Install](https://github.com/informaticameg/Plasta/blob/master/doc/en/install.md) | [Go > Getting started](https://github.com/informaticameg/Plasta/blob/master/doc/en/getting_started.md) | [Go > Use cases](https://github.com/informaticameg/plasta/blob/master/doc/en/uses_cases.md) | [Go > Example Apps](https://github.com/informaticameg/plasta/blob/master/doc/en/example_apps.md)