## Un ejemplo mas complejo sobre el uso de Plasta.

Se trata de un gestor de movimientos, donde se manejan cuentas de ingreso
y egreso. Permitiendo dar de alta movimientos para cada cuenta y poder
filtrarlos por fecha, tipo de cuenta y tipo de movimiento.

# Este ejemplo implementa:

- Relacion entre objetos.
- Reimplementación de metodos Plasta.
- Extención de clases Manager.
- Personalización de atributos mostrados en lista.

# Este ejemplo contiene las siguientes partes:

	/balance        -> paquete que contiene la logica de los balances
	/cuenta         -> paquete con todas las definiciones para este objeto
	/GUI            -> contiene la pantalla central
	/movimiento     -> paquete con todas las definiciones para este objeto
	/seccion        -> paquete con todas las definiciones para este objeto
	/tools          -> librerias extra usadas
	data.db         -> archivo de la base de datos
	managers.py     -> contiene las instancias de cada <manager>
	run.py          -> ejecuta el programa

NOTA: Para ejecutar este ejemplo, agregar el paquete `plasta` y `storm`
a esta misma carpeta.

¡Disfrútalo!