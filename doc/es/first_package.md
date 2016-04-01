# Como Empezar

## Creando el primer paquete Plasta


### Estructura de un ABM

Cada ABM se conforma por un paquete Python, que contiene la siguiente estructura:
* Clase Objeto (Ejemplo: Cliente).
* Clase Controladora (Ejemplo: ClientesManager)
* Clase Main del ABM (Ejemplo: ClientesGUI)
* Clase para dar de alta un registro (Ejemplo: AddCliente)
* Archivo .ui de Qt para la pantalla del <agregar cliente>.

El paquete resultante entonces quedaría algo así:

```
/cliente
|--- __init__.py
|--- manager.py
|--- gui.py
|--- add.py
|--- add.ui
```


**A continuación se detalla como se componen cada uno de los archivos del paquete:**

**1. Creando el archivo __init__.py**

Continuando con el ejemplo de “Cliente”, lo primero que haremos es crear un paquete Python para el objeto Cliente: creamos la carpeta `/cliente` y dentro de ella, creamos el archivo `__init__.py`. 

El código para el archivo sería algo así:

```python
from storm.locals import *

class Cliente (object):

	# nombre que tendrá la tabla en la BD para este objeto
	__storm_table__ = "cliente"

	# atributos de la clase
	ide = Int(primary = True)
	nombres = Unicode(allow_none = False)
	telefono = Unicode()
	domicilio = Unicode()
	zona = Int()
	
  	def __init__(self, nombres, telefono, domicilio, zona):
    	self.nombres = nombres
	    self.telefono = telefono
    	self.domicilio = domicilio
	    self.zona = zona
	
	# valor que se mostrará al invocar esta función
	def __str__(self):
		return self.nombres
```

Al estar usando Storm como ORM, Plasta se ajustará a cómo esta tecnología se
comporte.

**2. Creando el archivo manager.py**

Una vez hecho el objeto Cliente, pasamos a crear la clase controladora
para este objeto. 

Por convención usaremos el nombre `ClientesManager`. Quedando algo
así:

```python
from plasta.logic.manager import BaseManager
from cliente import Cliente

class ClientesManager( BaseManager ):

	def __init__( self, store, reset = False ):
		BaseManager.__init__( self, store, reset )
		# objeto a ser manejado por este controlador
		self.CLASS = Cliente
		self._start_operations()

```

Esta sería la estructura base de una clase manager. Lo único que cambiaría para
cada caso es: el nombre de la clase y el objeto que controla (self.CLASS).

Hasta aquí tenemos listas las dos clases de la “lógica” que se necesitan para poder
realizar las operaciones de agregar, editar, eliminar y buscar.

Ahora veremos cómo conectamos esto con la interfaz gráfica.

**3. Creando el archivo gui.py**

Creamos el archivo gui.py y renombramos la clase a “ClientesGUI”:

```python
from plasta.gui import BaseGUI
from cliente import Cliente
from cliente.add import AddCliente

class ClientesGUI(BaseGUI):

	def __init__(self, manager, managers = []):
		# llama al costructor de la clase base
		BaseGUI.__init__(self, manager, managers)

		# clase que mostrará a los diálogos de agregar y editar
		self.DialogAddClass = AddCliente
		
		# atributos usados como filtros
        self.ATRI_COMBO_BUSQUEDA = [ 
	        {u'Nombres':Cliente.nombres},
	        {u'Telefono':Cliente.telefono},
	        {u'Dirección':Cliente.direccion},
	        {u'Zona':Cliente.zona},
        ]

        # alineación de los atributos en la lista
		# C = CENTER, L = LEFT, R = RIGHT
        self.ALINEACIONLISTA = ['C','L','L','L','C']        
        
        # columnas/atributos mostrados en la lista
        self.ATRIBUTOSLISTA = [ 
	        {u'#':Cliente.ide},
	        {u'Nombres':Cliente.nombres},
	        {u'Telefono':Cliente.telefono},
	        {u'Dirección':Cliente.direccion},
	        {u'Zona':Cliente.zona},
        ]

		# realiza las operaciones de inicio para levantar la ventana
		self._start_operations()
```

**4. Creando el archivo add.py**

Por último crearemos el archivo add.py, y su contenido sería este:

```python
from os.path import join, abspath, dirname
from PyQt4 import uic
from plasta.gui.add_window import BaseAdd
from cliente import Cliente

class AddCliente(BaseAdd):

	def __init__(self, manager, itemToEdit = False, managers = []):
		# constructor de la clase base
		BaseAddWindow.__init__(self, manager, itemToEdit)
		# ubicación del archivo ui para esta ventana
		FILENAME = 'add.ui'
		# lee y levanta la información del archivo ui
		uic.loadUi( join(abspath(dirname(__file__)), FILENAME), self )

		# aquí indicaremos qué widget de la interfaz 
		# se corresponde con un atributo de la clase
		self.ITEMLIST = [
			{self.leNombres : Cliente.nombres},
			{self.leTelefono : Cliente.telefono},
			{self.leDomicilio : Cliente.domicilio},
			{self.leZona : Cliente.zona}
		]
		
		self._start_operations()
```

Es importante destacar que en `self.ITEMLIST` indicaremos con qué widget se corresponderá que atributo de la clase que estamos manejando. 
Para que cuando se de alta un registro, el valor contenido en ese widget, se establezca en ese atributo del objeto.

**Es necesario** que el orden en que estén indicados los items, se corresponda con el orden de los parámetros en el constructor de la clase del objeto con el que se este trabajando.

Usando el generador de Plasta para crear este paquete, el comando sería el siguiente:

`$ python plastagen plastagen g crud cliente nombres telefono domicilio zona`


**5. Creando el archivo run.py**

Por último crearemos el archivo que ejecutará la aplicación: 

```python
import sys
from PyQt4 import QtGui
from storm.locals import create_database, Store

from cliente.manager import ClientesManager
from cliente.gui import ClientesGUI

# objeto Store de Storm
DATABASE = create_database('sqlite: prueba.db')
store = Store(DATABASE)

# instancia del manager de ClientesGUI
cm = ClientesManager(store, reset = True)

# mostrando la ventana
app = QtGui.QApplication(sys.argv)
window = ClientesGUI( manager = cm, managers = [] )
window.show()
sys.exit(app.exec_())

```



[Ir a > Inicio](https://github.com/informaticameg/Plasta/blob/master/doc/es/index.md) | [Ir a > Instalación](https://github.com/informaticameg/Plasta/blob/master/doc/es/install.md) | [Ir a > Como empezar](https://github.com/informaticameg/Plasta/blob/master/doc/es/getting_started.md) | [Ir a > Casos de uso](https://github.com/informaticameg/plasta/blob/master/doc/es/uses_case.md) | [Ir a > Aplicaciones de ejemplo](https://github.com/informaticameg/plasta/blob/master/doc/es/example_apps.md)