#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2011 Ferreyra, Jonathan <jalejandroferreyra@gmail.com>
#       Copyright 2011 Fernandez, Emiliano <emilianohfernandez@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import os
from sys import argv

def getPathProgramFolder():
    ''' Obtiene la ruta de la carpeta del programa. '''
    program_folder = convertPath(os.path.abspath(os.path.dirname(argv[0])) + "/")
    return program_folder

def getPathDataFolder():
    ''' Obtiene la ruta del directorio data. '''
    program_folder = convertPath(os.path.abspath(os.path.dirname(argv[0])) + "/")
    data_folder = convertPath(os.path.dirname(program_folder[:-4])+'/data/')
    return data_folder

def getPathRootFolder():
    ''' Obtiene la ruta del directorio de la aplicacion. '''
    program_folder = convertPath(os.path.abspath(os.path.dirname(argv[0])) + "/")
    root_folder = convertPath(os.path.dirname(program_folder[:-4])+'/')
    return root_folder

def convertPath(path):
    """Convierte el path a el específico de la plataforma (separador)"""
    if os.name == 'posix':
        return "/"+apply( os.path.join, tuple(path.split('/')))
    elif os.name == 'nt':
        return apply( os.path.join, tuple(path.split('/')))

if __name__ == '__main__':


    data = getPathDataFolder()
    print data
