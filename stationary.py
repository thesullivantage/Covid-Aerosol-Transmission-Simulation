import numpy as np 
import random as random
import matplotlib.pyplot as plt 
# from matplotlib.animation import FuncAnimation, PillowWriter  


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

    
# First Person
healthCoord = [setCoord(), setCoord()]




def setPpl(healthCoord, infCoord): 
    infCoord = [setCoord(), setCoord()]

    # will have to loop through all v's eventually, would insert here
    v = np.sqrt(np.abs(healthCoord[0]-infCoord[0])**2+(healthCoord[1]-infCoord[1])**2)//1
    # remember, in terms of steps
    while(v < 5 ):
        
       infCoord = [setCoord(), setCoord()]
    # (and end here)
    return infCoord

infCoord = setPpl()

# SOURCE Here

## Diffusion
time = 3600 
# per second - I think that would make D correct
dt = 1
# Diffustion Coefficient
D = .05
# Square step for diffusion equation
step2 = step * step

c0 = np.zeros((len(gridX), len(gridY)))
c = c0.copy()


def diffStep(c0, c):
# Diffusion equation, vectorized. 
# Propagate with forward-difference in time, central-difference in space
# D must change depending on step size 
    c[1:-1, 1:-1] = c0[1:-1, 1:-1] + dt * D* ((c0[2:, 1:-1] - 2*c0[1:-1, 1:-1] + c0[:-2, 1:-1] + c0[1:-1, 2:] - 2*c0[1:-1, 1:-1] + c0[1:-1, :-2])/step2 )

    c0 = c.copy()
    # c0 is stored for next time, but is same as c 
    return c0, c



def setTarg(coord): 
    
    targ = [setCoord(), setCoord()]

    # will have to loop through all v's eventually, would insert here
    v = np.sqrt(np.abs(coord[0]-targ[0])**2+(coord[1]-targ[1])**2)//1
    # remember, in terms of steps
    while(v < 5 ):
       targ = [setCoord(), setCoord()]
    # (and end here)
    return targ

# Need a person array now Np x 3 (x, y, bool)
    # true = infected
    # on creation, do percent infected 
    # down the code, conditional expulsion vs. not at their coord
# need convert coord to 2D array
# For Each Person: 
# have Np x  4 (vX, vY, target, target) array for toTarget components (global)
# for each time step
    ## maybe lump this as below function:
    # for each person`
        
        # check reached (within R) 
        # if beginning or (reached):
            # set target 
            # Calculate X & Y velocity to get there: set
        # increment by timestep (finite difference)
        
        
        
def personStep(coord0, coord):
    
    # COME BACK HERE
    setTarg()
    
    # initial position of person inputted
    
    # pick target 
    # Start walking there 
        # fixed walking speed (by r) -- need calculate
    # when reached target or  (< 1 m) of boundary: pick new target rmax away    
    # check to see if within .5 of other person
    # if yes, bounce 
    pass
    # do vectorized again 
    # finite difference 


# for each person: 
    # get target (out of array)

### ANIMATION: This needs to be defined as an update function: read docs later, have commented out for loop 

for t in range(0, 5200): 
    
    # run the diffusion finite difference step
    c0, c = diffStep(c0, c)
    
    # cough at at the beginning of time, and then every 10 minutes
    if (t == 0 or t % 600 == 0): 
        c0[infCoord[0], infCoord[1]] += (4*10**5 + 5)
        
    # Normal Breathing (per second)
    c0[infCoord[0], infCoord[1]] += 5
    
    # Ventilation instantaneously removes some particles out of the air per second (1%)
    c0 = c0 - dt * c0/100
    
    # Find frequency of talking and put it here



plt.imshow(c, extent=[0, 100, 0, 100], origin='lower',
            cmap='Reds')
plt.colorbar()
plt.axis(aspect='image');



# dosing
# if (c[healthX, healthY] > 1):
#     plt.plot(gridX[healthX], gridY[healthY],           'ro')

# plt.plot(gridX[healthX], gridY[healthY],           'bo')


# for a in range(0, len(gridX)):
#     for b in range(0,len(gridY)):
#         if (c[a,b] > 1000): 
#             print(c[a, b])

# plt.plot(gridX[infX], gridY[infY], 'ro')
# plt.legend(loc='best', borderaxespad=.3)
# # plt.xlabel('x');plt.ylabel('high order')
# plt.grid(True)
plt.show()


