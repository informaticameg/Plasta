#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Informática MEG <contacto@informaticameg.com>
#
# Written by
#       Copyright 2012 Fernandez, Emiliano <emilianohfernandez@gmail.com>
#       Copyright 2012 Ferreyra, Jonathan <jalejandroferreyra@gmail.com>
#
# MIT Licence
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
