# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 21:01:09 2023

@author: alebr
"""





## AO Labs Modules
import ao_core as ao

# 3rd Party Modules
import numpy as np



arch_note = "Netbox device type relational autocomplete (10 binary digits per field to encode ids)"
arch = ao.Arch(arch_note)

## Topology
    # Number and shape of neurons

# Channels of data
arch.I_channels = 3     # there is only 1 input type in MNIST if taken as B&W
arch.Q_channels = 3     # by default, Q is a mirror copy of I
arch.Z_channels = 1     # classes of outputs; again only 1 type for MNIST
arch.C_channels = 1     # classes of outputs; again only 1 type for MNIST

# Creating registery of WNNs for each layer
arch.I = np.arange(arch.I_channels, dtype='O')
arch.Q = np.copy(arch.I)     # Q is by default a mirror copy of I
arch.Z = np.arange(arch.Z_channels, dtype='O')
arch.C = np.arange(arch.C_channels, dtype='O')     # classes of outputs; again only 1 type for MNIST

# Populating the registrys with unique identifiers for the WNNs
arch.i = (10,   10,   10)    
arch.q = (10,   10,   10)     # Q mirrors I
arch.z = (10,)         # 4 are used since 4 binary digits are necesary to encode 0-9 int
arch.c = (4,)         # 1 control neuron to identify training vs. inference states
arch.n_total = sum(arch.i) + sum(arch.q) + sum(arch.z) + sum(arch.c)
arch.IQZC = np.arange(arch.n_total)
arch.IQZ = np.arange(arch.n_total - 4)


arch.I[0] = list(range(arch.i[0]))
arch.I[1] = list(range(arch.i[0], arch.i[0]+arch.i[1]))
arch.I[2] = list(range(arch.i[0]+arch.i[1], arch.i[0]+arch.i[1]+arch.i[2]))
arch.ie = sum(arch.i)

arch.Q[0] = list(range(arch.ie, arch.ie+arch.q[0]))
arch.Q[1] = list(range(arch.ie+arch.q[0], arch.ie+arch.q[0]+arch.q[1]))
arch.Q[2] = list(range(arch.ie+arch.q[0]+arch.q[1], arch.ie+arch.q[0]+arch.q[1]+arch.q[2]))
arch.qe = sum(arch.i) + sum(arch.q)

arch.Z[0] = list(range(arch.qe, arch.qe+arch.z[0]))
arch.ze = sum(arch.i) + sum(arch.q) + sum(arch.z)

arch.C[0] = list(range(arch.ze, arch.ze+arch.c[0]))
# arch.C[1] = list(range(arch.ze+arch.c[0], arch.ze+arch.c[0]+arch.c[1]))

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
arch.datamatrix[0, arch.I__flat] = "Input"
arch.datamatrix[0, arch.Q__flat] = "CGA Q"
arch.datamatrix[0, arch.Z__flat] = "CGA Z"
arch.datamatrix[0, arch.C__flat] = "Control"

# arch.datamatrix[1, arch.Q[0]] = arch.I[0]
# arch.datamatrix[1, arch.Q[1]] = arch.I[1]
# arch.datamatrix[1, arch.Q[2]] = arch.I[2]

# arch.datamatrix[2, arch.Q[0]] = arch.Q[0]
# arch.datamatrix[2, arch.Q[1]] = arch.Q[1]
# arch.datamatrix[2, arch.Q[2]] = arch.Q[2]

arch.C__flat_command= np.array([70, 71, 72, 73])
arch.C__flat_pleasure= np.array([70, 71, 72, 73])
arch.C__flat_pain= np.array([73])

def rand_conn(i_conn, q_conn):
            
    for q in arch.Q__flat:
        arch.datamatrix[1, q] = sorted(np.random.randint(0, sum(arch.i), i_conn))
        arch.datamatrix[2, q] = sorted(np.random.randint(sum(arch.i), sum(arch.i) + sum(arch.q), q_conn))
        arch.datamatrix[3, q] = sorted(arch.C__flat)
        arch.datamatrix[4, q] = q - sum(arch.q)
    
    for z in arch.Z__flat:
        arch.datamatrix[1, z] = sorted(arch.Q__flat)
        arch.datamatrix[2, z] = sorted(arch.Z__flat)
        arch.datamatrix[3, z] = sorted(arch.C__flat)
        arch.datamatrix[4, z] = z
        
    for c in arch.C__flat:
        arch.datamatrix[3, c] = sorted(arch.Q__flat) + sorted(arch.Z__flat)
        
    arch.datamatrix_type = 'rand_conn, i_conn: '+str(i_conn)+'  q_conn: '+str(q_conn)
      
arch.rand_conn = rand_conn


def full_conn():
    Qin = 0            
    for Q in arch.Q:
        for q in arch.Q[Qin]:
            arch.datamatrix[1, q] = sorted(arch.I__flat)
            arch.datamatrix[2, q] = sorted(Q)
            arch.datamatrix[3, q] = sorted(arch.C__flat)
            arch.datamatrix[4, q] = q - sum(arch.q)
        Qin += 1

    for z in arch.Z__flat:
        arch.datamatrix[1, z] = sorted(arch.Q__flat)
        arch.datamatrix[2, z] = sorted(arch.Z__flat)
        arch.datamatrix[3, z] = sorted(arch.C__flat)
        arch.datamatrix[4, z] = z
        
    for c in arch.C__flat:
        arch.datamatrix[3, c] = sorted(arch.Q__flat) + sorted(arch.Z__flat)
        
    arch.datamatrix_type = 'full_conn'

arch.full_conn = full_conn




















