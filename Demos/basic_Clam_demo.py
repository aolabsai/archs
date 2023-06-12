# -*- coding: utf-8 -*-
"""
Thank you for trying our code! We welcome your feedback.
"""



# AO Labs Modules
#from ao_core import ao_core as ao

import ao_core as ao

# 3rd Party Modules
import numpy as np 


#%% # Constructing a Clam agent

# Configuring Architecture
from Architectures import basic_clam     # We've pre-built 3 archs for you in this folder;
arch = basic_clam.bClam                  # use them as a guide to build your own!

# Creating an agent
bc = ao.Agent( arch, "first attempt, basic clam")


#%% # Train agent
 
            # I={F, A, C }  Z={ open/close }   # c0 is by default 1 when a 
bc.reset_state()                              # LABEL is used with .next_state
bc.next_state( [1, 1, 0], [1])
bc.reset_state()
bc.next_state( [1, 0, 0], [1])
bc.reset_state()
bc.next_state( [0, 0, 0], [0])
bc.reset_state()
bc.next_state( [1, 1, 1], [1])
bc.reset_state()


#%% # Test agent

start_state = bc.state

for x in np.arange(200):
    
    bc.next_state([0, 0, 0], DD=False, INSTINCTS=False, unsequenced=True, print_result=False)
    bc.print_result(sel=[3, 4, 5, 6])
    
    bc.reset_state()
 
end_state = bc.state

sel = np.arange( start_state, end_state, 2)
aresults = sum( bc.story[sel, bc.arch.Z__flat])  # so that we're viewing Z-output results of the .next_states, ignoring the .reset_states

print("")
print("The Clam fired "+str(aresults)+"/200 times")


# Now, contrast the above with the method below V
#%% # Creating an agent trained through INSTINCTS

###
###

# Now that was basically the same as training with labels (since we provided the net with input<>output pairs)
# Below we are going to try the same experiment of clam association, but without labelled data;
# the clam will use it's instincts for continous learning

###
###

bcIN = ao.Agent( arch, "first attempt, basic clam")


#%% # Train agent with INSTINCTS
 
 #           I={F, A, C }  Z={ open/close }   # c0 is by default 1 when a 

bcIN.next_state( [0, 0, 0], [0])
bcIN.reset_state()



#%% # Test agent

start_state = bcIN.state

for x in np.arange( 200 ):
    
    bcIN.next_state( [1, 1, 0] , INSTINCTS=True)      # compare response of {0 1 0}
                                                           # to response of {0 0 1} 
    bcIN.reset_state()
 
end_state = bcIN.state

sel = np.arange( start_state, end_state, 2)
bresults = sum( bcIN.story[sel, bcIN.arch.Z__flat])  # so that we're viewing Z-output results of the .next_states, ignoring the .reset_states

print("")
print("The Clam fired "+str(bresults)+" /200 times")

