#!/usr/bin/env python
# -*- coding: utf-8 -*-


def openExternalFile(filename):
    import webbrowser
    webbrowser.open(filename)


def add_months(sourcedate, months):
    import datetime
    import calendar
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12)
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def showMessage(self, title, message, typemsg='info'):
    '''
    type = info, error, warn
    '''
    from PyQt4 import QtGui
    types = {
        'info': QtGui.QMessageBox.information,
        'error': QtGui.QMessageBox.critical,
        'warn': QtGui.QMessageBox.warning,
    }
    types[typemsg](self, title, message)


def getModel(class_name, model=None, package='model'):
    '''
    Retorna la clase del modelo indicado

    Uso:
        getModel('Person')
        getModel('OtherName', model='other_name')
    '''

    if model is None:
        model = class_name.lower()

    if class_name in ['User', 'Role']:
        package = 'auth'

    return __import__(package).__dict__[model].__dict__[class_name]
