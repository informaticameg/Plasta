#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

def validarMayorQueHoy(fecha):
    ''' Devuelve True si la fecha es mayor que la de hoy.'''
    date_fecha = datetime.strptime(fecha, '%d/%m/%Y')
    hoy = datetime.today()    
    return date_fecha > hoy
    
def getFechaHoy():    
    hoy = datetime.today().strftime('%d/%m/%Y')
    return hoy 

def calcularEdad(fecha_nacimiento):
    """
    Obtiene la edad a partir de una fecha en formato dd/mm/yyyy
    """
    #Utilizamos los operadores de corte para obtener los 4 digitos del aÃ±o
    anio = fecha_nacimiento[6:]
    #los dos del mes de acuerdo a la posiciÃ²n
    mes = fecha_nacimiento[3:5]
    #y los dos del dÃ­a
    dia = fecha_nacimiento[:2]

    #pasamos la fecha por el formato date
    nacim = datetime.date(int(anio),int(mes),int(dia))
    #Obtenemos la fecha actual
    dhoy = datetime.date.today()

    #Calculamos la edad
    edad = dhoy.year - nacim.year

    if nacim.replace(year=dhoy.year):
        edad -= 1
        resultado = str(edad + 1)
    return resultado
