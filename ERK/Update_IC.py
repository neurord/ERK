from lxml import etree
from xml.etree import ElementTree as ET
import os
import numpy as np
import h5py as h5
from NeuroRDanal import h5utils


#parameters
input_filename='IC_ERK-Test.xml'
h5filename='Model_ERK-TestInit2.h5'

#time args
time_args="3000 3600"

#automatically name the output file
input_name=os.path.split(input_filename)[-1]
outfile=input_name.split('.')[0]+'_new.xml'

#1 get list of molecules
data=h5.File(h5filename,"r")
molecules=h5utils.decode(data['model']['species'][:])
maxvols=len(data['model']['grid'])
TotVol=data['model']['grid'][:]['volume'].sum()

#constant needed for calculation
Avogadro=6.02214179e14 #to convert to nanoMoles
mol_per_nM_u3=Avogadro*1e-15 #0.6022 = PUVC


#2 get mean concentration of every molecules in the list
trials=[a for a in data.keys() if 'trial' in a]
arraysize=len(trials)
outputsets=data[trials[0]]['output'].keys()
out_location,dt,rows=h5utils.get_mol_info(data,molecules,maxvols)
voxel=0


#put data into a dictionary
molec_conc_ic={}
for mol in molecules:
            num_mols=len(molecules)
            outset =list(out_location[mol]['location'].keys())[0]
            imol=out_location[mol]['location'][outset]['mol_index']
            start_time=int(float(time_args.split(" ")[0])//dt[imol])
            end_time=int(float(time_args.split(" ")[1])//dt[imol])
            tempConc=np.zeros((len(trials),out_location[mol]['samples']))
            tempConc=data[trials[0]]['output'][outset]['population'][:,voxel,imol]/TotVol/mol_per_nM_u3
            molec_conc_ic[mol]=int(np.mean(tempConc[start_time:end_time]))
            

#read in the xml file
tree =ET.parse(input_filename)
root=tree.getroot()
for elem in root:
            if elem.tag=='ConcentrationSet':
                        print ('y')        
            else:
                        print('need to write code for this param')
            for subelem in elem:
                        print(subelem.attrib)  
             

#loop over all molecules in conc_IC dictionary and update values
for mol,val in molec_conc_ic.items():
            elems=tree.findall('.//NanoMolarity[@specieID="'+mol+'"]')[0]
            print(elems.attrib,'new value',val)
            elems.attrib['value']=str(val)
            print('updated elems',elems.attrib)
   
#write the new xml file
with open(outfile, 'wb') as out:
            out.write(ET.tostring(root))

    


