
#in python, type ARGS="IC_file name,factor number" then exec(open('path/to/file/UpdateIC_robustness.py')
##DO NOT PUT ANY SPACES NEXT TO THE COMMAS, DO NOT USE TABS
#IC_file name is the exact name of the Initial condition file that you wish to update whithout '.xml'
#factor is the desire incriment of conc increase 

from lxml import etree
from xml.etree import ElementTree as ET
import os
import numpy as np

#############################################


# list of require molecules change: update list as needed
species={'ERK':['ERK'], 'MEK':['MEK'],'MKP1':['MKP1'],'PP2A':['PP2A'],'Raf1':['Raf1'],'bRaf':['bRaf']}

########################################################################
#set up args
try:
    args = ARGS.split(",")
    print("ARGS =", ARGS, "commandline=", args)
    do_exit = False
except NameError: #NameError refers to an undefined variable (in this case ARGS)
    args = sys.argv[1:]
    print("commandline =", args)
    do_exit = True

try:
    data.close()
except Exception:
    pass

#define params file and factor 
input_filename=args[0].split('.')[0]
input_name=os.path.split(input_filename)[-1]
factor=args[1]


root=ET.parse(input_filename+'.xml').getroot()
for mol in species.keys():
    for molecules in species[mol]: 
            for elem in root:
                for subelem in elem:
                     if molecules== subelem.attrib['specieID']:
                         oldval=float(subelem.attrib['value'])
                         newval=str(oldval*1.1)
                         subelem.attrib['value']=newval
                         outfile=input_name.split('.')[0]+'-'+subelem.attrib['specieID']+'-'+str(factor)+'.xml'
                         with open(outfile, 'wb') as out:
                            out.write(ET.tostring(root))
                        subelem.attrib['value']=str(oldval)                                         
                        



                 
