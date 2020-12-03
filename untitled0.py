# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 16:37:38 2020

@author: Jack
"""

import numpy as np
import random

## 2D Simulation
# number of x & y coordinates
height=100 
width=100
# Number of points in each dimension 
numX = 100
numY = 100

# .05 steps
step = height / numX


### FIX gridX tomrrow!!!!! need in regular meters ! 

# Spatial coordinates
gridX = np.arange(0, 100, step)
gridY = np.arange(0, 100, step)

def randLoc(): 
    return int(len(gridX) * random.random()//1)

def setCoord():
    hold = randLoc()
    while (hold in range(0,int(height/20)) or hold in range(int(height-height/20),height)):
        hold = randLoc()
    return hold

print(setCoord())
