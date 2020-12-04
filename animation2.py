# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 00:35:04 2020

@author: Jack
"""


import numpy as np 
import random as random
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, bitrate=1800)


## 2D Simulation
# number of x & y coordinates
height=100
width=100
# Number of points in each dimension 
numX = 100
numY = 100

# Spatial Step
step = height / numX


### FIX gridX tomrrow!!!!! need in regular meters ! 

# Spatial coordinates
gridX = np.arange(0, 100, step)
gridY = np.arange(0, 100, step)

# Number of people
Np = 50
# per second 
dt = 1
# Diffustion Coefficient (m**2/s)
D = .05

# Average walking speed (m/s) chosen from [1]
avgWalkSpeed = .5
# Volume air inhaled per second (m**3/s)
Vbreathe = .0033
# Removal Timescale (ventilation) (sseconds)
tau = 50
# time from 0 to increment simulation (seconds)
time = 700 

def setCoord():
    hold = int((height-height/25) * random.random())
    if (hold <= height/25):
        hold += int(height/25)
    return hold 

### PEOPLE INSERTION

# Format [currX, currY, Infected, targetArr, coughOffSet, Dose, velocity]
# coughOffSet chosen arbitrarily so all people do not cough on 
# cue at 10 minute intervals
def makePpl(Np):
    array = []
    # Prevalence of Infected Person 
    # ***** May need to come back to this
    infNum = int(Np*.05)

    for p in range(Np): 
        # infected people at infNum percent
        hold = [setCoord(), setCoord(), False, [setCoord(), setCoord()], int(300*random.random()//1), 0]
        if (p <= infNum):
            hold[2] = True
 
        # Otherwise, they are non-infected 

        distance = np.subtract(np.array(hold[3]), np.array(hold[:2]))
        angle = np.arctan2(distance[1], distance[0])
        velArr = [0, 0]
        velArr[0] = .5 * np.cos(angle) 
        velArr[1] = .5 * np.sin(angle)
        hold.append(velArr)
        array.append(hold)
    return array

 
people = makePpl(Np)


## DIFFUSION

# Square step for diffusion equation
step2 = step * step
# Initialize concentration field and "future" concentration
c0 = np.zeros((len(gridX), len(gridY)))
c = c0.copy()

def diffStep(c0, c):
# Diffusion equation, vectorized. 
# Propagate with forward-difference in time, central-difference in space
# D must change depending on dt step size 
######### Thus far drops off at the boundaries
    
    c[1:-1, 1:-1] = c0[1:-1, 1:-1] + dt * D* ((c0[2:, 1:-1] + c0[:-2, 1:-1] + c0[1:-1, 2:] - 4*c0[1:-1, 1:-1] + c0[1:-1, :-2])/step2 )

    c0 = c.copy()
    # c0 is shallow copied for next time, but is same as c 
    return c0, c

def setTarg(coord): 
    
    targ = [setCoord(), setCoord()]

    # will have to loop through all v's eventually, would insert here
    v = np.sqrt(np.abs(coord[0]-targ[0])**2+(coord[1]-targ[1])**2)//1
    while(v < 1 ):
        targ = [setCoord(), setCoord()]
    return targ

def checkTarg(currCord, currTarg): 

    v = np.sqrt(np.abs(currCord[0]-currTarg[0])**2+(currCord[1]-currTarg[1])**2)//1
    # if distance small enough, or close to a wall, give signal 
    # to make new target
    if(v < 0.5 or currCord[0] >= 98 or currCord[1] >= 98 or currCord[0] <= 2 or currCord[1] <= 2):
        return 1
    return 0
        

# Defined for ANIMATION
fig = plt.figure()
ims = []
### UPDATE EVERYTHING
# Loop through each second
for t in range(0, time): 
    
    # # run the diffusion finite difference step
    c0, c = diffStep(c0, c)
    
    # # Ventilation instantaneously removes some particles out of the air per second (1%)
    # We want to be acting on c0 before next iteration
    c0 = c0 - dt * c0/tau
    
    # ANIMATION holders
    healthX = []
    healthY = []
    infX = []
    infY = []
    
    # For each person at each time
    for z in range(Np): 
        
        # Reference data elements for convenience of each person at each time
        # Format [currX, currY, Infected, targetArr, coughOffSet, Dose, vel]
        xCoord = people[z][0]
        yCoord = people[z][1]
        infBool = people[z][2] 
        targetArr = people[z][3]
        coughSet = people[z][4]
        dose = people[z][5]
        xVel = people[z][6][0]
        yVel = people[z][6][1]
        distance = np.array([0, 0])

        
        ## TRANSMISSION
        # If infected
        if (infBool  == True):
            # ANIMATION
            infX.append(people[z][0])
            infY.append(people[z][1])
            # if the person is infected
            # Different result if has just coughed 
            if ( (t + coughSet)  % 600 == 0): 
                # If time to cough, change concentration at current         coordinates
                # of infected person (Quantized nearest their location in 
                # Concentration field)
                c0[int(xCoord), int(yCoord)] += (4*10**5 + 5)
            else: c0[int(xCoord), int(yCoord)] += 5
        else:
            # Holding for Animation
            healthX.append(people[z][0])
            healthY.append(people[z][1])
            # Accumulates dose at coordinate, at pre-determined rate of 
            # breathing at the concentration nearest the person's spatial
            # coordinates (again, quantized for concentration field)
            dose += c0[int(xCoord), int(yCoord)] * Vbreathe
            if (dose >= 1000):
                # If healthy person accumulates critical dose of 100 particles, 
                # infect them with the virus
                people[z][2] = True
        
        
        ## WALKING
        combCoord = people[z][:2] # for convenience
        # check to see if hitting a wall or close to target
        if (checkTarg(combCoord, targetArr) == 1):
            # if yes, create new target
            targetArr = setTarg(combCoord)
            # set new velocity based on angle
            distance = np.subtract(np.array(targetArr), np.array(combCoord))
            angle = np.arctan2(distance[1], distance[0])
            people[z][6][0] = .5 * np.cos(angle) 
            people[z][6][1] = .5 * np.sin(angle)
        
        
        # References to velocity still work, if we've set above
        # Updating the position coordinates of each person in the people array
        # Update each person coordinate with forward Euler forward scheme 
        people[z][0] = xCoord + people[z][6][0] * dt
        people[z][1] = yCoord + people[z][6][1] * dt
        
       
    # ANIMATION- append to array of images
    im = plt.imshow(c0, extent=[0, width, 0, height], origin='lower', animated=True, cmap='Reds')
    # Store each image manually
    ims.append([im])

print(len(ims))
plt.colorbar()
plt.axis(aspect='image');
plt.figure(dpi=150)
ani = animation.ArtistAnimation(fig, ims, interval=1, blit=True, repeat=False)
ani.save('simulation.mp4', writer=writer)





