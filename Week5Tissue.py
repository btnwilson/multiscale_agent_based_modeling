# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 22:48:13 2024
"""

import numpy as np
import random as r
import Week5Cell2 as C
from matplotlib import pyplot as plt

class Tissue:
    def __init__(self, tissue_size, num_c_cells, num_a_cells):
        """
        Initialise the tissue. Each tissue has a tissue_size, an array tissue of tissue_size x tissue_size,
        a number of catabolic and anabolic cells, num_c_cells and num_a_cells, respectively. A Tissue object
        has a cell location array initialized to tissue_size x tissue_size. Initialize dictionaries anabolic and catabolic cells to be empty.
        :param tissue_size: An integer value representing the dimensions of tissue
        :param num_c_cells: An integer value representing the number of catabolic cells
        :param num_a_cells: An integer value representing the number of anabolic cells
        """
        self.tissue_size = tissue_size
        self.tissue = np.full((tissue_size, tissue_size), .5)
        self.num_c_cells = num_c_cells
        self.num_a_cells =  num_a_cells
        self.cell_location = np.full((tissue_size, tissue_size), np.nan)
        self.anabolic_cells = {}
        self.catabolic_cells = {}
    def get_tissue(self):
        return self.tissue
    def get_tissue_size(self):
        return self.tissue_size
    def get_cell_location(self):
        return self.cell_location
    def get_tissue_thickness(self, row, column):
        return self.tissue[row][column]
    def initialize_anabolic_cells(self):
        # Add Cells of anabolic type at random (row,column) position in cell_location map to anabolic_cells.
        for i in range(self.num_a_cells):
            a_start_row = r.randint(0, self.tissue_size - 1)
            a_start_column = r.randint(0, self.tissue_size - 1)
            # Add anabolic cell to anabolic_cells dict
            self.anabolic_cells[f"A_Cell_{i + 1}"] = C.Cell("anabolic", a_start_row, a_start_column)
            # Change value of cell_location array to 1 to represent occupation of anabolic cell
            self.cell_location[a_start_row, a_start_column] = 1
        return self.anabolic_cells


    def initialize_catabolic_cells(self):
        # Add Cells of catabolic type at random position to catabolic_cells.
        for i in range(self.num_c_cells):
            c_start_row = r.randint(0, self.tissue_size - 1)
            c_start_column = r.randint(0, self.tissue_size - 1)
            # Add catabolic cell to anabolic_cells dict
            self.catabolic_cells[f"C_Cell_{i + 1}"] = C.Cell("catabolic", c_start_row, c_start_column)
            # Change value of cell_location array to 0 to represent occupation of catabolic cell
            self.cell_location[c_start_row, c_start_column] = 0
        return self.catabolic_cells

    def Simulate_Tissue(self, movement_type, iterations, vmin, vmax, pause=True, figure = 1, alpha=.1, beta=.5):
        # Initialize cells
        self.initialize_catabolic_cells()
        self.initialize_anabolic_cells()
        # Create figure
        plt.figure(figure, clear = True)
        tissue_plot = plt.imshow(self.tissue, cmap='gray', interpolation='nearest', vmin=vmin, vmax=vmax)
        cell_plot = plt.imshow(self.cell_location, cmap='winter', interpolation='nearest', vmin=vmin, vmax=vmax)
        tbar = plt.colorbar(tissue_plot)
        tbar.set_label("Tissue Density", rotation= 270, labelpad=15)
        tbar.ax.text(0.5, 1.05, 'High', ha='center', va='bottom', transform=tbar.ax.transAxes, fontsize=12)
        tbar.ax.text(0.5, -0.05, 'Low', ha='center', va='top', transform=tbar.ax.transAxes, fontsize=12)
        cbar = plt.colorbar(cell_plot)
        cbar.set_label("Cell Type", rotation= 270, labelpad=15)
        cbar.ax.text(0.5, 1.05, 'Anabolic', ha='center', va='bottom', transform=cbar.ax.transAxes, fontsize=12)
        cbar.ax.text(0.5, -0.05, "Catabolic", ha='center', va='top', transform=cbar.ax.transAxes, fontsize=12)
        
        std_over_time = [0]
        if movement_type == 'random':
            plt.title("Random Movement")
            # Go through movement process for x number of times, where x = iterations.
            for t in range(iterations):
                if t in list(range(0, iterations, 100)):
                    std_over_time.append(self.get_moving_average(0, 0, 0, "Random Movement", plot=False))
                # Loop through each anabolic cell on tissue
                for anabolic in self.anabolic_cells.keys():
                    # Get current cell
                    current_cell = self.anabolic_cells[anabolic]
                    # Get current position of anabolic cell
                    current_position = (current_cell.Get_Row(), current_cell.Get_Column())
                    # Re-assign current position of cell to nan in cell location map to visual remove cell marker
                    self.cell_location[current_position[0], current_position[1]] = np.nan
                    # Call move_random method of tissue to get row and column of new cell location
                    row, column = current_cell.move_random(self.tissue_size)
                    # Change the value of the cell coordinates in cell_location grid to visualize location of cell
                    self.cell_location[row, column] = 1
                    # Cell thickness cannot exceed 1 (100%). Thus if tissue is already at maximum, anabolic cell does not lay down tissue.
                    if round(self.tissue[row, column], 3) >= 1:
                        pass
                    else:
                        self.tissue[row, column] += alpha * beta
                # Repeat process for each catabolic cell.
                for catabolic in self.catabolic_cells.keys():
                    # Get current cell
                    current_cell = self.catabolic_cells[catabolic]
                    current_position = (current_cell.Get_Row(), current_cell.Get_Column())
                    self.cell_location[current_position[0], current_position[1]] = np.nan
                    row, column = current_cell.move_random(self.tissue_size)
                    self.cell_location[row, column] = 0
                    if self.tissue[row, column] <= 0:
                        pass
                    else:
                        self.tissue[row, column] -= self.tissue[row, column] * alpha
                # Re plot tissue and cell location plots
                tissue_plot.set_array(self.tissue)
                cell_plot.set_array(self.cell_location)
                if pause == True:
                    plt.pause(0.01)
            plt.show()

        elif movement_type == 'durotaxis':
            plt.title("Durotaxis")
            # Go through movement process for x number of times, where x = iterations.
            for t in range(iterations):
                if t in list(range(0, iterations, 100)):
                    std_over_time.append(self.get_moving_average(0, 0, 0, "Durotaxis", plot=False))
                # Loop through each anabolic cell on tissue: Process is the same as random movement, except move_durotaxsis is called in
                # replace of move_random
                for anabolic in self.anabolic_cells.keys():
                    current_cell = self.anabolic_cells[anabolic]
                    current_position = (current_cell.Get_Row(), current_cell.Get_Column())
                    self.cell_location[current_position[0], current_position[1]] = np.nan
                    row, column = current_cell.move_durotaxis(self.tissue_size, self.tissue)
                    self.cell_location[row, column] = 1
                    if self.tissue[row, column] >= 1:
                        pass
                    else:
                        self.tissue[row, column] += alpha * beta

                for catabolic in self.catabolic_cells.keys():
                    current_cell = self.catabolic_cells[catabolic]
                    current_position = (current_cell.Get_Row(), current_cell.Get_Column())
                    self.cell_location[current_position[0], current_position[1]] = np.nan
                    row, column = current_cell.move_durotaxis(self.tissue_size, self.tissue)
                    self.cell_location[row, column] = 0
                    if self.tissue[row, column] <= 0:
                        pass
                    else:
                        self.tissue[row, column] -= self.tissue[row, column] * alpha
                tissue_plot.set_array(self.tissue)
                cell_plot.set_array(self.cell_location)
                if pause == True:
                    plt.pause(0.01)
            plt.show()
        return std_over_time
    def get_moving_average(self, figure1, figure2, figure3, title, plot=True):
        window_size = 5
        averages = []
        for row in range(0,self.tissue_size, window_size):
            for col in range(0, self.tissue_size, window_size):
                averages.append(np.mean(self.tissue[row:row+window_size, col:col+window_size]))
        
        avg_array = np.array(averages).reshape((int(self.tissue_size/window_size), int(self.tissue_size/window_size)))
        
        if plot == True:
            # Plot moving average as a line graph with squares ordered 0-1000
            plt.figure(figure1, clear = True)
            plt.title(f'Moving Average of {title}')
            plt.xlabel('Average mass')
            plt.hist(avg_array.flatten(), bins="auto")
            
            # create x and y values for CDF
            x = sorted(avg_array.flatten())
            y = np.arange(len(avg_array.flatten()))/len(avg_array.flatten())
        
            # create and annotate subplot on the left
            plt.figure(figure2, clear=True)
            
            plt.plot(x, y, '.', markersize=20)
            plt.plot(x, y, linewidth=2, c='r')
            plt.xlabel(f"Moving Average Mass of a 5x5 Grid")
            plt.ylabel("P<(x)")
            plt.title(f'CDF for Average Mass of Windows of Tissue {title}')
            
            #plot averages on a heat map
            
            plt.figure(figure3, clear = True)
            plt.title(f' Moving Average Heat map of {title}')
            plt.imshow(avg_array, cmap="hot", interpolation='nearest', vmin=0, vmax=1)
            cbar = plt.colorbar()
            cbar.set_label("Mean Tissue Density", rotation= 270, labelpad=15)
            cbar.ax.text(0.5, 1.05, 'High', ha='center', va='bottom', transform=cbar.ax.transAxes, fontsize=12)
            cbar.ax.text(0.5, -0.05, "Low", ha='center', va='top', transform=cbar.ax.transAxes, fontsize=12)
        # Calculate standard deviation 
        std = np.std(avg_array)    
        
        
        return std
