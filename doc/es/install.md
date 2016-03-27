# Instalación

### Desde pip
```sh
$ pip install plasta
```

### Desde Github

```sh
$ wget https://github.com/informaticameg/Plasta/archive/master.zip
$ tar xvf master.zip
$ cd plasta/
$ python setup.py install
```

## Usando localmente

Puedes usar Plasta localmente copiando la carpeta `plasta` en el nivel principal de la carpeta de tu aplicación.

Si también deseas usar `storm` localmente, [descarga](https://launchpad.net/storm/+download) y copia la carpeta en la carpeta de trabajo de tu aplicación.

Un ejemplo:
```
/myapp
|-- /plasta
|-- /storm
|-- ... # demás cosas
|-- run.py
```

## Usando globalmente

Una vez descargado y descomprimido el .zip ejecuta el siguiente comando para instalar Plasta globalmente, dentro de la carpeta descomprimida:

`$ python setup.py install`