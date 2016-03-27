# Introduction

When developing a typical application, we always find common operations that are repeated over and over again. Such as add, edit, delete, list and search. Plasta born to try to reduce development time and maintenance of these applications, providing a common API that implements these operations.


## Licence

Plasta is released under the [MIT License](http://www.opensource.org/licenses/MIT).

## Components

Plasta consists of 4 main components are the 4 base classes of a Plasta package.

Of these 4 classes, 3 are purely heritable: BaseManager, GUIManager y BaseAddWindow. At any time you can implement any of its operations to achieve the desired end.

### The Storm class

This is where the attributes for a model are defined, as stated in the documentation Storm [here](https://storm.canonical.com/Tutorial#The_Storm_base_class). It is the definition of an object / table for persistence in the database.

### The BaseManager class

This will be in charge of controlling model objects with which you are working, and where the operations side base logic are defined.

### The BaseGUI class

Here they are defined all operations that control the main GUI of a model. 

### The BaseAdd class

This class has operations to handle the operations of the form add / edit.

## Terminologies

| Term | Definition |
|-|-|
| Manager | controlling class of a model | 
| Package | Plasta package composed of four classes |
| UI | xml file from a Qt window |
| Widget | Qt visual component |

## Conventions

For the correctly work of Plasta, must respect these conventions:

#### Names of the classess

| Base class | Example |
|-|-|
| BaseManager     | ClientManager |
| BaseGUI         | ClientGUI |
| BaseAddWindow   | AddClient |

#### Widgets names in the main screen of a model

| Widget name | Widget type |
|-|-|
| lbTitle      | QLabel |
| btNew        | QPushButton |
| btEdit       | QPushButton |
| btDel        | QPushButton |
| leSearch     | QLineEdit |
| cbFilters    | QComboBox |
| lbItemsCount | QLabel |
| twItems      | QTableWidget |

#### Widget names in form add/edit

| Widget name | Widget type |
|-|-|
| btSave        | QPushButton |
| btCancel      | QPushButton |


#### Widget prefixes

Plasta has adopted this prefixes to name widgets of GUI:

| Widget | Prefix |
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