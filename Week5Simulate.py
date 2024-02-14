# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 15:41:47 2024

@author: bentn
"""

import Week5AnabolicCell as AC
import numpy as np 
import random as r
import matplotlib.pyplot as plt

def move(cell, array_size):
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


array_size = 100
grid = np.zeros((array_size,array_size))
vmin, vmax = 0, 5
fig, ax = plt.subplots()


heatmap = ax.imshow(grid, cmap='hot', interpolation='nearest', vmin=vmin, vmax=vmax)
plt.colorbar(heatmap)



anabolic_cells = {}
catabolic_cells = {}

num_cells = 20
for i in range(num_cells):
    anabolic_cells[f"A_Cell_{i+1}"] = AC.Cell("anabolic", r.randint(0, array_size), r.randint(0, array_size))
    catabolic_cells[f"C_Cell_{i+1}"] = AC.Cell("catabolic", r.randint(0, array_size), r.randint(0, array_size))
    
iterations = 1000
for t in range(iterations):
    for anabolic in anabolic_cells.keys():
        row, column = move(anabolic_cells[anabolic], array_size)
        grid[row, column] += .2 
    
    for catabolic in catabolic_cells.keys():
        row, column = move(catabolic_cells[catabolic], array_size)
        if grid[row, column] == 0:
            pass
        else:
            grid[row, column] -= .2
    heatmap.set_array(grid)
    
    plt.pause(0.25)
    
    


