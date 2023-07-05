
import numpy as np
import random as rn


description = "Basic Clam"
arch_i = [1, 1, 1]     # corresponding to Food, Chemical-A, Chemical-B (present=1/not=0)
arch_z = [1]           # corresponding to Open=1/Close=0
arch_c = []            # 4 c neurons are included in the default first channel-- 0-label, 1-force_positive, 2-force_negative, 3-default pleasure instinct triggered when I__flat[0]=1 and Z of previous step Z__flat[0]=1
connector_function = "full_conn"


# description = "Netbox device type relational autocomplete (10 binary digits per field to encode ids)"
# arch_i = [10, 10, 10]
# arch_z = [10]
# arch_c = []
# connector_function = "full_conn"

##############################################################################

class Arch(object):
    """Arch constructor class."""
    def __init__(self, arch_i, arch_z, arch_c=[], connector_function="full_conn",  description=""):
        super(Arch, self).__init__()
        self.i = arch_i
        self.q = self.i.copy()
        self.z = arch_z
        self.c = [4]+arch_c
        self.connector_function = connector_function
        self.description = description

arch = Arch(arch_i, arch_z, arch_c, connector_function, description)

arch.sets = [arch.i, arch.q, arch.z, arch.c]
arch.sets_labels = ["I", "Q", "Z", "C"]

# I - Input neurons: 0 or 1 depending on fixed ENV decoding
# Q - State or interneurons: 0 or 1 depending on learned lookup tabled comproised of connected neurons
# Z - Output neurons: also learning binary neurons like Q, except Z actuates Agent in enviroment
# C - Control neurons: 0 or 1 depending on designer defined trigger or method like instincts to activate learning; a defined condition on input which triggers the C neuron

si = 0     # sets, i.e. category of neurons corresponding to major type, i.g. I or Z or C
neuron_counter = 0
for s in arch.sets:
    
    Set_label = arch.sets_labels[si]
    Set = arch.sets[si].copy()
    
    arch.__setattr__(Set_label, Set)
    arch.__setattr__(Set_label+"__flat", [])
    
    ci = 0     # channel, i.e. subset of neuron set corresponding to application data channels, e.g. there are 3 Inputs in the Basic Clam: F, A, B
    for c in arch.__dict__[Set_label]:
        arch.__dict__[Set_label][ci] = list(range(neuron_counter, neuron_counter+c))
        arch.__dict__[Set_label+"__flat"] += arch.__dict__[Set_label][ci]
        neuron_counter += c
        ci += 1
    arch.__dict__[Set_label+"__flat"] = np.array(arch.__dict__[Set_label+"__flat"])
    si += 1
    
arch.n_total = sum(arch.i + arch.q + arch.z + arch.c)

arch.IQZC = np.concatenate((arch.I__flat, arch.Q__flat, arch.Z__flat, arch.C__flat))
arch.IQZ  = np.concatenate((arch.I__flat, arch.Q__flat, arch.Z__flat))
arch.QZ__flat = np.concatenate((arch.Q__flat, arch.Z__flat))        # remove flat from ao_core later for consistency

arch.C__flat_command = np.array(arch.C[0])     # the first C channel always contains the command neurons which are default to each Agent
arch.C__flat_pleasure= np.array([arch.C[0][0], arch.C[0][1], arch.C[0][3]])
arch.C__flat_pain    = np.array([arch.C[0][2]])

# Defining Neuron metadata -- the connections of neurons (i.e. which neurons consititue each others' lookup tables)
arch.datamatrix = np.zeros([5, arch.n_total], dtype="O")
# 5 rows, as follows:
    #0 Type
    #1 Input Connections
    #2 Neighbor Connections
    #3 C Connections
    #4 Dominant Connection
    #    ** note; the dominant connection is critical; it is why Q is made in the shape/size of I, so that each Q has a corresponding I as dominant connection (the dominant connection for Z is its own past state [-1]; since if the NSM did something "good / triggered C(s) pleasure neuron(s)" during iconic training, Q will be dominated by I and Z by its past Z (the training becomes; given C at state s, store I(s) and Z(s-1) since Z(s-1) led to the I(s) which triggered C(s)

arch.datamatrix[0, arch.I__flat] = "Input"
arch.datamatrix[0, arch.Q__flat] = "CGA Q"
arch.datamatrix[0, arch.Z__flat] = "CGA Z"
arch.datamatrix[0, arch.C__flat] = "Control"


## Connector functions follow

def full_conn():    
    """Fully connect the neurons-- Q to all I and Q; Z to all Q and Z"""

