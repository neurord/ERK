from lxml import etree
from xml.etree import ElementTree as ET
import os
import numpy as np



input_filename='IC_ERK-Test_basal-BCK'
input_name=os.path.split(input_filename)[-1]
factor=1.1


root=ET.parse(input_filename+'.xml').getroot()
elems=[]
for elem in root:
    for subelem in elem:
        oldval=float(subelem.attrib['value'])
        newval=str(oldval*1.1)
        subelem.attrib['value']=newval
        outfile=input_name.split('.')[0]+'-'+subelem.attrib['specieID']+'-'+str(factor)+'.xml'
        with open(outfile, 'wb') as out:
            out.write(ET.tostring(root))
        subelem.attrib['value']=str(oldval)








