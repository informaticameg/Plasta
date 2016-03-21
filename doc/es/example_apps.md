
# Aplicaciones de ejemplo

## Agenda de contactos

> Un ejemplo simple sobre el uso de Plasta.

Se trata de una sencilla agenda de contactos para manejar las operaciones basicas de
agregar, editar, eliminar y buscar soportadas por Plasta por defecto.

### Este ejemplo implementa:

- Definición simple de un objeto.
- No reimplementa metodos Plasta.
- No extiende funcionalidad de la clase Manager.
- Personalización de atributos mostrados en lista.

### Este ejemplo contiene las siguientes partes:

	/contacto       -> paquete que contiene la logica de los contactos
	contactos.db    -> archivo de la base de datos
	run.py          -> ejecuta el programa

Puedes encontrar este ejemplo en la carpeta `/examples/Agenda-de-contactos`

## Gestor de movimientos

> Un ejemplo mas complejo sobre el uso de Plasta.

Se trata de un gestor de movimientos, donde se manejan cuentas de ingreso
y egreso. Permitiendo dar de alta movimientos para cada cuenta y poder
filtrarlos por fecha, tipo de cuenta y tipo de movimiento.

### Este ejemplo implementa:

- Relacion entre objetos.
- Reimplementación de metodos Plasta.
- Extención de clases Manager.
- Personalización de atributos mostrados en lista.

### Este ejemplo contiene las siguientes partes:

	/balance        -> paquete que contiene la logica de los balances
	/cuenta         -> paquete con todas las definiciones para este objeto
	/GUI            -> contiene la pantalla central
	/movimiento     -> paquete con todas las definiciones para este objeto
	/seccion        -> paquete con todas las definiciones para este objeto
	/tools          -> librerias extra usadas
	data.db         -> archivo de la base de datos
	managers.py     -> contiene las instancias de cada <manager>
	run.py          -> ejecuta el programa

Puedes encontrar este ejemplo en la carpeta `/examples/Gestor-de-movimientos`