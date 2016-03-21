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

from plasta.tools import pathtools

#############################################################################################

_thisFolder = pathtools.getPathProgramFolder() + pathtools.convertPath('plasta/maker/templates/object')[1:]

_meta = {
  'widgets':{
    'lineEdit':'le',
    'comboBox':'cb',
    'spinBox':'sb',
    'doubleSpinBox':'dsb',
    'textEdit':'te',
    'dateEdit':'dt',
    'dateTimeEdit':'dte',
    'timeEdit':'tme',
    'checkBox':'chk',
  }
}

def generatePackage(objInfo):

  _generateFiles(objInfo)
  _generateContentFiles(objInfo)

def _generateContentFiles(objInfo):
  contentFiles = _readContentFiles()
  ############################################################
  ## Generate 'storm' file
  ############################################################
  if objInfo['classesToGenerate']['storm']:
    # generate attrs
    attrs = ''
    if objInfo['addIdeAttr']:
      attrs += 'ide = Int(primary = True)\n'
    for attr in objInfo['attributes']:
      attrs += '    %s = %s()\n' % (attr['name'], attr['type'])

    # generate init method
    initMethod = 'def __init__(self, {params}):\n{attrs}'
    classAttrs = [attr['name'] for attr in objInfo['attributes']]
    initMethod = initMethod.replace('{params}', ', '.join(classAttrs))
    # generate init attrs
    initAttrs = ''
    for attr in classAttrs:
      initAttrs += ' ' * 8 + 'self.' + attr + ' = ' + attr + '\n'
    initMethod = initMethod.replace('{attrs}', initAttrs)
    # generate content the file
    content = contentFiles['storm']
    content = content.replace('%Object_name%', objInfo['className'])
    content = content.replace('%object_name%', objInfo['className'].lower())
    content = content.replace('{attributes}', attrs)
    content = content.replace('{init_method}', initMethod)
    _writeContentFile(objInfo, 'storm', content)

  ############################################################
  ## Generate 'add' file
  ############################################################
  if objInfo['classesToGenerate']['add']:
    # generate attrs
    attrs = ''
    for attr, widget in objInfo['widgetToAttr'].iteritems():
      widgetName = _meta['widgets'][widget] + attr.lower().capitalize()
      attrs += ' ' * 10 + '{self.%s:%s.%s},\n' % (widgetName, objInfo['className'], attr)
    # generate content the file
    content = contentFiles['add']
    content = content.replace('%Object_name%', objInfo['className'])
    content = content.replace('%object_name%', objInfo['className'].lower())
    content = content.replace('{attributes}', attrs)
    _writeContentFile(objInfo, 'add', content)

  ############################################################
  ## Generate 'gui' file
  ############################################################
  if objInfo['classesToGenerate']['gui']:
    # generate attrs
    attrs = ''
    for attr, widget in objInfo['widgetToAttr'].iteritems():
      attrs += ' ' * 10 + "#{u'%s':%s.%s},\n" % (attr.lower().capitalize(), objInfo['className'], attr)
    # generate content the file
    content = contentFiles['gui']
    content = content.replace('%Object_name%', objInfo['className'])
    content = content.replace('%object_name%', objInfo['className'].lower())
    content = content.replace('{attributes}', attrs)
    _writeContentFile(objInfo, 'gui', content)

  ############################################################
  ## Generate 'manager' file
  ############################################################
  if objInfo['classesToGenerate']['manager']:
    # generate content the file
    content = contentFiles['manager']
    content = content.replace('%Object_name%', objInfo['className'])
    content = content.replace('%object_name%', objInfo['className'].lower())
    _writeContentFile(objInfo, 'manager', content)

def _generateFiles(data):
  nameFolder = pathtools.convertPath(
    '/' + data['className'].replace(" ", "").lower())
  outputFolder = data['outputFolder'] + nameFolder
  data['outputNameFolder'] = outputFolder
  import shutil
  shutil.copytree(_thisFolder, outputFolder)
  #print 'generate files...ok'

def _readContentFiles():
  return {
    'storm':open(_thisFolder + '/__init__.py', 'r').read(),
    'add':open(_thisFolder + '/add.py', 'r').read(),
    'gui':open(_thisFolder + '/gui.py', 'r').read(),
    'manager':open(_thisFolder + '/manager.py', 'r').read()
  }

def _writeContentFile(objInfo, fileType, content):
  nameFile = {
    'storm':'__init__.py',
    'add':'add.py',
    'gui':'gui.py',
    'manager':'manager.py',
  }[fileType]
  f = open(objInfo['outputNameFolder'] + '/' + nameFile, 'w')
  f.write(content)
  f.close()
  print 'created %s/%s ' % (objInfo['className'].lower(), fileType)

def main():
    pass

if __name__ == "__main__":
  # attrs = Unicode, Int, Date, Float, Time
  # data = {
  # 'className':'Myclass',
  # 'addIdeAttr':True,
  # 'attributes':[
  #     {'name':'attr1','type':'Unicode'},
  #     {'name':'attr2','type':'Unicode'},
  #     {'name':'attr3','type':'Int'},
  #   ],
  # 'widgetToAttr':{
  #   'attr1':'lineEdit',
  #   'attr2':'comboBox',
  #   'attr3':'spinBox',
  # },
  # 'classesToGenerate':{
  #   'storm':True,'manager':True,'gui':True,'add':True
  # },
  # 'outputFolder':''
  # }
  pass