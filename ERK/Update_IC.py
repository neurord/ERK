from lxml import etree
from xml.etree import ElementTree as ET
import os
import numpy as np
import h5py as h5

def decode(table):
    return np.array([s.decode('utf-8') for s in table])

def get_mol_info(simData,plot_molecules,gridpoints):
    outputsets=list(simData['model']['output'].keys())
    dt=np.zeros((len(plot_molecules)))
    samples=np.zeros((len(plot_molecules)),dtype=int)
    out_location={}
    for imol,molecule in enumerate(plot_molecules):
        temp_dict={}
        tot_voxels=0
        for outset in outputsets[1:]:           #better to go backward from last set, and then go to 0 set if mol not found
        #for each in outputsets[-1::-1] and while tot_voxels>grid_points:
            mol_index=get_mol_index(simData,outset,molecule)
            if mol_index>-1:
                samples[imol]=len(simData['trial0']['output'][outset]['times'])
                dt[imol]=simData['trial0']['output'][outset]['times'][1]/1000 #convert msec to sec
                tot_voxels=tot_voxels+len(simData['model']['output'][outset]['elements'])
                temp_dict[outset]={'mol_index':mol_index,'elements':simData['model']['output'][outset]['elements'][:]}
        if len(temp_dict)>0:
            out_location[molecule]={'samples':samples[imol],'dt':dt[imol],'voxels': tot_voxels,'location': temp_dict}
        else:
            outset=outputsets[0]
            print("************* MOLECULE",molecule, " NOT IN REGULAR OUTPUT SETS !")
            mol_index=get_mol_index(simData,outset,molecule)
            if mol_index>-1:
                samples[imol]=len(simData['trial0']['output'][outset]['times'])
                dt[imol]=simData['trial0']['output'][outset]['times'][1]/1000 #convert msec to sec
                temp_dict[outset]={'mol_index':mol_index,'elements':simData['model']['output'][outset]['elements'][:]}
                out_location[molecule]={'samples':samples[imol],'dt':dt[imol],'voxels': gridpoints,'location': temp_dict}
            else:
                out_location[molecule]=-1
                print("** Even Worse: MOLECULE",molecule, " DOES NOT EXIST !!!!!!!!!!!!!")
    return out_location,dt,samples
         
def get_mol_index(simData,outputset,molecule):
    species = decode(simData['model']['output'][outputset]['species'])
    indices=np.where(species == molecule)[0]
    if len(indices) == 1:
        return indices[0]
    else:
        return -1



#parameters
input_filename='IC_ERK-Test.xml'
h5filename='Model_ERK-Test.h5'

#time args
time_args="0 100"

#automatically name the output file
input_name=os.path.split(input_filename)[-1]
outfile=input_name.split('.')[0]+'_new.xml'

#1 get list of molecules
data=h5.File(h5filename,"r")
molecules=decode(data['model']['species'][:])
maxvols=len(data['model']['grid'])
TotVol=data['model']['grid'][:]['volume'].sum()

#constant needed for calculation
Avogadro=6.02214179e14 #to convert to nanoMoles
mol_per_nM_u3=Avogadro*1e-15 #0.6022 = PUVC


#2 get mean concentration of every molecules in the list
trials=[a for a in data.keys() if 'trial' in a]
arraysize=len(trials)
outputsets=data[trials[0]]['output'].keys()
out_location,dt,rows=get_mol_info(data,molecules,maxvols)

#put data into a dictionary
molec_conc_ic={}
for mol in molecules:
    num_mols=len(molecules)
    outset =list(out_location[mol]['location'].keys())[0]
    imol=out_location[mol]['location'][outset]['mol_index']
    voxel=out_location[mol]['location'][outset]['elements']
    start_time=int(float(time_args.split(" ")[0])//dt[imol])
    end_time=int(float(time_args.split(" ")[1])//dt[imol])
    tempConc=np.zeros((len(trials),out_location[mol]['samples']))
    tempConc=data[trials[0]]['output'][outset]['population'][:,voxel,imol]/TotVol/mol_per_nM_u3
    molec_conc_ic[mol]=np.round(np.mean(tempConc[start_time:end_time,:]),3)
            

#read in the xml file
tree =ET.parse(input_filename)
root=tree.getroot()
for elem in root:
            if elem.tag=='ConcentrationSet':
                        for subelem in elem:
                                    print('ConcSet',subelem.attrib)  
             
            elif elem.tag=='SurfaceDensitySet':
                        for subelem in elem:
                                    print('SurfaceDens',subelem.attrib)  

#loop over all molecules in conc_IC dictionary and update values
problems_list=[]
for mol,val in molec_conc_ic.items():
            elems=tree.findall('.//NanoMolarity[@specieID="'+mol+'"]')
            if len(elems)==1:
                print(mol,elems[0].attrib,'new value', val)
                elems[0].attrib['value']=str(val)
                print('updated elems',elems[0].attrib)
            else:
                problems_list.append((mol,elems))
if len(problems_list):
    print('*******************zero or more than 1 species found')
    for item in problems_list:
        print(item)
    


#write the new xml file
with open(outfile, 'wb') as out:
            out.write(ET.tostring(root))

    
#molecules=['Sos','Grb2','Grb2Sos','PP1','RasGRF','Raf1','bRafPKAc','RasGTP', 'RasGDP','RasGTPGap','RasGTPpGap','CKpPP1','SynGap','pSynGap','Rap1GTP', 'Rap1GDP','CK','CKp','CamCa4','Rap1GTPpGap','SrcGbgShc','Shc','Gbg','SrcGbg' ]

