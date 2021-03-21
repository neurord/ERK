###ARGS="model,,,stime etime,IC,Rxn"
###excec(open('UpdateIC_basal_spatial.py').read())
from lxml import etree
from xml.etree import ElementTree as ET
import os
import numpy as np
import h5py as h5
from NeuroRDanal import h5utilsV2
from NeuroRDanal.nrd_output import nrdh5_output
from NeuroRDanal.nrd_group import nrdh5_group

submembname='dendsub'
dendname="dend"
spinehead="head"
Species=[]
height=0.5#use the write height (or can try to figure it out from the morph, add code for that)  

#set up args
Rxn_filename=args[5]

try:
    args = ARGS.split(",")
    print("ARGS =", ARGS, "commandline=", args)
    do_exit = False
except NameError: #NameError refers to an undefined variable (in this case ARGS)
    args = sys.argv[1:]
    print("commandline =", args)
    do_exit = True

if len(args[2].split()):
    plot_molecules=args[2].split()
else:
    plot_molecules=None

#load the data 
og=nrdh5_group(args,Species)
for fnum,ftuple in enumerate(og.ftuples):
    data=nrdh5_output(ftuple)
    data.rows_and_columns(plot_molecules,args)
    data.molecule_population()
    #print(data.data['model']['grid'][:])
    if data.maxvols>1:
        data.region_structures(dendname,submembname,spinehead)#,stimspine) #stimspine is optional
        data.average_over_voxels()

#mol concentration for both spine and submem

mole_conc_ic={M:{} for M in data.molecules}
for mol in data.molecules:
    mole_conc_ic[mol]['general']=np.mean(np.mean(data.OverallMean[mol]))
if data.maxvols>1:
    mylist=['region','struct']
    for ii, regions_params in enumerate (mylist):
        for mol in data.molecules:
            for jj,key in enumerate(data.output_labels[regions_params][mol].split()):
                region=key.split('_')[-1]
                mole_conc_ic[mol][region]=np.mean(np.mean(data.means[regions_params][mol][:,-10:,jj],axis=1))
#print(mole_conc_ic)

#read in the xml file

def AllSpecies ():
    all_species =[]
    cytosol_species=root.findall('.//NanoMolarity')
    submembrane_species=root.findall('.//PicoSD')
    for specie_sub in submembrane_species:
        all_species.append(specie_sub.get("specieID"))
    for specie_cyt in cytosol_species:
        all_species.append(specie_cyt.get("specieID"))
    all_species=np.unique(all_species)# no repet mol name 
    return all_species


def DiffSpecies ():
    species_diff=[]
    tree_rxn=ET.parse(Rxn_filename+'.xml')
    root_rxn=tree_rxn.getroot()

    for elem_rxn in root_rxn:
        if elem_rxn.tag== 'Specie':
            if float(elem_rxn.get('kdiff'))>0:
                species_diff.append(elem_rxn.get('id'))
    return species_diff 

##check if all mol are present in the IC files, if important, add it, if not leave it 
missing_list=[]
for a in mole_conc_ic.keys():
    if a not in all_species:
        problems_list.append(a)
        print('**************',missing_list)


#read concentration set
#get initial conditions file
IC_filename=args[4]
#print(IC_filename)
tree=ET.parse(IC_filename+'.xml')
root=tree.getroot()
holder=[]
for elem_ic in root:
    if elem_ic.tag=='ConcentrationSet':
        holder.append(elem_ic.get('region'))
    holder=['general' if v is None else v for v in holder]
    if elem_ic.tag=='SurfaceDensitySet':
            hold=['dendsub']
#replace for spine 
for mol,dataset in mole_conc_ic.items():
    for reg,val in dataset.items():
        if reg in holder:
            elems=tree.findall('.//NanoMolarity[@specieID="'+mol+'"]')
            if len(elems)==1:
                elems[0].attrib['value']=str(val)
                #print('updated elems',reg,elems[0].attrib)
        if reg==submembname :
            elems=tree.findall('.//PicoSD[@specieID="'+mol+'"]')
            if len(elems)==1:
                elems[0].attrib['value']=str(val*height)
                #print('updated elems',reg,elems[0].attrib)
        
            
with open('test.xml', 'wb') as out:
    out.write(ET.tostring(root))            
'''
next: 
clean up not needed code
check if diff are same are general

last:
def, finger cross for that 
'''
 
