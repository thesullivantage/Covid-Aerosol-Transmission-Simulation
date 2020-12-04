import numpy as np 
import random as random
import matplotlib.pyplot as plt 
# from matplotlib.animation import FuncAnimation, PillowWriter  
from matplotlib.animation import FuncAnimation, PillowWriter  


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


def setCoord():
    hold = int((height-height/25) * random.random())
    if (hold <= height/25):
        hold += int(height/25)
    return hold 



### PEOPLE INSERTION
# Number of people
Np = 50
# Format [currX, currY, Infected, targetArr, coughOffSet, Dose]
# coughOffSet chosen arbitrarily so all people do not cough on cue at 10 minute intervals
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

 
people = makePpl(100)


## DIFFUSION

# per second 
dt = 1
# Diffustion Coefficient
D = .05
# Square step for diffusion equation
step2 = step * step

# Initialize concentration field and "future" concentration
c0 = np.zeros((len(gridX), len(gridY)))
c = c0.copy()

def diffStep(c0, c):
# Diffusion equation, vectorized. 
# Propagate with forward-difference in time, central-difference in space
# D must change depending on step size 
######### Thus far drops off at the boundaries
    
    c[1:-1, 1:-1] = c0[1:-1, 1:-1] + dt * D* ((c0[2:, 1:-1] - 2*c0[1:-1, 1:-1] + c0[:-2, 1:-1] + c0[1:-1, 2:] - 2*c0[1:-1, 1:-1] + c0[1:-1, :-2])/step2 )

    c0 = c.copy()
    # c0 is shallow copied for next time, but is same as c 
    return c0, c


## Walking

# In m/s

# Average particles inhaled per second [m**-2]
avgWalkSpeed = .5
Vbreathe = .33
tau = 50
time = 3600 

def setTarg(coord): 
    
    targ = [setCoord(), setCoord()]

    # will have to loop through all v's eventually, would insert here
    v = np.sqrt(np.abs(coord[0]-targ[0])**2+(coord[1]-targ[1])**2)//1
    # remember, in terms of steps
    while(v < 1 ):
        targ = [setCoord(), setCoord()]
    # (and end here)
    return targ

def checkTarg(currCord, currTarg): 

    v = np.sqrt(np.abs(currCord[0]-currTarg[0])**2+(currCord[1]-currTarg[1])**2)//1
    if(v < 0.5 or currCord[0] >= 98 or currCord[1] >= 98 or currCord[0] <= 2 or currCord[1] <= 2):
        return 1
    return 0
    
 
# ANIMATION
fig, ax = plt.subplots()    
ln1, = plt.plot([], [], 'ro')  
ln2, = plt.plot([], [], 'm*')  
ln3, = plt.imshow([], extent=[0, width, 0, height], origin='lower',cmap='Reds')
# IT'S TIME!
def update(t):
        
    # Need to bring these into this function   
    global c0
    global c

    #### Uncomment this when person done! 
    # # run the diffusion finite difference step
    c0,  c = diffStep(c0, c)
    
    # # Ventilation instantaneously removes some particles out of the air per second (1%)
    c0 = c0 - dt * c0/tau
    
    # ANIMATION
    healthX = []
    healthY = []
    infX = []
    infY = []
    
    for z in range(Np): 
        xCoord = people[z][0]
        yCoord = people[z][1]
        infBool = people[z][2] 
        targetArr = people[z][3]
        dose = people[z][5]
        distance = np.array([0, 0])

        # Could use copy here
        # Format [currX, currY, Infected, targetArr, coughOffSet, Dose]
        ##### TRANSMISSION
        if (infBool  == True):
            infX.append(people[z][0])
            infY.append(people[z][1])
            # if the person is infected
            # Different result if has just coughed 
            if ( t  % 600 == 0): 
                # If time to cough, change concentration at current coordinates
                # of infected person (Quantized nearest their location in 
                # Concentration field)
                print(t)
                c0[int(xCoord), int(yCoord)] += (4*10**5 + 5)
                # ANIMATION
                
            else: 
                c0[int(xCoord), int(yCoord)] += 5
        else:
            # ANIMATION: 
            healthX.append(people[f][0])
            healthY.append(people[f][1])
            dose += c0[int(xCoord), int(yCoord)] * Vbreathe
            if (dose >= 1000):
                # If healthy person accumulates critical dose of 100 particles, 
                # infect them with the virus
                people[z][2] = True
        
        
        
        combCoord = people[z][:2]
        ## WALKING
        if (checkTarg(combCoord, targetArr) == 1):
            targetArr = setTarg(combCoord)
            distance = np.subtract(np.array(targetArr), np.array(combCoord))
            angle = np.arctan2(distance[1], distance[0])
            people[z][6][0] = .5 * np.cos(angle) 
            people[z][6][1] = .5 * np.sin(angle)
        
        
        # References to velocity still work, if we've set above
        # Updating the position coordinates of each person in the people array
        people[z][0] = xCoord + people[z][6][0] * dt
        people[z][1] = yCoord + people[z][6][1] * dt
    
    # Ready to write everything to animation     
    ln1.set_data(healthX, healthY)
    ln2.set_data(infX, infY)
    ln3.set_data(c)        
    
plt.colorbar()
plt.axis(aspect='image');
plt.figure(dpi=150)
ani = FuncAnimation(fig, update, np.linspace(0, 60, 1))
plt.show()

counter = 0
for f in range(Np): 
    if (people[f][2] == True):
        counter += 1 
        

print("Infected: ", counter)









