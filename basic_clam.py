# -*- coding: utf-8 -*-
"""
Thank you for trying our code! We welcome your feedback.

Created on Thu Jul 14 00:37:29 2022
@author: aee@aolabs.ai 
"""
# AO Labs Modules
import ao_core as ao

# 3rd Party Modules
import numpy as np

#%%
arch_note = "Basic clam architecture; the fundmental, smallest possible reference design\
    with 3 I neurons (FAC), 3 Q neurons (mirrors I), 1 Z neuron (open/close),\
    and 4 C neurons (the 3 defaults: label, Cpos, Cneg for commanding, and 1 pleasure instinct neuron)\
    -- 11 neurons total"
arch = ao.Arch(arch_note)

## Topology
    # Number and shape of neurons

# Channels of data
arch.I_channels = 1
arch.Q_channels = 1     
arch.Z_channels = 1
arch.C_channels = 1

# Creating registery of WNNs for each layer
arch.I = np.arange(arch.I_channels, dtype='O')
arch.Q = np.copy(arch.I)     # Q is by default a mirror copy of I
arch.Z = np.arange(arch.Z_channels, dtype='O')
arch.C = np.arange(arch.C_channels, dtype='O')

# Populating the registries with unique identifiers for the WNNs

## number of neurons
arch.i = (3,)     # FAC
arch.q = (3,)     # Q mirrors I
arch.z = (1,)     # 1 neuron for open/close
arch.c = (4,)         # 1 control neuron to identify training vs. inference states
arch.n_total = sum(arch.i) + sum(arch.q) + sum(arch.z) + sum(arch.c)

# # nids of neurons
arch.I[0] = np.arange(3)
arch.Q[0] = np.arange(3, 6)
arch.Z[0] = np.arange(6, 7)
arch.C[0] = np.arange(7, 11)
arch.IQZC = np.arange(arch.n_total)
arch.IQZ = np.arange(arch.n_total - sum(arch.c))

arch.I__flat = np.concatenate(arch.I, axis=None).ravel() 
arch.Q__flat = np.concatenate(arch.Q, axis=None).ravel() 
arch.Z__flat = np.concatenate(arch.Z, axis=None).ravel() 
arch.C__flat = np.concatenate(arch.C, axis=None).ravel() 
arch.QZ__flat = np.concatenate((arch.Q__flat, arch.Z__flat))

# Defining Neuron metadata
arch.datamatrix = np.zeros([5, arch.n_total], dtype="O")
# 5 rows, as follows:
    #0 Type
    #1 Input Connections; during iconic learning / formation of neuron lookup table (tsets), input connections are taken from the current state
    #2 Neighbor Connections; in constrast to input connections, these take from the past state
    #3 C Connections; neurons connections to C
    #4 Dominant Connection; 1 connection only; a CGA type neuron copies its dominant connection 
    #    ** note; the dominant connection is critical; it is why Q is made in the shape/size of I, so that each Q has a corresponding I as dominant connection (the dominant connection for Z is its own past state [-1]; since if the NSM did something "good / triggered C(s) pleasure neuron(s)" during iconic training, Q will be dominated by I and Z by its past Z (the training becomes; given C at state s, store I(s) and Z(s-1) since Z(s-1) led to the I(s) which triggered C(s)

arch.datamatrix[0, arch.I__flat] = "Input"
arch.datamatrix[0, arch.Q__flat] = "CGA Q"
arch.datamatrix[0, arch.Z__flat] = "CGA Z"
arch.datamatrix[0, arch.C__flat] = "Control"

arch.datamatrix[1, arch.Q[0][0]] = arch.I__flat
arch.datamatrix[1, arch.Q[0][1]] = arch.I__flat  # let's see what this does
arch.datamatrix[1, arch.Q[0][2]] = arch.I__flat
# arch.datamatrix[1, arch.Q[0][3]] = arch.I__flat

arch.datamatrix[1, arch.Z[0][0]] = arch.Q__flat


arch.datamatrix[2, arch.Q[0][0]] = arch.Q__flat
arch.datamatrix[2, arch.Q[0][1]] = arch.Q__flat
arch.datamatrix[2, arch.Q[0][2]] = arch.Q__flat
# arch.datamatrix[2, arch.Q[0][3]] = arch.Q__flat

