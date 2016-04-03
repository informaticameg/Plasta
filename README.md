# Plasta

<img src="https://raw.github.com/informaticameg/plasta/master/resources/plasta.png" />

Plasta is a framework written in Python for rapid deployment of [CRUDs]((http://en.wikipedia.org/wiki/Create,_read,_update_and_delete)) in a simple way, in a few steps and in few lines of code.

Is designed with the MVC pattern and the DRY (Don't Repeat Yourself) development
technique.

## Sinopsis

In software engineering we often find the task of performing various CRUD (Create, read, update and delete) in the development of a typical management system or application. This leads to the repetitive task of writing the same operations over and over again for each CRUD being performed, increasing deployment time, lines of code, risk of errors and increased maintenance.
Plasta born to cover the task of automating these processes.

It focuses on both deployment and maintenanceof an aplication is minimized, for this the core of Plasta is designed so that at any time, if necessary, you can reimplement any method that does not meet our interests. Leaving it open to the possibility of a more comfortable development.

## Database Support

Using [Storm ORM](https://storm.canonical.com/), Plasta is conditioned by the support that offers this technology on databases.

For more info see the official [documentation](https://storm.canonical.com/Manual) of Storm.


## GUI Support

Plasta uses the graphic library Qt on graphic interfaces.

Has a number of Qt's .ui files by default ready for use.

## Resuming technical features

- [Storm](https://storm.canonical.com/) in the persistence.

- PyQt4 in GUIs.

## Structure of a CRUD

Each CRUD is made up of a Python package, that contains the follow structure:
* Object class (e.g.: Client).
* Manager class (e.g.: ClientsManager)
* Main class of the gui CRUD (e.g.: ClientsGUI)
* Adding a record class (e.g.: AddClient)
* Qt's .ui file for <add client> screen.

Then the resulting package would be something like this:
```
/client
|--- __init__.py
|--- manager.py
|--- gui.py
|--- add.py
|--- add.ui
```

**With this structure we're ready to manage Client objects and working with them.**

See [Creating the first package Plasta]() for more details.

## Not implemented yet

* Support for cross object references.

## Requirements

Plasta requires:
* Python 2.5 or higher.
* Storm 0.19. Download [here](https://launchpad.net/storm/+download).
* PyQt 4.7. Download [here](http://www.riverbankcomputing.co.uk/software/pyqt/download).

## Install


### From pip (TODO)
```sh
$ pip install plasta
```

### From Github

```sh
$ wget https://github.com/informaticameg/Plasta/archive/master.zip
$ tar xvf six-1.0b1.tar.gz 
$ cd plasta/
$ python setup.py install
```

## Wiki

Check the Plasta wiki in [English](https://github.com/informaticameg/Plasta/blob/master/doc/en/index.md) or [Spanish](https://github.com/informaticameg/Plasta/blob/master/doc/es/index.md) version.

## Plasta Social

* Follow us on [Twitter](https://twitter.com/PlastaFramework)

## License


    Copyright (C) 2012 by Informática MEG <contacto@informaticameg.com>
	
	MIT Licence

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

**Plasta is maintained by:**
* Jonathan Ferreyra <jalejandroferreyra@gmail.com> 
	* GitHub [@jonathanferreyra](https://github.com/jonathanferreyra)
* Emiliano Fernandez <emilianohfernandez@gmail.com>
	* GitHub [@emilianox](https://github.com/emilianox)

## Logo licence
	
	Plasta logo is licenced under the terms of Creative Commons licence.

	Copyright (C) 2012 by Cecilia Schiebel <ceciliaschiebel@gmail.com>

	