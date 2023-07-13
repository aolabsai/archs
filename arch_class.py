# -*- coding: utf-8 -*-
"""
// aolabs.ai software >ao_core/Arch.py (C) 2023 Animo Omnis Corporation. All Rights Reserved.

Open source; temporarily under the MIT liscence as per the README.md in parent repository; final lisence and more info TBD at aolabs.ai/strategy.

Thank you for your curiosity!
"""

## // About :: https://docs.aolabs.ai/docs/arch-config
#
# This class defines the Agent Architecture logic used to configure Agents, comprised of 2 components: 
#    1) how many binary neurons to encode your input-output assocations (required),
#    2) How those neurons are connected (optional, more advanced-- best to start with the default of fully-connected network of neurons and them trim down)
#
# For interactive visual representation of Archs: https://miro.com/app/board/uXjVM_kESvI=/?share_link_id=72701488535
#
# We eagerly welcome contributors who relate to these ideas. :)
#
#
##############################################################################
# Reference Archs for Testing

description = "Basic Clam"
arch_i = [1, 1, 1]     # corresponding to Food, Chemical-A, Chemical-B (present=1/not=0)
arch_z = [1]           # corresponding to Open=1/Close=0
arch_c = []            # 4 c neurons are included in the default first channel-- 0-label, 1-force_positive, 2-force_negative, 3-default pleasure instinct triggered when I__flat[0]=1 and Z of previous step Z__flat[0]=1
connector_function = "full_conn"


# description = "Netbox device type relational autocomplete (10 binary digits per field to encode ids)"
# arch_i = [10, 10, 10]
# arch_z = [10]
# arch_c = []
# connector_function = "forward_full_conn"


##############################################################################
# Arch Class

# 3rd Party Modules
import numpy as np
import random as rn


