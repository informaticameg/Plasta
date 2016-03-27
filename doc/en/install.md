# Install

### From pip
```sh
$ pip install plasta
```

### From Github

```sh
$ wget https://github.com/informaticameg/Plasta/archive/master.zip
$ tar xvf master.zip
$ cd plasta/
$ python setup.py install
```

## Using locally

Can use Plasta locally coping the folder `plasta` at the same level of the parent folder of the application

If you also want to use `storm` locally, [download](https://launchpad.net/storm/+download) and copy the folder into the working folder of your application.

An example:
```
/myapp
|-- /plasta
|-- /storm
|-- ... # other things
|-- run.py
```

## Using globally

Once downloaded and unzip the .zip, run the following command to install Plasta globally within the unzipped folder:

`$ python setup.py install`