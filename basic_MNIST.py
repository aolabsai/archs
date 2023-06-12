# -*- coding: utf-8 -*-


# Importing Modules

## AO Labs Modules
import ao_core as ao

## 3rd Party Modules
import numpy as np





#%%

arch = ao.Arch("Basic MNIST arch, to be used as a base for MNIST v0.1.0")


## Topology
    # Number and shape of neurons

# Channels of data
arch.I_channels = 1     # there is only 1 input type in MNIST if taken as B&W
arch.Q_channels = 1     # by default, Q is a mirror copy of I
arch.Z_channels = 1     # classes of outputs; again only 1 type for MNIST
arch.C_channels = 1     # classes of outputs; again only 1 type for MNIST

# Creating registery of WNNs for each layer
arch.I = np.arange(arch.I_channels, dtype='O')
arch.Q = np.copy(arch.I)     # Q is by default a mirror copy of I
arch.Z = np.arange(arch.Z_channels, dtype='O')
arch.C = np.arange(arch.C_channels, dtype='O')     # classes of outputs; again only 1 type for MNIST

# Populating the registrys with unique identifiers for the WNNs
arch.i = 28*28     # to match MNIST (28x28 pixels), black and white
arch.q = 28*28     # Q mirrors I
arch.z = 4         # 4 are used since 4 binary digits are necesary to encode 0-9 int
arch.c = 3         # 1 control neuron to identify training vs. inference states, Cpos and Cneg there by default
arch.n_total = arch.i + arch.q + arch.z + arch.c

arch.I[0] = np.arange(arch.i)
arch.Q[0] = np.arange(arch.i, arch.i + arch.q)
arch.Z[0] = np.arange(arch.i+arch.q, arch.i+ arch.q + arch.z)
arch.C[0] = np.arange(arch.i+arch.q+arch.z, arch.n_total)
arch.IQZC = np.arange(arch.n_total)
arch.IQZ = np.arange(arch.n_total - arch.c)

arch.I__flat = np.concatenate(arch.I, axis=None).ravel()  # is .ravel even needed?
arch.Q__flat = np.concatenate(arch.Q, axis=None).ravel()
arch.Z__flat = np.concatenate(arch.Z, axis=None).ravel()
arch.C__flat = np.concatenate(arch.C, axis=None).ravel()
arch.QZ__flat = np.concatenate((arch.Q__flat, arch.Z__flat))

# Defining Neuron metadata
arch.datamatrix = np.zeros([5, arch.n_total], dtype="O")
# 5 rows, as follows:
    #0 Type
    #1 Input Connections
    #2 Neighbor Connections
    #3 C Connections
    #4 Dominant Connection

# Only setting types for now (other neuron meta data will be populated by 
    # the function this_module.rand_conn below)
arch.datamatrix[0, arch.I[0]] = "Input"
arch.datamatrix[0, arch.Q[0]] = "CGa Q"
arch.datamatrix[0, arch.Z[0]] = "CGa Z"
arch.datamatrix[0, arch.C[0]] = "Control"

arch.C__flat_command= np.array([arch.n_total-3]) # to grab the labelling neuron
arch.C__flat_pleasure= np.array([arch.n_total-3, arch.n_total-2])
arch.C__flat_pain= np.array([arch.n_total-1])


def rand_conn(i_conn, q_conn):
            
    for q in arch.Q__flat:
        arch.datamatrix[1, q] = sorted(np.random.randint(0, arch.i, i_conn))
        arch.datamatrix[2, q] = sorted(np.random.randint(arch.i, arch.i + arch.q, q_conn))
        arch.datamatrix[3, q] = sorted(arch.C__flat)
        arch.datamatrix[4, q] = q - arch.q
        
    z0 = 0
    for z in arch.Z__flat:
        arch.datamatrix[1, z] = sorted(arch.Q__flat)
        arch.datamatrix[2, z] = sorted(arch.Z__flat)
        arch.datamatrix[3, z] = sorted(arch.C__flat)
        arch.datamatrix[4, z] = 0    # should fix
        z0 += 1
    
    for c in arch.C__flat:
        arch.datamatrix[3, c] = sorted(arch.Q__flat) + sorted(arch.Z__flat)
        
arch.rand_conn = rand_conn


