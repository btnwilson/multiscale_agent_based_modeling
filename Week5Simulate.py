# -*- coding: utf-8 -*-

import Week5Tissue as T
from matplotlib import pyplot as plt
import numpy as np
iterations = 10000
# Create tissue object
random_tissue = T.Tissue(100,20,20)
# simulate random movement on tissue
std_rand_over_time = random_tissue.Simulate_Tissue('random', iterations, 0, 1, pause = False, alpha=.1, beta=.5)

# Create tissue object
durotaxis_tissue = T.Tissue(100,20,20)
# Simulate durotaxis movement on tissue
std_duro_over_time = durotaxis_tissue.Simulate_Tissue('durotaxis', iterations, 0, 1, figure=2, pause = False, alpha=.1, beta= .5)

# Find a way to see if random or durotaxis movement creates more consistent value b

std_rand = random_tissue.get_moving_average(3, 4, 5, 'Random Movement')
std_duro = durotaxis_tissue.get_moving_average(6, 7, 8, 'Durotaxis')
# %%
plt.figure()
plt.plot(np.arange(0, iterations+1, 100), std_rand_over_time, label="Random Movement")
plt.plot(np.arange(0, iterations+1, 100), std_duro_over_time, label="Durotaxis")
plt.xlabel("Time in number of iterations")
plt.ylabel("Standard Deviation of Sliding Window Means")
plt.legend()