arch.datamatrix[2, arch.Z[0][0]] = arch.Z__flat


arch.datamatrix[3, arch.QZ__flat] = [arch.C__flat]
arch.datamatrix[3, arch.C[0][0]] = arch.QZ__flat
arch.datamatrix[3, arch.C[0][1]] = arch.QZ__flat
arch.datamatrix[3, arch.C[0][2]] = arch.QZ__flat
arch.datamatrix[3, arch.C[0][3]] = arch.QZ__flat
# arch.datamatrix[3, arch.C[0][4]] = arch.QZ__flat


arch.datamatrix[4, arch.Q__flat] = arch.I__flat
arch.datamatrix[4, arch.Z__flat] = arch.Z__flat
arch.datamatrix[4, arch.C[0][0]] = "Default if label"
arch.datamatrix[4, arch.C[0][1]] = "C+ pleasure signal"
arch.datamatrix[4, arch.C[0][2]] = "C- pain signal"

arch.C__flat_command= np.array([7, 8, 9])
arch.C__flat_pleasure= np.array([7, 8, 10])
arch.C__flat_pain= np.array([9])

arch.hasInstincts = True

def c0_instinct_rule(INPUT, Agent):

    # if F == 1, C = 1
    
    if INPUT[0] == 1    and    Agent.story[ Agent.state-1,  Agent.arch.Z__flat] == 1 :
        
        instinct_response = [1, "F/I[0]=1, food!"]
    
    else:
        instinct_response = [0, "pass0"]
    
    return instinct_response
            
arch.datamatrix[4, arch.C[0][3]] = c0_instinct_rule




#%%

b4Clam = ao.Arch("Same as arch except with an extra neuron in I, corresponding neuron in Q, and extra pain instinct C neuron-- 14 neurons total")


## Topology
    # Number and shape of neurons

# Channels of data
b4Clam.I_channels = 1     
b4Clam.Q_channels = 1     
b4Clam.Z_channels = 1     
b4Clam.C_channels = 1     

# Creating registery of WNNs for each layer
b4Clam.I = np.arange(b4Clam.I_channels, dtype='O')
b4Clam.Q = np.copy(b4Clam.I)     # Q is by default a mirror copy of I
b4Clam.Z = np.arange(b4Clam.Z_channels, dtype='O')
b4Clam.C = np.arange(b4Clam.C_channels, dtype='O')

# Populating the registries with unique identifiers for the WNNs

## number of neurons
b4Clam.i = (4,)     # to match MNIST (28x28 pixels), black and white
b4Clam.q = (4,)     # Q mirrors I
b4Clam.z = (1,)         # 4 are used since 4 binary digits are necesary to encode 0-9 int
b4Clam.c = (5,)         # 1 control neuron to identify training vs. inference states
b4Clam.n_total = sum(b4Clam.i) + sum(b4Clam.q) + sum(b4Clam.z) + sum(b4Clam.c)

# nids of neurons
b4Clam.I[0] = np.arange(4)
b4Clam.Q[0] = np.arange(4, 8)
b4Clam.Z[0] = np.arange(8, 9)
b4Clam.C[0] = np.arange(9, 14)
b4Clam.IQZC = np.arange(b4Clam.n_total)
b4Clam.IQZ = np.arange(b4Clam.n_total - 5)

b4Clam.I__flat = np.concatenate(b4Clam.I, axis=None).ravel() 
b4Clam.Q__flat = np.concatenate(b4Clam.Q, axis=None).ravel() 
b4Clam.Z__flat = np.concatenate(b4Clam.Z, axis=None).ravel() 
b4Clam.C__flat = np.concatenate(b4Clam.C, axis=None).ravel() 
b4Clam.QZ__flat = np.concatenate((b4Clam.Q__flat, b4Clam.Z__flat))



