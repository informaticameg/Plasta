# Cómo empezar

## Eligiendo la estructura de la aplicación

Plasta no está sujeto a una estructura definida, mientras se respete la estructura del objeto Plasta, lo demás queda a tu criterio. 
De todas maneras te mostramos dos posibles estructuras que puedes usar:

### Estructura simple

```
/myapp
  /person
  mainwindow.py  # clase controladora de la ventana principal
  mainwindow.ui  # archivo ui de la ventana principal
  run.py         # archivo que ejecuta la aplicación
```

Puedes descargar esta estructura desde [aquí]().

### Estructura tipo MVC

```
/myapp
  /model
  .  /person
  .  .  __init__.py # clase storm
  .  .  manager.py  # clase manager de objeto1
  .  .  gui.py      # clase gui de objeto1
  .  .  add.py      # clase add de objeto1
  .  .  add.ui      # archivo ui del formulario objeto1
  /gui
  .  mainwindow.py  # clase controladora de la ventana principal
  .  mainwindow.ui  # archivo ui de la ventana principal
  /mvc
  .  controller.py  # configuración de la base de datos
  .  models.py      # instancias de las clases Manager
  .  views.py       # instancias de las clases GUI
  run.py            # archivo que ejecuta la aplicación
```
Puedes descargar esta estructura desde [aquí]().

## Generador Plasta

Plasta viene con un generador para las siguientes operaciones:

### Generar paquete para un modelo

`> plasta g crud [OPTIONS] NAMEMODEL [ATTRIBUTES]`

**Opciones:**
* `-ui`: genera junto con el modelo el archivo ui
* `-s`: genera unicamente el archivo storm
* `-m`: genera unicamente el archivo manager
* `-g`: genera unicamente el archivo gui
* `-a`: genera unicamente el archivo add

**Atributos**:

Para indicar el tipo de los atributos, sigue las indicaciones de la siguiente tabla:

| Tipo atributo | Widget relacionado |
|-|-|
| unicode (por defecto) | QLineEdit |
| int | QSpinBox | 
| float | QDoubleSpinBox | 
| date | QDateEdit | 
| datetime| QDateTimeEdit | 
| bool | QCheckBox | 

Formato a usar: `atributo:tipo` e.g: `nombre cumpleanios:date estaActivado:bool`

**Ejemplos de uso:**

`> plasta g crud -ui persona nombre apellido direccion cumpleanios:date sexo`

*Resultado:* generará el paquete con las 4 clases y el archivo ui

`> plasta g crud -s -m persona nombre apellido direccion sexo`

*Resultado:* generará el paquete solamente con las clases Storm y Manager.

### Generar archivo ui para un formulario

`> plasta g ui [ATTRIBUTES]`

**Ejemplo de uso:**

`> plasta g ui nombre apellido email`

## [Ir a > Creando el primer paquete Plasta](https://github.com/informaticameg/plasta)