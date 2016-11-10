#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.logic.manager import BaseManager
from country import Country
import csv

class CountryManager( BaseManager ):

    def __init__(self, store, reset = False ):
        BaseManager.__init__(self, store, reset)
        # set the class model wich controlling
        self.CLASS = Country

        self._start_operations()

    def insertCountries(self):
        '''
        Insert into database the list of countries readed from csv file.
        '''
        csv_file = 'countries.csv'
        with open(csv_file, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                country = {
                'code':unicode(row[0], 'utf-8'),
                'name':unicode(row[1].decode('string-escape'))
                }
                self.add(country, commit=False)
        self.store.flush()
        self.store.commit()