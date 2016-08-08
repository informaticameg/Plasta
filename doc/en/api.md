# API

The following functions are described base containing each Plasta base class.
You know them will allow you to extend its functionality as needed.

## BaseManager API

```python
# Import this class
from plasta.logic.manager import BaseManager
```
### Base Methods

#### add(values, commit=True)

Create and add an object to the database

| Param | Type | Description |
|-------|------|-------------|
| values | dict or list | Receiving init parameters of self.CLASS. If values is a `list`, the order of values must match the class init.|
| commit | bool| If True, stores changes instantly. |

Example:
```python
# Client(names, address)
values = {'names':u'John Smith', 'address':u'Some address'}
obj = self.add(values) # adding with dict values

values = [u'John Smith', u'Some address']
obj = self.add(values) # adding with list values

# commiting at finish
for name in ['name1', 'name2', 'name3']:
    self.add({'names':name}, commit=False)
self.store.commit()
```

#### delete(obj)

Delete and object of db

#### count()

Gets the number of objects of this manager

#### getall()

Gets all objects of this manager

#### get(value)

Obtain the objects where "value" matches with `self.searchattr`

#### getById(id)

Returns the object according to the `id` indicated

#### searchBy(column, value)

Perform a search for the name value according column

| Param | Type | Description |
|-------|------|-------------|
| column | storm column | Attribute of class|
| value | str/int/date/reference | Value to search

Example:

```python
print self.searchBy(client.names, u'Smith')
>> [<object>, <object>, ...]
```

#### checkIfExists(obj)

Check that the indicated object exist in the database

Returns two values, bool indicates if exists and the object.

```python
print self.checkIfExists(some_obj)
>> True, <obj_from_db> # if exists
>> False, None # if not exists

```

### Exclusive methods


#### _start_operations()

Required operations to get up the manager

#### _reset()

Drop and recreate the model table

### Inspection Methods

Methods used for object introspection

#### getClassName()

Returns the name of the class that handles

#### getDataObject(obj, columns, rformat='dict')

Returns the data of an object according to the indicated columns

| Param | Type | Description |
|-------|------|-------------|
| obj | object | Object instance|
| columns | list | List of Storm columns. |
| rformat | str | Return format. Possible values `dict`, `list`. By default return in `dict` format. |

Example:

```python
print self.getDataObject(obj_client, [Client.names, Client.address])
>> {'names':u'John Smith', 'address':u'Some address'}

print self.getDataObject(obj_client, [Client.names, Client.address], rformat='list')
>> [{'names':u'John Smith'}, {'address':u'Some address'}]
```

#### getClassAttributes()

Get the attributes of the class that handles

#### getClassAttributesValues(obj, rformat='list')

Returns all the attributes of the object with its respective value

Example:

```python
print self.getClassAttributesValues(obj_client)
>> [u'John Smith', u'Some address']

print self.getClassAttributesValues(obj_client, [Client.names, Client.address], rformat='dict')
>> {'names':u'John Smith', 'address':u'Some address'}
```

#### getClassAttributesInfo()

Returns a dictionary with the data types of the class

Example:
```python
print self.getClassAttributesInfo()
>> {<storm.properties.Unicode object at 0x9e87b0c>: {'name':'names','default': None, 'null': True, 'type': 'str', 'primary': False,'reference':False}}
```

#### getPropertyName(property)

Return the name of Property object

```python
print self.getPropertyName(Client.names)
>> 'names'
```
#### getReferenceName(reference)

Return the name of Reference object

#### getAttributeName(property_or_reference)

Return the name of Property/Reference object

#### propertyToColumn(property)

From a property returns the corresponding column

#### getSqlTable(engine)

Get the SQL to create the table corresponding to the current model

Engines: `sqlite`, `mysql`, `postgres`.

## BaseGUI API

### Logic functions

### GUI functions

## BaseAdd API