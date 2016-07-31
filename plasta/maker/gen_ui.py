#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Copyright 2011 Jonathan Ferreyra <jalejandroferreyra@gmail.com>
#
#   MIT Licence
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#   THE SOFTWARE.

import os.path
import shutil
from plasta.utils import pathtools
import xml_widgets

prefijos_widgets = {
    'QCheckBox':'chk',
    'QRadioButton':'rb',
    'QComboBox':'cb',
    'QLineEdit':'le',
    'QPushButton':'bt',
    'QDateEdit':'de',
    'QDateTimeEdit':'dte',
    'QSpinBox':'sb',
    'QDoubleSpinBox':'dsb'
}

#~ Orden de los valores que se reemplazaran en la plantilla: <todo>
#~ 1- Nombre clase o tipo de Ventana [MainWindow, Dialog]
#~ 2- Ancho y Alto
#~ 3- Widgets

def __palabra_mas_larga(palabra1, palabra2):
    return palabra1 if len(palabra1) > len(palabra2) else palabra2

def __guardarUI(ruta, contenido):
    archivo_ui = open(ruta,'w')
    archivo_ui.write(contenido)
    archivo_ui.close()
    return True

def __obtenerEventoCerrarVentana(nombre_boton, tipo_ventana) :
    resultado = xml_widgets.evento_cerrar_ventana.replace('#nombre_boton#',nombre_boton)
    resultado = resultado.replace('#tipo_ventana#',tipo_ventana)
    return resultado

def __obtenerTextoBotones(botones, lang) :
    """
    """
    values = {'bt_salir_aceptar':False,'bt_salir_guardar':False,
        'bt_cancelar_aceptar':False,'bt_limpiar':False}
    for k, v in botones.iteritems():
        values[k] = v
    boton1, boton2 = '',''
    if values['bt_salir_aceptar']:
        if lang == 'es':
            boton1, boton2 = 'Salir','Aceptar'
        elif lang == 'en':
            boton1, boton2 = 'Exit','Acept'
    elif values['bt_salir_guardar']:
        if lang == 'es':
            boton1, boton2 = 'Salir','Guardar'
        elif lang == 'en':
            boton1, boton2 = 'Exit','Save'
    elif values['bt_cancelar_aceptar']:
        if lang == 'es':
            boton1, boton2 = 'Cancelar','Aceptar'
        elif lang == 'en':
            boton1, boton2 = 'Cancel','Acept'
    elif values['bt_limpiar']:
        if lang == 'es':
            boton1, boton2 = 'Limpiar',''
        elif lang == 'en':
            boton1, boton2 = 'Clean',''

    return boton1, boton2

def __generarBotones(codigo, lang, botones = {}):
    """
    Devuelve el codigo xml correspondiente al tipo de botones indicado.
    """
    defButtons = {'bt_limpiar': False, 'bt_cancelar_aceptar': False,
        'bt_salir_guardar': True, 'bt_salir_aceptar': False}
    botonA, botonB = '',''
    if botones :
        for k in botones:
            defButtons[k] = botones[k]
        # obtiene que botones se van a generar
        botonA, botonB = __obtenerTextoBotones(botones, lang)
        resultado = xml_widgets.par_botones.replace('###',botonA)
        resultado = resultado.replace('%%%',botonB)
        return resultado
    else:
        return codigo
    pass

def __generarWidgets(campos, lang, botones = {}):
    """
    Genera el codigo xml correspondiente a los campos indicados.
    """
    codigo_widgets = ''
    tamano_layout = 20 # se incrementa de a 40 pixeles

    # con esto se obtiene la longitud del label para que quede todo ordenadito
    longitud_labels = __obtenerLongitudLabels(campos)
    cant_campos = len(campos)
    for current_campo in campos:
        campo = current_campo.keys()[0]
        widget = current_campo.values()[0]
        # primero, obtiene el xml correspondiente al tipo de widget actual,
        # y lo mezcla con el del label
        # luego, reemplaza los ### por el nombre actual del campo
        xml_widget = xml_widgets.source_widgets[widget]
        widget_actual = (xml_widgets.par_label_layout % (longitud_labels, xml_widget)).replace('#nombre_widget#',campo.capitalize())
        prefijo_widget = prefijos_widgets[ widget ]
        widget_actual = widget_actual.replace(u'#prefijo#', prefijo_widget)
        widget_actual = widget_actual.replace(u'#nombre_campo#', campo.capitalize())
        tamano_layout += 40 # incrementa para  ubicar el proximo widget
        codigo_widgets +=  widget_actual + '\n'

    # genera el codigo correspondiente a los botones en caso de que
    # se reciba algun valor como parametro
    if botones :
        codigo_widgets += __generarBotones(codigo_widgets, lang, botones)

    return codigo_widgets

