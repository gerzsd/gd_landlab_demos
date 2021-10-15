# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 12:00:57 2021

@author: gerzsd
"""

from copy import deepcopy

import numpy as np
import matplotlib.pyplot as plt

from landlab import RasterModelGrid
from landlab.plot import imshow_grid
from landlab.io.esri_ascii import read_esri_ascii
from landlab.values import sine
from terrainbento import Basic, Clock
from terrainbento.boundary_handlers import SingleNodeBaselevelHandler


def run_Basic(grid, m_sp, n_sp, time=(0, 10, 1000), **kwds):
    print(m_sp," ", n_sp)
    grid = deepcopy(grid)
    clock = Clock(start=time[0],
                  step=time[1],
                  stop=time[2])
    bch=deepcopy(bh)
    model = Basic(clock, grid,
                  m_sp=m_sp,
                  n_sp=n_sp,
                  boundary_handlers={'SingleNodeBaselevelHandler': bch},
                  **kwds)
    model.run()
    return model


path = './relief__10m_gauss5_nyaraska_1hydro.asc'
rmg, z = read_esri_ascii(path, name='topographic__elevation', halo=1)

min_z = np.min(z[np.where(z > 0)])
max_z = np.max(z[np.where(z > 0)])
lim_z = (min_z, max_z)

rmg.set_watershed_boundary_condition(z, nodata_value=-99999)
outlet_id = rmg.open_boundary_nodes

bh = SingleNodeBaselevelHandler(rmg,
                                outlet_id=outlet_id,
                                lowering_rate=-0.001,
                                )

m_list = [0.4, 0.5, 0.6]
n_list = [0.8, 1.0, 1.2]

basics_m_n_var = [[run_Basic(grid=rmg,
                             m_sp=m,
                             n_sp=n,
                             time=(0, 10, 100),
                             flow_director='FlowDirectorD8')
                  for m in m_list]
                  for n in n_list
                  ]


for i in basics_m_n_var:
    for j in i:
        plt.figure()
        label='m: {} & n: {}'.format(j.m, j.n)
        plt.title(label=label)
        imshow_grid(j.grid, 'cumulative_elevation_change')

