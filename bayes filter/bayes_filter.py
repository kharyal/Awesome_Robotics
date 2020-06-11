#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import matplotlib.pyplot as plt
import random
import keyboard
import time


# Default values
# 
# $   p(z_t = sense-open|x_t = open) = 0.7 $    
# $   p(z_t = sense-closed|x_t = closed) = 0.7 $
# 
# $   p(x_t = open| u_t = push, x_{t-1} = open) = 1 $ <br />
# $   p(x_t = open| u_t = push, x_{t-1} = closed) = 0.8 $<br />
# $   p(x_t = closed| u_t = push, x_{t-1} = closed) = 0.2 $<br />
# $   p(x_t = closed| u_t = push, x_{t-1} = open) = 0 $<br />
# $   p(x_t = closed| u_t = pull, x_{t-1} = open) = 0.7 $<br />
# $   p(x_t = closed| u_t = pull, x_{t-1} = closed) = 1 $<br />
# $   p(x_t = open| u_t = pull, x_{t-1} = closed) = 0 $<br />
# $   p(x_t = close| u_t = pull, x_{t-1} = open) = 0.7 $<br />
# $   p(x_t = open| u_t = pull, x_{t-1} = open) = 0.3 $<br />
# 
# $   p(x_t = open| u_t = do-nothing, x_{t-1} = open) = 1 $<br />
# $   p(x_t = open| u_t = do-nothing, x_{t-1} = closed) = 0 $<br />
# $   p(x_t = close| u_t = do-nothing, x_{t-1} = open) = 0 $<br />
# $   p(x_t = closed| u_t = do-nothing, x_{t-1} = closed) = 1 $<br />
# 
# 
#    
# 

# In[21]:


# BAYES FILTER
'''
    Environment: 
        A robot tryng to open/close a door and estimate the state (open/close) of the door
'''
"""
    probability array:
                        open_to_open   open_to_closed   closed_to_closed   closed_to_open
        u = nothing          xxx            xxx               xxx                xxx
        u = push             xxx            xxx               xxx                xxx
        u = pull             xxx            xxx               xxx                xxx
"""

p = np.array([[1,   0, 1,   0],
              [1,   0, 0.2, 0.8],
              [0.3, 0.7, 1, 0]])
states = []
bel = []
crashed = False
state = random.randint(0,1)  ## random initial state, completely unknown to the robot

bel_open = 0.5
bel_closed = 1 - bel_open
bel_open_ = 0.5
bel_closed_ = 1-bel_open_

while not crashed:
    if keyboard.is_pressed('q'):
        crashed = True
    
    elif keyboard.is_pressed('w'):
        bel_open_ = p[1][0]*bel_open + p[1][1]*bel_closed
        bel_closed_ = 1 - bel_open_
        rand = random.uniform(0,1)
        if state == 0 and rand<=0.8:
            state = 1
                
    elif keyboard.is_pressed('s'):
        bel_open_ = p[2][0]*bel_open + p[2][1]*bel_closed
        bel_closed_ = 1 - bel_open_
        rand = random.uniform(0,1)
        if state == 1 and rand<=0.7:
            state = 0
    else:
        bel_open_ = p[0][0]*bel_open + p[0][1]*bel_closed
        bel_closed_ = 1 - bel_open_
    
    bel_open = 0.7*state*bel_open_ + 0.3*(1-state)*bel_open_
    bel_closed = 0.3*state*bel_closed_ + 0.7*(1-state)*bel_closed_
        
    eta = bel_open + bel_closed
    bel_open = bel_open/eta
    bel_closed = bel_closed/eta
    
    states.append(state)
    bel.append(bel_open)
    
    print("state:",state)
    print("bel:",bel_open)
    time.sleep(1)

fig = plt.figure()
ax = plt.axes()
ax.plot(bel,label='belief', linestyle='--')
ax.plot(states,label='state')
plt.legend()
plt.show()


# In[15]:




