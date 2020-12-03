import numpy as np 
import random as random
import matplotlib.pyplot as plt 
# from matplotlib.animation import FuncAnimation, PillowWriter  


## 2D Simulation
# number of x & y coordinates
height=100 
width=100
# Number of points in each dimension 
numX = 2000
numY = 2000

# .05 steps
step = height / numX


### FIX gridX tomrrow!!!!! need in regular meters ! 

# Spatial coordinates
gridX = np.arange(0, 100, 1)
gridY = np.arange(0, 100, 1)

def randLoc(): 
    return int(len(gridX) * random.random()//1)

def setCoord():
    hold = randLoc()
    while (hold in range(0,100) or hold in range(1900,2000)):
        hold = randLoc()
    return hold

# need randLoc() not be near existing coord
# take pythag. of x & y diff... but not here?
# get first two 
# For now, just make sure x & y at least certain distance away
#### Probably should convert ppl to matrix 
    
healthX = setCoord()
healthY = setCoord()

def setPpl(): 
    infX = setCoord()
    infY = setCoord()
    # will have to loop through all v's eventually, would insert here
    v = np.sqrt(np.abs(healthX-infX)**2+(healthY-infY)**2)//1
    # remember, in terms of steps
    while(v < 200 ):
        infX = setCoord()
        infY = setCoord()
    # (and end here)
    return infX, infY

infX, infY = setPpl()

# SOURCE Here

## Diffusion
# Can just increment by one, no need for diffusion coefficient -- still need talk about it
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
    c[1:-1, 1:-1] = c0[1:-1, 1:-1] + dt * D* ((c0[2:, 1:-1] - 2*c0[1:-1, 1:-1] + c0[:-2, 1:-1] + c0[1:-1, 2:] - 2*c0[1:-1, 1:-1] + c0[1:-1, :-2])/step2 )

    c0 = c.copy()
    # c0 is stored for next time, but is same as c 
    return c0, c





### ANIMATION: This needs to be defined as an update function: read docs later, have commented out for loop 

for t in range(0, 60): 
    
    c0, c = diffStep(c0, c)
    
    # cough at certain inverval (6 times an hour)
    if (t == 0 or t % 600 == 0): 
        c0[infX, infY] += (4*10**5 + 5)
        
    # Normal Breathing (per second)
    c0[infX, infY] += 5
    
    # Find frequency of talking and put it here

counter = 0
for a in range(0, len(gridX)):
    for b in range(0,len(gridY)):
        if (c[a,b] == 0): 
            counter +=1 
print(counter)


plt.imshow(c, extent=[0, 100, 0, 100], origin='lower',
            cmap='RdGy')
plt.colorbar()
plt.axis(aspect='image');


# plt.xlabel('x'); plt.ylabel('cos(x)')
# plt.axis([0, 100, 0, 100])
# plt.plot(gridX[healthX], gridY[healthY], 'bo')
# plt.plot(gridX[infX], gridY[infY], 'ro')
# plt.legend(loc='best', borderaxespad=.3)
# # plt.xlabel('x');plt.ylabel('high order')
# plt.grid(True)
plt.show()


