#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = 'plasta',
    version = '0.1.5',
    description = 'Framework for rapid deployment of CRUDs',
    long_description = 'Plasta is a framework for rapid deployment of CRUDs in a simple way, in a few steps and in few lines of code.',
    author = 'Jonathan Ferreyra & Emiliano Fernandez',
    author_email = 'plasta@informaticameg.com',
    license = 'MIT',
    url = 'http://github.com/informaticameg/plasta',

    classifiers = [
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = [
        'plasta',
        'plasta.gui',
        'plasta.gui.uis',
        'plasta.gui.uis.images_rc',
        'plasta.logic',
        'plasta.maker',
        'plasta.maker.templates.object',
        'plasta.tools'
    ],
    # package_dir={'gui':'plasta/gui'},
    # package_data={
    #     '': ['README.md'],
    #     #'object':['*.txt'],
    # },
    data_files = [
        ('uis',['plasta/gui/uis/en_list.ui',
                        'plasta/gui/uis/es_list.ui'])]
    #      ("plasta/gui",[
    #          "plasta/gui/uis/en_list.ui",
    #          "plasta/gui/uis/es_list.ui"
    #          ],
    #      )
    #     #("/plasta")
    #  ]
)
