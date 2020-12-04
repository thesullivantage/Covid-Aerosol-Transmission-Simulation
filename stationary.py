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


def setCoord():
    hold = int(int(height-height/25) * random.random())
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
        hold = [setCoord(), setCoord(), False, [setCoord(), setCoord()], int(500*random.random()//1), 0]
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




# ###############################3

# SOURCE Here

## DIFFUSION
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
######### Thus far drops off at the boundaries
    
    c[1:-1, 1:-1] = c0[1:-1, 1:-1] + dt * D* ((c0[2:, 1:-1] - 2*c0[1:-1, 1:-1] + c0[:-2, 1:-1] + c0[1:-1, 2:] - 2*c0[1:-1, 1:-1] + c0[1:-1, :-2])/step2 )

    c0 = c.copy()
    # c0 is stored for next time, but is same as c 
    return c0, c



## Walking
avgWalkSpeed = .5
# In m/s
    
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
        



Vbreathe = .33
tau = 75


# IT'S TIME! 
for t in range(0, 700): 
    

    #### Uncomment this when person done! 
    # # run the diffusion finite difference step
    c0, c = diffStep(c0, c)
    
    # # Ventilation instantaneously removes some particles out of the air per second (1%)
    c0 = c0 - dt * c0/tau
    

    for z in range(Np): 
 
        xCoord = people[z][0]
        yCoord = people[z][1]
        infBool = people[z][2] 
        targetArr = people[z][3]
        coughSet = people[z][4]
        dose = people[z][5]
        xVel = people[z][6][0]
        yVel = people[z][6][1]
        distance = np.array([0, 0])

        # Could use copy here
        # Format [currX, currY, Infected, targetArr, coughOffSet, Dose]
        ##### TRANSMISSION
        if (infBool  == True):
            # if the person is infected
            if ( t  % 600 == 0): 
                # If time to cough, change concentration at current coordinates
                # of infected person (Quantized nearest their location in 
                # Concentration field)
                c0[int(xCoord), int(yCoord)] += (4*10**5 + 5)
            else: c0[int(xCoord), int(yCoord)] += 5
        else: 
# =============================================================================
#             # coordinates are lined up from the beginning 
# =============================================================================
            # print(people[z][0], " ", people[z][1])
            dose += c0[int(xCoord), int(yCoord)] * Vbreathe
            if (dose >= 700):
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
        

        

plt.imshow(c, extent=[0, width, 0, height], origin='lower',cmap='Reds')

    

counter = 0
for f in range(Np): 
    if (people[f][2] == True):
        counter += 1 
    # plt.plot(people[f][:2], 'm*')
print(counter)
    

plt.colorbar()
plt.axis(aspect='image');

####### PEOPLE 

        # Need to invent random starting times for each person, can do in person array
        # cough at at the beginning of time, and then every 10 minutes

        # Normal Breathing (per second)
        
        
        # GET DOSE, change person; will start coughing & breathing next time

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


   
    
    
    
    # Find frequency of talking and put it here







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


