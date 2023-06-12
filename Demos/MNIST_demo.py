# -*- coding: utf-8 -*-
"""
Please do not share or in any way distributed; in closed beta.

@author: AO Labs (not yet formed, contact Ali Al-Ebrahim)

"""


# AO Labs Modules
import ao_core as ao

# 3rd Party Modules
import numpy as np



#%% # Preparing MNIST data

import Demos.MNIST_files.mnist_and_st as mn

    # mn Module Data ####
     
    # mn.MN_TEST is the 10,000 MNIST test images (28x28 pixels each)
    # mn.MN_TEST_labels are the corresponding labels
    #
    # mn.MN_TRAIN is the 60,000 MNIST training images (28x28 pixels each)
    # mn.MN_TRAIN_labels are the corresponding labels
    #
    # mn.ST_TRAIN has 120 standard fonts (times new roman, calibri, arial, etc., 12 fonts total)
    #    that can be used for training, too.
    # mn.ST_TRAIN_labels are the corresponding labels.
 

# Changing the labels from 0-9 int to binary for our weightless neural state machine

MN_TEST_Z = np.zeros([mn.MN_TEST_labels.size, 4])
for i in np.arange(mn.MN_TEST_labels.size):
    MN_TEST_Z[i] = mn.label_to_binary[mn.MN_TEST_labels[i]]

MN_TRAIN_Z = np.zeros([mn.MN_TRAIN_labels.size, 4])
for i in np.arange(mn.MN_TRAIN_labels.size):
    MN_TRAIN_Z[i] = mn.label_to_binary[mn.MN_TRAIN_labels[i]]

ST_TRAIN_Z = np.zeros([mn.ST_TRAIN_labels.size, 4])     ## transforming ST_labels from int to binary
for i in np.arange(mn.ST_TRAIN_labels.size):
    ST_TRAIN_Z[i] = mn.label_to_binary[mn.ST_TRAIN_labels[i].astype(int)]


# Downsample data (to keep things simple, we're running against B&W MNIST)
def down_sample(image, down=200):
    image[image < down] = 0
    image[image >= down] = 1
    return image



#%% # Constructing an MNIST agent

# Configuring Architecture
from Architectures import basic_MNIST
arch = basic_MNIST.arch



# Create Agent
bMN = ao.Agent( arch, "Basic agent for MNIST" )
bMN.arch.rand_conn(360,180) # Connecting each neuron from Q to 360 random Is
                            # and 180 random Qs 
                            # the Z is fully-connected to Q


#%% # Train Agent on STANDARD data (times new roman, calibri, arial, etc.)

for T in np.arange(0, 120):     # can go up to 120; we have 12 fonts in ST training
    
    INPUT = (mn.ST_TRAIN[ T, :, :]).reshape([784])
    LABEL = ST_TRAIN_Z[ T, :]

    bMN.next_state(INPUT, LABEL, print_result=False)
    bMN.reset_state()
    
    

############### << OR >>  ########   
## (you can train with both ST and MN, or change number of training examples (0,10), 
## just reconfigure the post-processing code at the bottom [the 10s] to view results properly or write your own post-processing)
#%% # Train Agent on MNIST data

for T in np.arange(0, 10):     # MNIST has 60,000 testing sets, we're taking (0,10)
    
    INPUT = down_sample(  mn.MN_TRAIN[ T, :, :] ).reshape(784)
    LABEL = MN_TRAIN_Z[ T, :]

    bMN.next_state(INPUT, LABEL, print_result=False)
    bMN.reset_state()



#%% # Test Agent on MNIST data

Steps = 30     # holding same INPUT for Steps

# pick any index (MNIST has 10,000 testing sets, here we do 60-70)
mn_testfrom = 60
mn_to = 70

for T in np.arange( mn_testfrom, mn_to ):     

    INPUT = (down_sample(mn.MN_TEST[ T, :, :])).reshape([784])
    
    print("#####     COMMENCING TEST # "+str(T)+"     #####")
    
    for h in np.arange(Steps):
    
        bMN.next_state(INPUT, DD=False)
        print("Step # "+str(h))

    bMN.reset_state()
    
    

#%% Post Processing
# 
# to easily view data (built around the Spyder IDE's object
# viewer), and to extract final states/results from
# Agent.story and .metastory
                        
I_viewer = np.copy( bMN.story[ 0:bMN.state, bMN.arch.I__flat] )
I_viewer = np.reshape(I_viewer, [bMN.state, 28,28])


Q_viewer = np.copy( bMN.story[ 0:bMN.state, bMN.arch.Q__flat] )
Q_viewer = np.reshape(Q_viewer, [bMN.state, 28,28])
Qmeta_viewer = np.copy( bMN.metastory[ 0:bMN.state, bMN.arch.Q__flat] )
Qmeta_viewer = np.reshape(Qmeta_viewer, [bMN.state, 28,28])

Z_viewer = np.copy( bMN.story[ 0:bMN.state, bMN.arch.Z__flat] )
Zmeta_viewer = np.copy( bMN.metastory[ 0:bMN.state, bMN.arch.Z__flat] )

Z_labels = np.concatenate( (np.zeros(Z_viewer.shape), Z_viewer), axis=1 )
Z_labels = np.packbits( Z_labels.astype(int) )

# Getting the outputs at the end of the Steps (we don't care about the intermediate steps')
Final_Zs = np.arange(10*2 + Steps+1, (10*2+Steps+1) + (mn_to-mn_testfrom)*(Steps+1), (Steps+1))-1
OUTPUT_Zs = bMN.story[Final_Zs][:, bMN.arch.Z__flat]

OUTPUT_METALABELS = bMN.metastory[Final_Zs][:, bMN.arch.Z__flat]
OUTPUT_LABEL = Z_labels[Final_Zs]

MNIST_LABELS = mn.MN_TEST_labels[ mn_testfrom : mn_to]

ACCURACY = sum( MNIST_LABELS == OUTPUT_LABEL ) / len(OUTPUT_LABEL)


# you should get 10% accuracy (1 right answer)
# check it out at # Q_viewer and Q_metaviewer, states ~300-330
# should look like a Times New Roman 3 if you trained against only 0-10 STandard