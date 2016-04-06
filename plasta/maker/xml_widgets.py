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

#~ Orden de los valores que se reemplazaran en la plantilla: <todo>
#~ 1- Nombre clase o tipo de Ventana [MainWindow, Dialog]
#~ 2- Ancho y Alto
#~ 3- Widgets

todo = u'''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>###</class>
 <widget class="Q###" name="###">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>%ancho%</width>
    <height>%alto%</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>###</string>
  </property>

  <layout class="QVBoxLayout" name="verticalLayout_2">
   <item>
    <layout class="QVBoxLayout" name="verticalLayout">
     %widgets%
    </layout>
   </item>
  </layout>

 </widget>
 <resources/>
 <connections/>
</ui>'''

#~ Orden de los valores que se reemplazaran en la plantilla: <par_label_layout>
#~ 1- Nombre del layout
#~ 2- Nombre del label
#~ 3- Ancho del label
#~ 4- Etiqueta del label
#~ 5- Widget

par_label_layout = u'''<item>
     <layout class="QHBoxLayout" name="hl###">
      <item>
       <widget class="QLabel" name="lb#nombre_widget#">
        <property name="minimumSize">
         <size>
          <width>%d</width>
          <height>0</height>
         </size>
        </property>
        <property name="text">
            <string>#nombre_campo#</string>
        </property>
        <property name="alignment">
            <set>Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter</set>
        </property>
       </widget>
      </item>
      %s
     </layout>
    </item>'''

#~ Orden de los valores que se reemplazaran en la plantilla: <par_botones>
#~ 1- Nombre del boton1
#~ 2- Nombre del boton2

par_botones = u'''<item>
     <layout class="QHBoxLayout" name="horizontalLayout">
      <item>
       <widget class="QPushButton" name="bt###">
        <property name="text">
         <string>###</string>
        </property>
       </widget>
      </item>
      <item>
       <spacer name="horizontalSpacer">
        <property name="orientation">
         <enum>Qt::Horizontal</enum>
        </property>
        <property name="sizeHint" stdset="0">
         <size>
          <width>40</width>
          <height>20</height>
         </size>
        </property>
       </spacer>
      </item>
      <item>
       <widget class="QPushButton" name="bt%%%">
        <property name="text">
         <string>%%%</string>
        </property>
       </widget>
      </item>
     </layout>
    </item>'''

#~ Orden de los valores que se reemplazaran en la plantilla: <par_botones>
#~ 1- Nombre del boton al que le asigna el evento
#~ 2- Tipo de ventana

evento_cerrar_ventana = u'''<connections>
  <connection>
   <sender>bt#nombre_boton#</sender>
   <signal>clicked()</signal>
   <receiver>#tipo_ventana#</receiver>
   <slot>close()</slot>
   <hints>
    <hint type="sourcelabel">
     <x>273</x>
     <y>201</y>
    </hint>
    <hint type="destinationlabel">
     <x>123</x>
     <y>186</y>
    </hint>
   </hints>
  </connection>
 </connections>'''

#~ Orden de los valores que se reemplazaran en la plantilla: <lineedit>
#~ 1- Nombre del entry

lineedit = u'''<item>
       <widget class="QLineEdit" name="#prefijo##nombre_widget#">
        <property name="sizePolicy">
         <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
          <horstretch>0</horstretch>
          <verstretch>0</verstretch>
         </sizepolicy>
        </property>
       </widget>
      </item>'''

lineedit_with_btref = u'''<item><layout class="QHBoxLayout" name="hl_#nombre_widget#">
       <property name="spacing">
        <number>0</number>
       </property>
       <item>
        <widget class="QLineEdit" name="#prefijo##nombre_widget#">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="text">
          <string/>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QPushButton" name="bt#nombre_widget#">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Preferred">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="maximumSize">
          <size>
           <width>30</width>
           <height>26</height>
          </size>
         </property>
         <property name="cursor">
          <cursorShape>PointingHandCursor</cursorShape>
         </property>
         <property name="text">
          <string/>
         </property>
         <property name="icon">
          <iconset>
           <normaloff>find.png</normaloff>find.png</iconset>
         </property>
         <property name="iconSize">
          <size>
           <width>20</width>
           <height>20</height>
          </size>
         </property>
        </widget>
       </item>
      </layout>
      </item>'''

#~ Orden de los valores que se reemplazaran en la plantilla: <combobox>
#~ 1- Nombre del combo

combobox = u'''<item>
       <widget class="QComboBox" name="#prefijo##nombre_widget#"><!-- Cambio -->
        <property name="sizePolicy">
         <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
          <horstretch>0</horstretch>
          <verstretch>0</verstretch>
         </sizepolicy>
        </property>
       </widget>
      </item>'''

#~ Orden de los valores que se reemplazaran en la plantilla: <radiobutton>
#~ 1- Nombre del radiobutton
#~ 2- Etiqueta del radiobutton

radiobutton = u'''<item>
       <widget class="QRadioButton" name="#prefijo##nombre_widget#">
        <property name="text">
         <string>#nombre_campo#</string>
        </property>
        <property name="sizePolicy">
         <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
          <horstretch>0</horstretch>
          <verstretch>0</verstretch>
         </sizepolicy>
        </property>
       </widget>
      </item>'''

#~ Orden de los valores que se reemplazaran en la plantilla: <checkbox>
#~ 1- Nombre del checkbox
#~ 2- Etiqueta del checkbox

checkbox = u'''<item>
       <widget class="QCheckBox" name="#prefijo##nombre_widget#">
        <property name="text">
         <string>#nombre_campo#</string>
        </property>
        <property name="sizePolicy">
         <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
          <horstretch>0</horstretch>
          <verstretch>0</verstretch>
         </sizepolicy>
        </property>
       </widget>
      </item>'''

dateedit = u'''<item>
     <widget class="QDateEdit" name="#prefijo##nombre_widget#">
      <property name="sizePolicy">
       <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
        <horstretch>0</horstretch>
        <verstretch>0</verstretch>
       </sizepolicy>
      </property>
      <property name="displayFormat">
       <string>dd/MM/yyyy</string>
      </property>
      <property name="calendarPopup">
       <bool>true</bool>
      </property>
     </widget>
    </item>'''

datetimeedit = u'''<item>
      <widget class="QDateTimeEdit" name="#prefijo##nombre_widget#">
       <property name="sizePolicy">
        <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
         <horstretch>0</horstretch>
         <verstretch>0</verstretch>
        </sizepolicy>
       </property>
      </widget>
     </item>'''

spinbox = '''<item>
     <widget class="QSpinBox" name="#prefijo##nombre_widget#"/>
    </item>'''

doublespinbox = '''<item>
     <widget class="QDoubleSpinBox" name="#prefijo##nombre_widget#"/>
    </item>'''

# diccionario que contiene el fuente de los distintos widgets
source_widgets = {
'QCheckBox':checkbox,
'QRadioButton':radiobutton,
'QComboBox':combobox,
'QLineEdit':lineedit,
'QLineEditWithReference':lineedit_with_btref,
'QDateEdit':dateedit,
'QDateTimeEdit':datetimeedit,
'QSpinBox':spinbox,
'QDoubleSpinBox':doublespinbox
}