class Arch(object):
    """Arch constructor class."""
    def __init__(self, arch_i, arch_z, arch_c=[], connector_function="full_conn",  connector_parameters=(), description=""):
        super(Arch, self).__init__()
        self.i = arch_i
        self.q = self.i.copy()
        self.z = arch_z
        self.c = [4]+arch_c
        self.connector_function = connector_function
        self.connector_parameters = connector_parameters
        self.description = description

        # Neuron Sets
        self.sets = [self.i, self.q, self.z, self.c]
        self.sets_labels = ["I", "Q", "Z", "C"]
        # I - Input neurons: 0 or 1 depending on fixed ENV decoding
        # Q - State or interneurons: 0 or 1 depending on learned lookup tabled comproised of connected neurons
        # Z - Output neurons: also learning binary neurons like Q, except Z actuates Agent in enviroment
        # C - Control neurons: 0 or 1 depending on designer defined trigger or method like instincts to activate learning; a defined condition on input which triggers the C neuron

        # Creating nids in Channels in Sets
        si = 0     # sets, i.e. category of neurons corresponding to major type, i.g. I or Z or C
        neuron_counter = 0
        for s in self.sets:
            
            Set_label = self.sets_labels[si]
            Set = self.sets[si].copy()
            
            self.__setattr__(Set_label, Set)
            self.__setattr__(Set_label+"__flat", [])
            
            ci = 0     # channel, i.e. subset of neuron set corresponding to application data channels, e.g. there are 3 Inputs in the Basic Clam: F, A, B
            for c in self.__dict__[Set_label]:
                self.__dict__[Set_label][ci] = list(range(neuron_counter, neuron_counter+c))
                self.__dict__[Set_label+"__flat"] += self.__dict__[Set_label][ci]
                neuron_counter += c
                ci += 1
            self.__dict__[Set_label+"__flat"] = np.array(self.__dict__[Set_label+"__flat"])
            si += 1
    
        self.n_total = sum(self.i + self.q + self.z + self.c)

        self.IQZC = np.concatenate((self.I__flat, self.Q__flat, self.Z__flat, self.C__flat))
        self.IQZ  = np.concatenate((self.I__flat, self.Q__flat, self.Z__flat))
        self.QZ__flat = np.concatenate((self.Q__flat, self.Z__flat))        # remove flat from ao_core later for consistency
        
        self.C__flat_command = np.array(self.C[0])     # the first C channel always contains the command neurons which are default to each Agent
        self.C__flat_pleasure= np.array([self.C[0][0], self.C[0][1], self.C[0][3]])
        self.C__flat_pain    = np.array([self.C[0][2]])
        
        # Defining Neuron metadata -- the connections of neurons (i.e. which neurons consititue each others' lookup tables)
        self.datamatrix = np.zeros([5, self.n_total], dtype="O")
        # 5 rows, as follows:
            #0 Type
            #1 Input Connections
            #2 Neighbor Connections
            #3 C Connections
            #4 Dominant Connection
            #    ** note; the dominant connection is critical; it is why Q is made in the shape/size of I, so that each Q has a corresponding I as dominant connection (the dominant connection for Z is its own past state [-1]; since if the NSM did something "good / triggered C(s) pleasure neuron(s)" during iconic training, Q will be dominated by I and Z by its past Z (the training becomes; given C at state s, store I(s) and Z(s-1) since Z(s-1) led to the I(s) which triggered C(s)
        
        self.datamatrix[0, self.I__flat] = "Input"
        self.datamatrix[0, self.Q__flat] = "CGA Q"
        self.datamatrix[0, self.Z__flat] = "CGA Z"
        self.datamatrix[0, self.C__flat] = "Control"

        ## Defining C control propertires
        self.datamatrix[4, self.C[0][0]] = "Default if label"
        self.datamatrix[4, self.C[0][1]] = "C+ pleasure signal"
        self.datamatrix[4, self.C[0][2]] = "C- pain signal"
        #self.datamatrix[4, self.C[0][3]] the default instinct control neuron
        def c0_instinct_rule(INPUT, Agent):
            if INPUT[0] == 1    and    Agent.story[ Agent.state-1,  Agent.self.Z__flat[0]] == 1 :        # self.Z__flat[0] needs to be adjusted as per the agent, which output the designer wants the agent to repeat while learning postively or negatively
                instinct_response = [1, "c0 instinct triggered"]    
            else:
                instinct_response = [0, "c0 pass"]    
            return instinct_response            
        self.datamatrix[4, self.C[0][3]] = c0_instinct_rule        



    ## Connector functions follow
    
        if self.connector_function=="full_conn":
            """Fully connect the neurons-- Q to all I and Q; Z to all Q and Z"""
        
        #    for Channel in self.I:   # I has no incoming connections; input is supplied ex machina (by the env)
        
            for Channel in self.Q:
                for n in Channel:
                    self.datamatrix[1, n] = sorted(self.I__flat)
                    self.datamatrix[2, n] = sorted(self.Q__flat)
                    self.datamatrix[3, n] = sorted(self.C__flat)
                    self.datamatrix[4, n] = n - sum(self.q)
                    
            for Channel in self.Z:
                for n in Channel:
                    self.datamatrix[1, n] = sorted(self.Q__flat)
                    self.datamatrix[2, n] = sorted(self.Z__flat)
                    self.datamatrix[3, n] = sorted(self.C__flat)
                    self.datamatrix[4, n] = n
                
            for Channel in self.C:
                for n in Channel:
                    self.datamatrix[3, n] = sorted(self.Q__flat) + sorted(self.Z__flat)
                    
                self.datamatrix_type = 'full_conn'
    
    
        if self.connector_function == "forward_full_conn":    
            """Fully connect the neurons input-wise-- Q channel to *all* I and itsel; Z channel to all Q and itself"""
        
            for Channel in self.Q:
                for n in Channel:
                    self.datamatrix[1, n] = sorted(self.I__flat)
                    self.datamatrix[2, n] = sorted(Channel)
                    self.datamatrix[3, n] = sorted(self.C__flat)
                    self.datamatrix[4, n] = n - sum(self.q)
                    
            for Channel in self.Z:
                for n in Channel:
                    self.datamatrix[1, n] = sorted(self.Q__flat)
                    self.datamatrix[2, n] = sorted(Channel)
                    self.datamatrix[3, n] = sorted(self.C__flat)
                    self.datamatrix[4, n] = n
                
            for Channel in self.C:
                for n in Channel:
                    self.datamatrix[3, n] = sorted(self.Q__flat) + sorted(self.Z__flat)
                    
                self.datamatrix_type = 'forward_full_conn'
    
    
        if self.connector_function == "forward_forward_conn":    
            """fully connect the neurons forward only-- Q channel to *corresponding* I and itself; Z channel to all Q and itself"""
        
            ci = 0
            for Channel in self.Q:
                for n in Channel:
                    self.datamatrix[1, n] = sorted(self.I[ci])
                    self.datamatrix[2, n] = sorted(Channel)
                    self.datamatrix[3, n] = sorted(self.C__flat)
                    self.datamatrix[4, n] = n - sum(self.q)
                ci += 1
            
            for Channel in self.Z:
                for n in Channel:
                    self.datamatrix[1, n] = sorted(self.Q__flat)
                    self.datamatrix[2, n] = sorted(Channel)
                    self.datamatrix[3, n] = sorted(self.C__flat)
                    self.datamatrix[4, n] = n
                
            for Channel in self.C:
                for n in Channel:
                    self.datamatrix[3, n] = sorted(self.Q__flat) + sorted(self.Z__flat)
                    
                self.datamatrix_type = 'forward_forward_conn'
    
    
        if self.connector_function == "rand_conn":
            """Connect neurons randomly (choose how many random connections per neuron set).
        
            Keyword arguments:
            q_in_conn -- int of random I-input connections for Q neurons
            q_ne_conn -- int of random Q-neighbor connections for Q neurons
            z_in_conn -- int of random Q-input connections for Z neurons
            z_ne_conn -- int of random Z-neighbor connections for Z neurons
            """    
            q_in_conn = self.connector_parameters[0]
            q_ne_conn = self.connector_parameters[1]
            z_in_conn = self.connector_parameters[2]
            z_ne_conn = self.connector_parameters[3]
        
            for Channel in self.Q:
                for n in Channel:
                    self.datamatrix[1, n] = sorted(rn.sample(list(self.I__flat), q_in_conn))
                    self.datamatrix[2, n] = sorted(rn.sample(list(self.Q__flat), q_ne_conn))
                    self.datamatrix[3, n] = sorted(self.C__flat)
                    self.datamatrix[4, n] = n - sum(self.q)
                    
            for Channel in self.Z:
                for n in Channel:
                    self.datamatrix[1, n] = sorted(rn.sample(list(self.Q__flat), z_in_conn))
                    self.datamatrix[2, n] = sorted(rn.sample(list(self.Z__flat), z_ne_conn))
                    self.datamatrix[3, n] = sorted(self.C__flat)
                    self.datamatrix[4, n] = n
                
            for Channel in self.C:
                for n in Channel:
                    self.datamatrix[3, n] = sorted(self.Q__flat) + sorted(self.Z__flat)
                    
            self.datamatrix_type = "rand_conn "+str(q_in_conn)+"-"+str(q_ne_conn)+"--"+str(z_in_conn)+"-"+str(z_ne_conn)
            

            
###############################################################################


# arch = Arch(arch_i, arch_z, arch_c, connector_function, description)

# if you added extra C neurons beyond the 4 default, then after creating the arch instance, program the C neuron like below:
    # arch.datamatrix[4, arch.C[1]]= "define a instinct new_function, like ln 92-98"
    # also you may wish to change how the connections of the new C neuron: arch.datamatrix[3, arch.C[1]]= connections of new C channel
