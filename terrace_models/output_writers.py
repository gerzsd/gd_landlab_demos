# -*- coding: utf-8 -*-
"""
Output writes functions for terrainbento models.

@author: gerzsd
"""
import time

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
    print(m.model_time)

def surface_output_writer_png(model):
    min = model.grid.at_node['initial_topographic__elevation'].min()
    max = model.grid.at_node['initial_topographic__elevation'].max()
    T_str = str(round(model.model_time))
    X = model.grid.node_vector_to_raster(model.grid.node_x,
                                         flip_vertically=1)
    Y = model.grid.node_vector_to_raster(model.grid.node_y,
                                         flip_vertically=1)
    Z = model.grid.node_vector_to_raster(model.z,
                                         flip_vertically=1)
    fig = plt.figure(figsize=(10, 4))
    fig.suptitle('Model time: ' + T_str)
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X[1:-1, 1:-1],
                           Y[1:-1, 1:-1],
                           Z[1:-1, 1:-1],
                           cmap='terrain',
                           vmin=min,
                           vmax=max)
    ax.set_zlim(min, max)
    fig.colorbar(surf)
#    plt.show()
    fname = "hillslope_2_" + T_str + ".png"
    plt.savefig(fname)

def plot_all(model):
    pkeys = model.grid.at_node.keys()
    for i in pkeys:
        figure(i)
        plt.title(i)
        imshow_grid(model.grid, i)

def print_model_time(model):
    print(model.model_time)

def print_model_local_time(model):
    local_time = time.asctime(time.localtime())
    model_time = model.model_time
    print("Model time: {} - Local time: {}".format(model_time, local_time))
