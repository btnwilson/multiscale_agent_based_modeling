# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 15:41:47 2024

@author: bentn
"""

import Week5Cell as AC
import numpy as np 
import random as r
import matplotlib.pyplot as plt

def move_random(cell, array_size):
    change_row = r.randint(-1,1)
    change_column = r.randint(-1,1)
    row_position = cell.Get_Row()
    column_position = cell.Get_Column()
    new_row = row_position + change_row
    if new_row == array_size:
        new_row = 0
    elif new_row == -1:
        new_row = array_size - 1
    cell.Set_Row(new_row)
    new_column = column_position + change_column
    if new_column == array_size:
        new_column = 0
    elif new_column == -1:
        new_column = array_size - 1
    cell.Set_Column(new_column)
    return new_row, new_column

def move_durotaxis(cell, array_size):
    pass

array_size = 100
grid = np.full((array_size,array_size), .5)
cell_location = np.full((array_size, array_size), np.nan)
vmin, vmax = 0, 1
fig, ax = plt.subplots()


tissue = ax.imshow(grid, cmap='hot', interpolation='nearest', vmin=vmin, vmax=vmax)
cell = ax.imshow(cell_location, cmap='winter', interpolation='nearest', vmin=vmin, vmax=vmax)
plt.colorbar(tissue)



anabolic_cells = {}
catabolic_cells = {}

num_cells = 20
for i in range(num_cells):
    a_start_row = r.randint(0, array_size-1)
    a_start_column = r.randint(0, array_size-1)
    anabolic_cells[f"A_Cell_{i+1}"] = AC.Cell("anabolic", a_start_row, a_start_column)
    cell_location[a_start_row, a_start_column] = 1
    
    c_start_row = r.randint(0, array_size-1)
    c_start_column = r.randint(0, array_size-1)
    catabolic_cells[f"C_Cell_{i+1}"] = AC.Cell("catabolic", c_start_row, c_start_column)
    cell_location[c_start_row, c_start_column] = 0
iterations = 1000
for t in range(iterations):
    for anabolic in anabolic_cells.keys():
        current_position = (anabolic_cells[anabolic].Get_Row(), anabolic_cells[anabolic].Get_Column())
        cell_location[current_position[0], current_position[1]] = np.nan
        row, column = move_random(anabolic_cells[anabolic], array_size)
        cell_location[row, column] = 1
        if grid[row, column] == 1:
            pass
        else:
            grid[row, column] += .05
    
    for catabolic in catabolic_cells.keys():
        current_position = (catabolic_cells[catabolic].Get_Row(), catabolic_cells[catabolic].Get_Column())
        cell_location[current_position[0], current_position[1]] = np.nan
        row, column = move_random(catabolic_cells[catabolic], array_size)
        cell_location[row, column] = 0
        if grid[row, column] == 0:
            pass
        else:
            grid[row, column] -= .05
    tissue.set_array(grid)
    cell.set_array(cell_location)
    
    plt.pause(0.05)
    
    