# Defining Neuron metadata
b4Clam.datamatrix = np.zeros([5, b4Clam.n_total], dtype="O")
# 5 rows, as follows:
    #0 Type
    #1 Input Connections; during iconic learning / formation of neuron lookup table (tsets), input connections are taken from the current state
    #2 Neighbor Connections; in constrast to input connections, these take from the past state
    #3 C Connections; neurons connections to C
    #4 Dominant Connection; 1 connection only; a CGA type neuron copies its dominant connection 
    #    ** note; the dominant connection is critical; it is why Q is made in the shape/size of I, so that each Q has a corresponding I as dominant connection (the dominant connection for Z is its own past state [-1]; since if the NSM did something "good / triggered C(s) pleasure neuron(s)" during iconic training, Q will be dominated by I and Z by its past Z (the training becomes; given C at state s, store I(s) and Z(s-1) since Z(s-1) led to the I(s) which triggered C(s)

b4Clam.datamatrix[0, b4Clam.I__flat] = "Input"
b4Clam.datamatrix[0, b4Clam.Q__flat] = "CGA Q"
b4Clam.datamatrix[0, b4Clam.Z__flat] = "CGA Z"
b4Clam.datamatrix[0, b4Clam.C__flat] = "Control"

b4Clam.datamatrix[1, b4Clam.Q[0][0]] = b4Clam.I__flat
b4Clam.datamatrix[1, b4Clam.Q[0][1]] = b4Clam.I__flat
b4Clam.datamatrix[1, b4Clam.Q[0][2]] = b4Clam.I__flat
b4Clam.datamatrix[1, b4Clam.Q[0][3]] = b4Clam.I__flat

b4Clam.datamatrix[1, b4Clam.Z[0][0]] = b4Clam.Q__flat


b4Clam.datamatrix[2, b4Clam.Q[0][0]] = b4Clam.Q__flat
b4Clam.datamatrix[2, b4Clam.Q[0][1]] = b4Clam.Q__flat
b4Clam.datamatrix[2, b4Clam.Q[0][2]] = b4Clam.Q__flat
b4Clam.datamatrix[2, b4Clam.Q[0][3]] = b4Clam.Q__flat

b4Clam.datamatrix[2, b4Clam.Z[0][0]] = b4Clam.Z__flat


b4Clam.datamatrix[3, b4Clam.QZ__flat] = [b4Clam.C__flat]
b4Clam.datamatrix[3, b4Clam.C[0][0]] = b4Clam.QZ__flat
b4Clam.datamatrix[3, b4Clam.C[0][1]] = b4Clam.QZ__flat
b4Clam.datamatrix[3, b4Clam.C[0][2]] = b4Clam.QZ__flat
b4Clam.datamatrix[3, b4Clam.C[0][3]] = b4Clam.QZ__flat
b4Clam.datamatrix[3, b4Clam.C[0][4]] = b4Clam.QZ__flat


b4Clam.datamatrix[4, b4Clam.Q__flat] = b4Clam.I__flat
b4Clam.datamatrix[4, b4Clam.Z__flat] = b4Clam.Z__flat
b4Clam.datamatrix[4, b4Clam.C[0][0]] = "Default if label"
b4Clam.datamatrix[4, b4Clam.C[0][1]] = "C+ pleasure signal"
b4Clam.datamatrix[4, b4Clam.C[0][2]] = "C- pain signal"

b4Clam.C__flat_pleasure= np.array([9, 10, 12])
b4Clam.C__flat_pain= np.array([11, 13])


def c0_instinct_rule(INPUT, Agent):

    # if F == 1, C = 1
    
    if INPUT[0] == 1    and    Agent.story[ Agent.state-1,  Agent.arch.Z__flat] == 1 :
        
        instinct_response = [1, "F/I[0]=1, food!"]
    
    else:
        instinct_response = [0, "pass0"]
    
    return instinct_response
            
b4Clam.datamatrix[4, b4Clam.C[0][3]] = c0_instinct_rule


def c1_instinct_rule_pain(INPUT, Agent):

    # if F == 1, C = 1
    
    if INPUT[-1] == 1    and    Agent.story[ Agent.state-1,  Agent.arch.Z__flat] == 1 :
        
        instinct_response = [1, "OUCH!-CLOSE! (instinctive reflex action)"]
    
    else:
        instinct_response = [0, "pass1"]
    
    return instinct_response
            
b4Clam.datamatrix[4, b4Clam.C[0][4]] = c1_instinct_rule_pain





