#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Este archivo genera el archivo 'uis.py' con el
contenido de cada archivo .ui del proyecto.
'''

from os.path import join, abspath, dirname
ignore_folders = ['docs', '.git', 'presenter']


def findRecursively(dir, pattern):
    import os
    import fnmatch
    matches = []
    for root, dirnames, filenames in os.walk(dir):
        ignore_iteration = False
        for ignore in ignore_folders:
            if root.find(ignore) != -1:
                ignore_iteration = True
                break
        # print ignore, root
        if ignore_iteration:
            continue
        # print root , dirnames, filenames
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches


def main():
    thisFolder = join(abspath(dirname(__file__)))

    uis = findRecursively(thisFolder, '*.ui')

    result = {}
    for ui_file in uis:
        content_file = open(ui_file, 'r').read().replace('\n', '')
        name_file = ui_file.replace(thisFolder, '')
        result[name_file] = content_file

    content_file = str(result).replace("', '", "',\n'")
    content_file = u'\n'.join(['#!/usr/bin/env python',
                               '# -*- coding: utf-8 -*-\n',
                               'ui = %s' % content_file])

    py_file = open('uis.py', 'w')
    py_file.write(content_file)
    py_file.close()
    print 'uis.py has been generated...'

main()
