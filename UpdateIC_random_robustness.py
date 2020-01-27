
#in python, type ARGS="IC_file name,range_start,range_stop" then exec(open('path/to/file/UpdateIC_robustness.py')
##DO NOT PUT ANY SPACES NEXT TO THE COMMAS, DO NOT USE TABS
#IC_file name is the exact name of the Initial condition file that you wish to update whithout '.xml'
#range_start is the range starting number
#range_stop is the range stopping number

from lxml import etree
from xml.etree import ElementTree as ET
import os
import numpy as np

#################################################################################
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

#define params file and range 
input_filename=args[0].split('.')[0]
input_name=os.path.split(input_filename)[-1]
range_start=int(args[1])
range_stop=int(args[2])


for i in range(range_start,range_stop):
    outfile=input_name.split('.')[0]+'-'+'random'+str(i)+'.xml'
    root=ET.parse(input_filename+'.xml').getroot()
    for elem in root:
        for subelem in elem:
            oldval=float(subelem.attrib['value'])
            newval=str(np.random.uniform(.9,1.1)*oldval) #np.random(low, high)
            subelem.attrib['value']=newval     
    with open(outfile, 'wb') as out:
        out.write(ET.tostring(root))