def __generarPlantilla(destino, tipo, metodos = None):
    """
    {str} tipo = Dialog | MainWindow
    """
    nombre_archivo = os.path.basename(destino).split('.')[0] + '.py'
    ruta_destino = pathtools.convertPath(os.path.dirname(destino)+'/'+nombre_archivo)
    shutil.copyfile(
            pathtools.convertPath( pathtools.getPathProgramFolder()+'plantillas/plantilla.py' ),
            ruta_destino)

    archivo = open(ruta_destino,'r')
    contenido = archivo.read()
    archivo.close()

    # reemplaza en el texto los campos de la plantilla
    contenido = contenido.replace(u'%%%',tipo)
    contenido = contenido.replace(u'&&&',os.path.basename(destino).split('.')[0])
    archivo = open(ruta_destino,'w')
    archivo.write(contenido)
    archivo.close()
    print '>>> Plantilla .py generada'
    return True

def __obtenerLongitudLabels(campos) :
    """
    Devuelve la longitud que deberan tener los labels para que "quede
    ordenado" en la interfaz.
    """
    palabras = map(lambda elemento : elemento.keys()[0] , campos)
    return len(reduce(__palabra_mas_larga,  palabras )) * 8

def __obtenerAltoVentana(campos):
    return int((len(campos) * 40) * 1.5)

def generateUI( destino,
                campos,
                botones = {},
                opciones = {}
            ):
    """
    Genera un archivo .ui con los datos que recibe del diccionario campos.
    Params:
    {str}  destino = ubicacion de destino
    {dict} campos = [{u'field1': u'QLineEdit'}, {u'field2': u'QLineEdit'}, ...]
    {dict} botones = {'bt_limpiar': False, 'bt_cancelar_aceptar': False, 'bt_salir_guardar': True, 'bt_salir_aceptar': False}
    {dict} opciones = {'tipo': 'Dialog', 'generar_plantilla': False, 'lang':'es|en'}
    """
    if 'lang' not in opciones.keys():
        opciones['lang'] = 'en'
    ### Atributos
    ancho_ventana = 400
    alto_ventana = __obtenerAltoVentana(campos)
    widgets = __generarWidgets(campos, opciones['lang'], botones)
    resultado = ''
    tipo_ventana = opciones['tipo']
    opciones_generacion = opciones.keys()

    # reemplaza el ancho
    resultado = xml_widgets.todo.replace('%ancho%',str(ancho_ventana))
    # reemplaza el alto
    resultado = resultado.replace('%alto%',str(alto_ventana))
    # reemplaza los widgets
    resultado = resultado.replace('%widgets%',widgets)

    # reemplaza la señal del boton que cierra la ventana
    btn1, btn2 = __obtenerTextoBotones(botones, opciones['lang'])
    codigo_evento = __obtenerEventoCerrarVentana(btn1,tipo_ventana)
    resultado = resultado.replace('<connections/>',codigo_evento)

    # establece el tipo de ventana
    if 'tipo' in opciones_generacion :
        resultado = resultado.replace('###',tipo_ventana)
        # si la ventana es del tipo QMainWindow agrega la siguiente linea
        if tipo_ventana == 'MainWindow':
            layout = '<layout class="QVBoxLayout" name="verticalLayout_2">'
            resultado = resultado.replace(
                layout,
                '<widget class="QWidget" name="centralwidget">\n   ' + layout
            )
            resultado = resultado.replace(
                ' </widget>\n <resources/>',
                '  </widget> </widget>\n <resources/>'
            )
    # guarda el resultado del parseo en el archivo .ui
    __guardarUI(destino, resultado)

    # genera la plantilla para levantar el ui
    if opciones['generar_plantilla'] == True :
        __generarPlantilla(destino,opciones['tipo'])

    print 'created ui file'
    return True
