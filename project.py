#!/usr/bin/env python
# coding: utf-8

# In[11]:


# Fixed parameters

import math  
import random as rnd  
import numpy as np 
import matplotlib.pyplot as plt  
from scipy import stats

frontage = 400*1852
depth = 300*1852
SpeedE = 60
SpeedA = 600
SweepWidth = 100*1852
timeUnit = 1
incrShipx = 0
incrShipy = SpeedE/timeUnit
incrMPAx = SpeedA/timeUnit
incrMPAy = 0
ShortLeg = 180
iterations=10
Num_Aircraft = 5



Det_prob = []
for a in range(Num_Aircraft):
    vector = []
    total_ships= []
    for i in range(iterations):
        startMPAx = (SweepWidth/2)+rnd.uniform(0, frontage-(SweepWidth/2)) 
        startMPAy = (SweepWidth/2)+rnd.uniform(0, depth-(SweepWidth/2)) 
        startShipx = rnd.uniform(0, frontage) 
        startShipy = depth
        numLongLeg = 1 + round((depth - SweepWidth)/ShortLeg) # calculate more precisely
        T = round(min(depth*timeUnit/SpeedE, numLongLeg*((frontage-SweepWidth)*timeUnit + (numLongLeg-1)*ShortLeg*timeUnit)/SpeedA))

        # Check if detected or not at each time unit (can be improved)
        xshipPrev = startShipx
        yshipPrev = startShipy
        xMPAPrev = startMPAx
        yMPAPrev = startMPAy
        changeDir = False
        for t in range(T):
            if (changeDir):
                yMPANow = yMPAPrev + ShortLeg
                incrMPAx = -incrMPAx
                changeDir = False
            xshipNow = xshipPrev - incrShipx
            yshipNow = yshipPrev - incrShipy
            xMPANow = xMPAPrev + incrMPAx
            yMPANow = yMPAPrev + incrMPAy

            #print (yshipNow, xMPANow)

            # Detection
            if (xshipNow >= (xMPANow - SweepWidth/2) and xshipNow <= (xMPANow + SweepWidth/2) 
                and yshipNow >= (yMPANow - SweepWidth/2) and yshipNow <= (yMPANow + SweepWidth/2)):
                detected = True
                #print ("DETECTED!")
                #print (t,T)
                break

            # Check if direction of MPA should be changed
            if (xMPANow <= SweepWidth/2 or xMPANow >= frontage - SweepWidth/2):
                changeDir = True

            xshipPrev = xshipNow
            yshipPrev = yshipNow
            xMPAPrev = xMPANow
            yMPAPrev = yMPANow
            vector.append(t)
            total_ships.append(T)
        
    total_ships = np.array(total_ships)
    vector  = np.array(vector)
    Mean = sum(vector)/len(vector)
    Mean_total = sum(total_ships)/len(total_ships)
    print("Mean number of ships detected: ",math.floor(Mean))
    print("Total number of ships: ",math.floor(Mean_total))
    DetectionProbability = Mean/Mean_total
    Det_prob.append(DetectionProbability)
    print("Detection Probability for aircraft", a+1 , "is : ", DetectionProbability)


# To calculate overall detection probability
q = 1
for a in range(Num_Aircraft):
    d = 1- Det_prob[a]
    q *= d
overall_det_prob = 1 - q

print("Overall Detection Probability is : ", overall_det_prob)