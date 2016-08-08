
# Examples apps

## Contact list

> A simple example about use of Plasta.

It is a simple contact list to handle the basic operations add, edit, delete and search Plasta supported by default.

### This example implements:

- Simple definition of an object.
- No reimplements methods Plasta.
- No functionality extends the Manager class.
- Customizing attributes shown in list.

### This example contents the following parts:

	/contact        -> package containing the logic of the contacts
	contactos.db    -> database file
	run.py          -> run the program

Can find this example in the folder `/examples/Agenda-de-contactos`

## Movements manager

> A more complex example about use of Plasta.

This is a manager of movements, where entry and exit accounts are handled. Allowing to register movements for each account and filter them by date, account type and type of movement.

### This example implements:

- Relationship between objects.
- Reimplementation of methods Plasta.
- Extension Manager classes.
- Customizing attributes shown in list.

### This example contents the following parts:

	/balance        -> package containing the logic of the balance
	/cuenta         -> package with all definitions for this object
	/GUI            -> containing the main screen
	/movimiento     -> package with all definitions for this object
	/seccion        -> package with all definitions for this object
	/tools          -> extra librarys used
	data.db         -> database file
	managers.py     -> cantaining the instances of each <manager>
	run.py          -> run the program

Can find this example in the folder  `/examples/Gestor-de-movimientos`

[Go > Index](https://github.com/informaticameg/Plasta/blob/master/doc/en/index.md) | [Go > Install](https://github.com/informaticameg/Plasta/blob/master/doc/en/install.md) | [Go > Getting started](https://github.com/informaticameg/Plasta/blob/master/doc/en/getting_started.md) | [Go > Use cases](https://github.com/informaticameg/plasta/blob/master/doc/en/uses_cases.md) | [Go > Example Apps](https://github.com/informaticameg/plasta/blob/master/doc/en/example_apps.md)