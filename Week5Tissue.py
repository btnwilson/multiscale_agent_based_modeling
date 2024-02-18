"""
Created on 02.18.2024

"""

import numpy as np
import random as r
import Week5Cell as C
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

    def Simulate_Tissue(self, movement_type, iterations, vmin, vmax, bitesize, pause=True, figure = 1):
        # Initialize cells
        self.initialize_catabolic_cells()
        self.initialize_anabolic_cells()
        # Create figure
        plt.figure(figure)
        tissue_plot = plt.imshow(self.tissue, cmap='gray', interpolation='nearest', vmin=vmin, vmax=vmax)
        cell_plot = plt.imshow(self.cell_location, cmap='winter', interpolation='nearest', vmin=vmin, vmax=vmax)
        plt.colorbar(tissue_plot)

        if movement_type == 'random':
            plt.title("Random Movement")
            # Go through movement process for x number of times, where x = iterations.
            for t in range(iterations):
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
                    if self.tissue[row, column] == 1:
                        pass
                    else:
                        self.tissue[row, column] += bitesize
                # Repeat process for each catabolic cell.
                for catabolic in self.catabolic_cells.keys():
                    # Get current cell
                    current_cell = self.catabolic_cells[catabolic]
                    current_position = (current_cell.Get_Row(), current_cell.Get_Column())
                    self.cell_location[current_position[0], current_position[1]] = np.nan
                    row, column = current_cell.move_random(self.tissue_size)
                    self.cell_location[row, column] = 0
                    if self.tissue[row, column] == 0:
                        pass
                    else:
                        self.tissue[row, column] -= bitesize
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
                # Loop through each anabolic cell on tissue: Process is the same as random movement, except move_durotaxsis is called in
                # replace of move_random
                for anabolic in self.anabolic_cells.keys():
                    current_cell = self.anabolic_cells[anabolic]
                    current_position = (current_cell.Get_Row(), current_cell.Get_Column())
                    self.cell_location[current_position[0], current_position[1]] = np.nan
                    row, column = current_cell.move_durotaxis(self.tissue_size, self.tissue)
                    self.cell_location[row, column] = 1
                    if self.tissue[row, column] == 1:
                        pass
                    else:
                        self.tissue[row, column] += bitesize

                for catabolic in self.catabolic_cells.keys():
                    current_cell = self.catabolic_cells[catabolic]
                    current_position = (current_cell.Get_Row(), current_cell.Get_Column())
                    self.cell_location[current_position[0], current_position[1]] = np.nan
                    row, column = current_cell.move_durotaxis(self.tissue_size, self.tissue)
                    self.cell_location[row, column] = 0
                    if self.tissue[row, column] == 0:
                        pass
                    else:
                        self.tissue[row, column] -= bitesize
                tissue_plot.set_array(self.tissue)
                cell_plot.set_array(self.cell_location)
                if pause == True:
                    plt.pause(0.01)
            plt.show()