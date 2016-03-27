# Getting started

## Choosing the structure of the application

Plasta is not subject to a defined structure, while respecting the structure of the object plasta, the rest is up to you is maintained.
Anyway we show two possible structures that you can use:

### Simple structure

```
/myapp
  /object1
  /object2
  /object3
  mainwindow.py  # controlling class of the main window
  mainwindow.ui  # ui file of the main window
  run.py         # running the application
```


You can download this structure from [here]().

### MVC structure type

```
/myapp
  /models
  .  /object1
  .  .  __init__.py # storm class
  .  .  manager.py  # manager class of objeto1
  .  .  gui.py      # gui class of objeto1
  .  .  add.py      # add class of objeto1
  .  .  add.ui      # ui file of objeto1 form
  .  /object2
  .  /object3
  /gui
  .  mainwindow.py  # controlling class of the main window
  .  mainwindow.ui  # ui file of the main window
  /mvc
  .  controller.py  # database configurations
  .  models.py      # instances of Manager classes
  .  views.py       # instances of GUI classes
  run.py            # running the application
```
You can download this structure from [here]().

## Plasta generator

Plasta comes with a generator for the following operations:

### Generate package for a model

`> plasta g crud [OPTIONS] NAMEMODEL [ATTRIBUTES]`

**Options:**
* `-ui`: along with the model generates the ui file
* `-s`: generates storm file only 
* `-m`: generates manager file only 
* `-g`: generates gui file only 
* `-a`: generates add file only

**Attributes**:

To indicate type attributes, follow the directions in the following table:

| Attribute type | Related widget |
|-|-|
| unicode (default) | QLineEdit |
| int | QSpinBox | 
| float | QDoubleSpinBox | 
| date | QDateEdit | 
| datetime| QDateTimeEdit | 
| bool | QCheckBox | 

Format to use: `attribute:type` e.g: `name birthday:date isActived:bool`

**Examples of use:**

`> plasta g crud -ui person name lastname address birthday:date sex`

*Result:* will generate the 4 classess and the ui file

`> plasta g crud -s -m person name lastname address sex`

*Result:* will generate the package only with the Storm and Manager classes 

### Generate ui file for a form

`> plasta g ui [ATTRIBUTES]`

**Example of use:**

`> plasta g ui name lastname email`


[Go > Index](https://github.com/informaticameg/Plasta/blob/master/doc/en/index.md) | [Go > Install](https://github.com/informaticameg/Plasta/blob/master/doc/en/install.md) | [Go > Getting started](https://github.com/informaticameg/Plasta/blob/master/doc/en/getting_started.md) | [Go > Use cases](https://github.com/informaticameg/plasta/blob/master/doc/en/uses_cases.md) | [Go > Example Apps](https://github.com/informaticameg/plasta/blob/master/doc/en/example_apps.md)