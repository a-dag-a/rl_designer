# Goal: To optimize a common source amplifier
import re

def loadTemplateNetList(file_path):
    print(f'---> {file_path}')
    with open(file_path,'r') as handle:
        template_netlist = handle.read()#.replace('\n','')
    run_description = template_netlist.split('\n')[0] # inefficient just to get the first line but works for now

    # pattern for finding tokens starting with 'param__'
    pattern = re.compile(r'param__\w+')
    param_tokens = re.findall(pattern, template_netlist)
    paramList = [s.replace('param__','') for s in list(set(param_tokens))] # FIXME: can optimize

    return run_description,template_netlist,paramList

# netlistPath = 'netlists\\template__CS_Amp.cir' # Windows
# netlistPath = 'netlists/template__CS_Amp.cir'

# Test with simpler netlist first
netlistPath = 'netlists/template__RC_LPF_N3.cir'

run_description,template_netlist,paramList = loadTemplateNetList(netlistPath)

# FIXME: Find a better way to do this
netlist_simulation = """
.control
ac dec 100 1 1000Meg
wrdata results/out.dat v(out)
.endc
.end
"""

template_netlist = template_netlist.replace('.end',netlist_simulation)
trial_values = {
'R1':1e3,
'C1':1e-9,
'R2':10e3,
'C2':1e-12,
'R3':10e3,
'C3':1e-12
}

# FIXME: Consider making a netlist class, with paramList in the attributres
# Load the netlist and plant parameters
def generateNetlist(netlist, paramValues):
    ''' Plants parameters into netlist'''
    for _name in paramValues.keys():
        _searchKey = '{param__' + _name +'}'
        netlist = netlist.replace(_searchKey,str(paramValues[_name]))
    return netlist

# Write out the new netlist to see if it simulates fine
new_netlist = generateNetlist(template_netlist, trial_values)
with open('new_netlist.cir','w') as f:
    f.write(new_netlist)
f.close()


# Simulate the netlist
command_string = f'ngspice -b new_netlist.cir'
import os
os.system(command_string)

# Load data
import numpy as np
import matplotlib.pyplot as plt
data = np.loadtxt('results/out.dat')
f = data[:,0]
V = data[:,1]+1j*data[:,2]
plt.plot(np.log10(f),20*np.log10(abs(V)))
plt.grid()
plt.show()

# Test target
V_ideal = 1/(2*np.pi*10e-3)

def computePenalty(V):
    '''Compute the MSE against the ideal response'''
    # ideal transfer function
    V_ideal = 1/(2*np.pi*10e-3)

    # get mean square error
    mse = np.mean(abs(V_ideal-V)**2)
    return mse







# Can we just use backpropagation to guide the bot?


# Optimizing even a large cascade of two ports 
# is a differentiable cost function, 
# so isnt backpropagation a suitable candidate?