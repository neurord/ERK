from lxml import etree
from xml.etree import ElementTree as ET
import os
import numpy as np



input_filename='IC_ERK-Test_basal-BCK'
input_name=os.path.split(input_filename)[-1]
outfile=input_name.split('.')[0]+'-'+'randon'+'.xml'


root=ET.parse(input_filename+'.xml').getroot()
elems=[]
for elem in root:
    for subelem in elem:
        oldval=float(subelem.attrib['value'])
        newval=str(np.random.uniform(.9,1.1)*oldval) #np.randon(low, high)
        subelem.attrib['value']=newval
                
with open(outfile, 'wb') as out:
    out.write(ET.tostring(root))
