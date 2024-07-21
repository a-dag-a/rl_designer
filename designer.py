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

netlistPath = 'netlists\\template__CS_Amp.cir'
run_description,template_netlist,paramList = loadTemplateNetList(netlistPath)

# FIXME: Find a better way to do this
netlist_simulation = """
.control
wrdata results\out.dat all
.endc
.end
"""

template_netlist.replace('.end',netlist_simulation)

