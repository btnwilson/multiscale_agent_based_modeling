# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 15:41:47 2024

@author: bentn
"""
import Week5Tissue as T
from matplotlib import pyplot as plt
import numpy as np
# Create tissue object
random_tissue = T.Tissue(100,20,20)
# simulate random movement on tissue
random_tissue.Simulate_Tissue('random', 1000, 0, 1, 0.05, pause = False)

# Create tissue object
durotaxis_tissue = T.Tissue(100,20,20)
# Simulate durotaxis movement on tissue
durotaxis_tissue.Simulate_Tissue('durotaxis', 1000, 0, 1, 0.05, figure=2, pause = False)

# Find a way to see if random or durotaxis movement creates more consistent value b

def get_moving_average(tissue, figure1, figure2, title):
    tissue = tissue.get_tissue()
    positions = [(-1, -1), (-1, 1), (-1, 1), (0, -1), (0,0), (0, 1), (1, -1), (1, 0), (1, 1)]
    moving_average = []
    row_index = -1
    column_index = -1
    total = 0
    for row in tissue:
        row_index += 1
        column_index = -1
        for column in row:
            total = 0
            column_index += 1 
            for position in positions:
                new_row_index = row_index + position[0]
                new_column_index = column_index + position[1]
                #new_row = positions[position][0]+row
                #new_column = positions[position][1]+column

                # Check to see if new value wraps around grid
                tissue_size = random_tissue.get_tissue_size()
                if new_row_index == tissue_size:
                    new_row_index = 0
                elif new_row_index == -1:
                    new_row_index = random_tissue.get_tissue_size() - 1
                if new_column_index == tissue_size:
                    new_column_index = 0
                elif new_column_index == -1:
                    new_column_index = tissue_size - 1
                total += random_tissue.get_tissue_thickness(new_row_index, new_column_index)
            moving_average.append(total/9)
            
    # Plot moving average as a line graph with squares ordered 0-1000
    moving_average_positions = np.arange(len(moving_average))
    plt.figure(figure1, clear = True)
    plt.title(f'Moving Average of {title}')
    plt.xlabel('Square Values from Right to Left')
    plt.ylabel('Average value ')
    plt.plot(moving_average_positions, moving_average)
    
    # Reshape moving_average list into array of 100 x 100 and plot averages on a heat map
    moving_avg = np.reshape(moving_average, (100,100))
    plt.figure(figure2, clear = True)
    plt.title(f' Moving Average Heat map of {title}')
    plt.imshow(moving_avg, interpolation='nearest', vmin=0, vmax=1)
    
    # Calculate standard deviation 
    std = np.std(moving_average)
    return std

std_rand = get_moving_average(random_tissue, 3, 4, 'Random Movement')
std_duro = get_moving_average(durotaxis_tissue, 5, 6, 'Durotaxis')
