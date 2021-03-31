# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 23:43:45 2021

@author: gerzsd
"""

import numpy as np
from landlab.utils import get_watershed_masks
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, subplot
from landlab import imshow_grid

def output_writer_1(m):

    min_z = np.min(m.z[np.where(m.z > 0)])
    max_z = np.max(m.z[np.where(m.z > 0)])
    lim_z = (min_z, max_z)
    # Creating the watershed masks from the model's model grid.
    mask = get_watershed_masks(m.grid)
    # Creating the figure with the subplots.
    figure(figsize=(20, 4))
    subplot(151)
    imshow_grid(m.grid, 'initial_topographic__elevation',
                plot_name='initial_topographic__elevation',
                cmap='terrain',
                color_for_closed=None,
                limits=lim_z,
                shrink=0.5)
    subplot(152)
    imshow_grid(m.grid, 'topographic__elevation',
                plot_name=f'topographic__elevation -{m.model_time}',
                cmap='terrain',
                color_for_closed=None,
                limits=lim_z,
                shrink=0.5)

    subplot(153)
    imshow_grid(m.grid, 'cumulative_elevation_change',
                plot_name=f'Cumulative elevation change - {m.model_time}',
                cmap='viridis',
                color_for_closed=None,
                shrink=0.5)

    subplot(154)
    imshow_grid(m.grid, 'topographic__steepest_slope',
                plot_name=f'topographic__steepest_slope - {m.model_time}',
                cmap='YlOrRd',
                color_for_closed=None,
                shrink=0.5)

    subplot(155)
    imshow_grid(m.grid, mask,
                plot_name=f'Watersheds - {m.model_time}',
                cmap='tab20b',
                color_for_closed=None,
                shrink=0.5)

    plt.tight_layout()
    plt.show()