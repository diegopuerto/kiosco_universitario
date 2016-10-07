'''
Created on 12/11/2015

@author: EJArizaR
'''
import csv
import StringIO

class Formatter(object):



    def email_format(self, input_text):
        emails = self._extract_column(input_text, 0)
        return ",".join(emails)

    def cellphone_format(self, input_text):
        cellphones = self._extract_column(input_text, 1)
        return ",".join(cellphones)
    
    def _extract_column(self, input_text, col_number):
        column = []
        reader = self._create_reader(input_text)
        for row in reader:
            column.append(row[col_number].strip())
        
        return column   

    def _create_reader(self, input_text):
        f = StringIO.StringIO(input_text)
        reader = csv.reader(f, delimiter=',')
        reader.next()
        return reader    


