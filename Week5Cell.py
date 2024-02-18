# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 15:32:09 2024
Cell class creates a cell object, cell type can be anaabolic or catabolic.
Cell location is represented by x,y coordinates on a grid (column and row location).

@author: bentn
"""

import numpy as np
import random as r
class Cell:
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

    def move_random(self, tissue_size):
        # assign random number value (-1 = left,0 = no change, 1 = right) to represent direction change of cell's new column location
        change_row = r.randint(-1, 1)
        # assign random number value (-1 = left ,0 = no change,1 = right) to represent direction change of cell's new row location
        change_column = r.randint(-1, 1)
        # Get current row and column location of cell
        row_position = self.Get_Row()
        column_position = self.Get_Column()
        # change row location of cell. If cell moves 'off' tissue, new location wraps around
        new_row = row_position + change_row
        if new_row == tissue_size:
            new_row = 0
        elif new_row == -1:
            new_row = tissue_size - 1
        self.Set_Row(new_row)
        new_column = column_position + change_column
        if new_column == tissue_size:
            new_column = 0
        elif new_column == -1:
            new_column = tissue_size - 1
        self.Set_Column(new_column)
        return new_row, new_column


    def move_durotaxis(self, tissue_size, tissue):
        # Create sequence of possible movements where -1 = left or down, 0 = no movement, and 1 = right or up
        sequence = [(-1, -1), (-1, 1), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        # Get current position of the cell
        current_position = (self.Get_Row(), self.Get_Column())

        # Create array, weights, where each value corresponds to the
        weights = []
        # For each possible movement, get the location (column, row) on the tissue and append the
        for i in range(8):
            row = current_position[0] + sequence[i][0]
            if row == tissue_size:
                row = 0
            elif row == -1:
                row = tissue_size - 1

            column = current_position[1] + sequence[i][1]
            if column == tissue_size:
                column = 0
            elif column == -1:
                column = tissue_size - 1


            if self.Get_Cell_Type() == "anabolic":
                # Append value of tissue at [row,column]
                weights.append(1 - tissue[row, column])
            else:
                # Append value of tissue at [row, column]
                weights.append(tissue[row, column])
        # Normalize weights value
        normalized_weights = weights / sum(weights)
        # Use random.choices to choose a movement choice based on weighted values of each choice
        # Movement choice will be a tuple where each value can be -1,0 or 1
        movement_choice = r.choices(sequence, normalized_weights, k=1)
        # Reassign row and column based off movement choice
        new_row = current_position[0] + int(movement_choice[0][0])
        new_column = current_position[1] + int(movement_choice[0][1])

        # exception handling for cell moving 'off' tissue.
        if new_row == tissue_size:
            new_row = 0
        elif new_row == -1:
            new_row = tissue_size - 1
        self.Set_Row(new_row)

        if new_column == tissue_size:
            new_column = 0
        elif new_column == -1:
            new_column = tissue_size - 1
        self.Set_Column(new_column)

        # Return the new row and column location of cell
        return new_row, new_column