#    for Channel in arch.I:   # I has no incoming connections; input is supplied ex machina (by the env)

    for Channel in arch.Q:
        for n in Channel:
            arch.datamatrix[1, n] = sorted(arch.I__flat)
            arch.datamatrix[2, n] = sorted(arch.Q__flat)
            arch.datamatrix[3, n] = sorted(arch.C__flat)
            arch.datamatrix[4, n] = n - sum(arch.q)
            
    for Channel in arch.Z:
        for n in Channel:
            arch.datamatrix[1, n] = sorted(arch.Q__flat)
            arch.datamatrix[2, n] = sorted(arch.Z__flat)
            arch.datamatrix[3, n] = sorted(arch.C__flat)
            arch.datamatrix[4, n] = n
        
    for Channel in arch.C:
        for n in Channel:
            arch.datamatrix[3, n] = sorted(arch.Q__flat) + sorted(arch.Z__flat)
            
        arch.datamatrix_type = 'full_conn'


def forward_full_conn():    
    """Fully connect the neurons input-wise-- Q channel to *all* I and itsel; Z channel to all Q and itself"""

    for Channel in arch.Q:
        for n in Channel:
            arch.datamatrix[1, n] = sorted(arch.I__flat)
            arch.datamatrix[2, n] = sorted(Channel)
            arch.datamatrix[3, n] = sorted(arch.C__flat)
            arch.datamatrix[4, n] = n - sum(arch.q)
            
    for Channel in arch.Z:
        for n in Channel:
            arch.datamatrix[1, n] = sorted(arch.Q__flat)
            arch.datamatrix[2, n] = sorted(Channel)
            arch.datamatrix[3, n] = sorted(arch.C__flat)
            arch.datamatrix[4, n] = n
        
    for Channel in arch.C:
        for n in Channel:
            arch.datamatrix[3, n] = sorted(arch.Q__flat) + sorted(arch.Z__flat)
            
        arch.datamatrix_type = 'forward_full_conn'


def forward_forward_conn():    
    """fully connect the neurons forward only-- Q channel to *corresponding* I and itself; Z channel to all Q and itself"""

    ci = 0
    for Channel in arch.Q:
        for n in Channel:
            arch.datamatrix[1, n] = sorted(arch.I[ci])
            arch.datamatrix[2, n] = sorted(Channel)
            arch.datamatrix[3, n] = sorted(arch.C__flat)
            arch.datamatrix[4, n] = n - sum(arch.q)
        ci += 1
    
    for Channel in arch.Z:
        for n in Channel:
            arch.datamatrix[1, n] = sorted(arch.Q__flat)
            arch.datamatrix[2, n] = sorted(Channel)
            arch.datamatrix[3, n] = sorted(arch.C__flat)
            arch.datamatrix[4, n] = n
        
    for Channel in arch.C:
        for n in Channel:
            arch.datamatrix[3, n] = sorted(arch.Q__flat) + sorted(arch.Z__flat)
            
        arch.datamatrix_type = 'forward_forward_conn'


def rand_conn(q_in_conn, q_ne_conn, z_in_conn, z_ne_conn):
    """Connect neurons randomly (choose how many random connections per neuron set).

    Keyword arguments:
    q_in_conn -- int of random I-input connections for Q neurons
    q_ne_conn -- int of random Q-neighbor connections for Q neurons
    z_in_conn -- int of random Q-input connections for Z neurons
    z_ne_conn -- int of random Z-neighbor connections for Z neurons
    """    

    for Channel in arch.Q:
        for n in Channel:
            arch.datamatrix[1, n] = sorted(rn.sample(arch.I__flat, q_in_conn))
            arch.datamatrix[2, n] = sorted(rn.sample(arch.Q__flat, q_ne_conn))
            arch.datamatrix[3, n] = sorted(arch.C__flat)
            arch.datamatrix[4, n] = n - sum(arch.q)
            
    for Channel in arch.Z:
        for n in Channel:
            arch.datamatrix[1, n] = sorted(rn.sample(arch.Q__flat, z_in_conn))
            arch.datamatrix[2, n] = sorted(rn.sample(arch.Z__flat, z_ne_conn))
            arch.datamatrix[3, n] = sorted(arch.C__flat)
            arch.datamatrix[4, n] = n
        
    for Channel in arch.C:
        for n in Channel:
            arch.datamatrix[3, n] = sorted(arch.Q__flat) + sorted(arch.Z__flat)
            
    arch.datamatrix_type = "rand_conn "+str(q_in_conn)+"-"+str(q_ne_conn)+"--"+str(z_in_conn)+"-"+str(z_ne_conn)
    
    
## Defining C control propertires
arch.datamatrix[4, arch.C[0][0]] = "Default if label"
arch.datamatrix[4, arch.C[0][1]] = "C+ pleasure signal"
arch.datamatrix[4, arch.C[0][2]] = "C- pain signal"
#arch.datamatrix[4, arch.C[0][3]] the default instinct control neuron
def c0_instinct_rule(INPUT, Agent):
    if INPUT[0] == 1    and    Agent.story[ Agent.state-1,  Agent.arch.Z__flat[0]] == 1 :        # arch.Z__flat[0] needs to be adjusted as per the agent, which output the designer wants the agent to repeat while learning postively or negatively
        instinct_response = [1, "c0 instinct triggered"]    
    else:
        instinct_response = [0, "c0 pass"]    
    return instinct_response            
arch.datamatrix[4, arch.C[0][3]] = c0_instinct_rule