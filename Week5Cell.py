# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 15:32:09 2024

@author: bentn
"""


class Cell :
    def __init__(self, cell_type, row, column):
        self.position_row = row
        self.position_column = column
        self.type = cell_type
    
    def Set_Row(self, position):
        self.position_row = position
        
    def Set_Column(self, position):
        self.position_column = position
        
    def Get_Row(self):
        return self.position_row
    
    def Get_Column(self):
        return self.position_column
    
    def Get_Cell_Type(self):
        return self.type