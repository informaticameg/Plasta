# Introducción

A la hora de desarrollar una aplicación típica, siempre nos encontramos con operaciones comunes que se repiten una y otra vez. Tales como agregar, editar, eliminar, listar y buscar. Plasta nace para intentar reducir el tiempo de desarrollo y mantenimiento de este tipo de aplicaciones, ofreciendo una API común que implementa estas operaciones.


## Licencia

Plasta está publicado bajo la licencia [MIT](http://www.opensource.org/licenses/MIT).

## Componentes

Plasta se compone de 4 componentes principales que son las 4 clases base de un paquete Plasta.

De estas 4 clases, 3 son puramente heredables: BaseManager, BaseGUI y BaseAdd. En cualquier momento se pueden reimplementar cualquiera de sus operaciones para lograr el fin deseado.

### La clase Storm

Aquí es donde se definen los atributos para un modelo, según lo estipulado en la documentación de Storm [aquí](https://storm.canonical.com/Tutorial#The_Storm_base_class). Es la definición de un objeto/tabla para la persistencia en la base de datos.

### La clase BaseManager

Ésta será la encargada de controlar los objetos del modelo con el que se esté trabajando, y donde están definidas las operaciones base del lado de la lógica.

### La clase BaseGUI

Aquí están definidas todas las operaciones que controlarán la interfaz gráfica principal de un modelo.

### La clase BaseAdd

Esta clase posee las operaciones para manejar las operaciones del formulario  agregar/editar.

## Terminologías

| Término | Definición |
|---------|------------|
| Manager | clase controladora de un modelo |
| Paquete | paquete Plasta compuesta de las 4 clases |
| UI | archivo xml de una ventana Qt |
| Widget | componente visual Qt |

## Convenciones

Para el correcto funcionamiento de Plasta, se deberán respetar estas convenciones:

#### Nombres de las clases

| Clase base | Ejemplo |
|------------|---------|
| BaseManager     | ClienteManager |
| BaseGUI         | ClienteGUI |
| BaseAdd         | AddCliente |

#### Nombres widgets en la pantalla principal de un modelo

| Nombre widget | Tipo widget |
|---------------|-------------|
| lbTitle      | QLabel |
| btNew        | QPushButton |
| btEdit       | QPushButton |
| btDelete     | QPushButton |
| leSearch     | QLineEdit |
| cbFilters    | QComboBox |
| lbItemsCount | QLabel |
| twItems      | QTableWidget |

#### Nombres widgets en el formulario agregar/editar

| Nombre widget | Tipo widget |
|---------------|-------------|
| btSave        | QPushButton |
| btExit      | QPushButton |


#### Prefijos de los widgets

Plasta ha adoptado estos prefijos para nombrar a los widgets de la GUI:

| Widget | Prefijo |
|--------|---------|
| QLabel         | lb |
| QLineEdit      | le |
| QComboBox      | cb |
| QSpinBox       | sb |
| QDoubleSpinBox | dsb |
| QTextEdit      | te |
| QDateEdit      | dt |
| QDateTimeEdit  | dte |
| QTimeEdit      | tme |
| QCheckBox      | chk |



[Ir a > Inicio](https://github.com/informaticameg/Plasta/blob/master/doc/es/index.md) | [Ir a > Instalación](https://github.com/informaticameg/Plasta/blob/master/doc/es/install.md) | [Ir a > Como empezar](https://github.com/informaticameg/Plasta/blob/master/doc/es/getting_started.md) | [Ir a > Casos de uso](https://github.com/informaticameg/plasta/blob/master/doc/es/uses_cases.md) | [Ir a > Aplicaciones de ejemplo](https://github.com/informaticameg/plasta/blob/master/doc/es/example_apps.md)