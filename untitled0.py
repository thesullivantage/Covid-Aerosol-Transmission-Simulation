# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 23:36:33 2020

@author: Jack
"""


import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

rZero = 10.5
rOne = 10.5*3
# add a lil more on the bottom

# Create the mesh in polar coordinates and compute corresponding Z.
r = np.linspace(rZero, rOne, 50)
p = np.linspace(0, 2*np.pi, 50)
R, P = np.meshgrid(r, p)




intercept = 100.5
# Height
newZ = (intercept)-np.abs(R)*3
# start at 69
# phi = (-25, 25)
# pi = (0, 2*np.pi)
# z = (0, 1)


## LIGHTS
# from rZero, rOne
# Spacing: 

# Express the mesh in the cartesian system.
X, Y = R*np.cos(P), R*np.sin(P)

# Plot the surface.
ax.plot_surface(X, Y, newZ, cmap=plt.cm.YlGnBu_r)

# Tweak the limits and add latex math labels.
ax.set_zlim(0, 75)
ax.set_xlabel(r'$\phi_\mathrm{real}$')
ax.set_ylabel(r'$\phi_\mathrm{im}$')
ax.set_zlabel(r'$V(\phi)$')

plt.show()

# Finding our intercept: 
# (10.5, 69)
# (10, 70.5)
# (0, 100.5)

# X at 33.5