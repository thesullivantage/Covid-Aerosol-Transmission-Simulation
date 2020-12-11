# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 00:21:18 2020

@author: Jack
"""
import matplotlib.pyplot as plt
import numpy as np 

x = [0, 1, 2]
y = np.abs(x)*3

print(np.arctan2(2, 6)*360)

x = np.linspace(10.5, 10.5*3, 400)

y = 100.5-np.abs(x)*3

print(y[0])
    
    


plt.xlabel('x'); plt.ylabel('cos(x)')
plt.axis([0,100, 0, 105])
plt.plot(x, y, '-', label='test')
plt.show()

