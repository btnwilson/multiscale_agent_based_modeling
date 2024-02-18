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
random_tissue.Simulate_Tissue('random', 1000, 0, 1, 0.05)

# Create tissue object
durotaxsis_tissue = T.Tissue(100,20,20)
# Simulate durotaxis movement on tissue
durotaxsis_tissue.Simulate_Tissue('durotaxis', 1000, 0, 1, 0.05, figure=2)

# Find a way to see if random or durotaxis movement creates more consistent value

def get_moving_average(tissue):
    tissue = tissue.get_tissue()
    positions = [(-1, -1), (-1, 1), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    moving_average = []
    for row in tissue:
        for column in row:
            for position in positions:
                total = random_tissue.get_tissue_thickness(row, column)
                new_row = positions[position][0]+row
                new_column = positions[position][1]+column

                # Check to see if new value wraps around grid
                tissue_size = random_tissue.get_tissue_size()
                if new_row == tissue_size:
                    new_row = 0
                elif new_row == -1:
                    new_row = random_tissue.get_tissue_size() - 1
                if new_column == tissue_size:
                    new_column = 0
                elif new_column == -1:
                    new_column = tissue_size - 1
                total += random_tissue.get_tissue_thickness(new_row, new_column)
            moving_average.append(total/9)

    moving_average_positions = np.arange(len(moving_average))
    plt.figure(3)
    plt.title('Moving Average')
    plt.plot(moving_average, moving_average_positions)


get_moving_average(random_tissue)
# Do this using a moving average
# Take the average of 5x5 square around central square
# Graph moving average
# find standard deviation of points