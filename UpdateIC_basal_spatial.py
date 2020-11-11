from lxml import etree
from xml.etree import ElementTree as ET
import os
import numpy as np
import h5py as h5
from NeuroRDanal import h5utilsV2
from NeuroRDanal.nrd_output import nrdh5_output
from NeuroRDanal.nrd_group import nrdh5_group

submembname='sub'
dendname="dend"
spinehead="head"
num_region=2
Species=[]

#set up args
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


og=nrdh5_group(args,Species)
for fnum,ftuple in enumerate(og.ftuples):
    data=nrdh5_output(ftuple)
    data.rows_and_columns(plot_molecules,args)
    data.molecule_population()
    #print(data.data['model']['grid'][:])
    if data.maxvols>1:
        data.region_structures(dendname,submembname,spinehead)#,stimspine) #stimspine is optional
        data.average_over_voxels()

#get the region index and region names 
mylist=['region','struct']
reg_name={reg:[] for tt,reg in enumerate(mylist)}#{reg:[] for reg in range (num_region)}
for ii, region_params in enumerate (mylist):
    reg_name[region_params]=[]
    for regions in data.output_labels[region_params].values():
        for reg in regions.split():
            reg_name[region_params].append(reg.split('_')[-1])
            
for k,v in reg_name.items():
    newreg_name=list(np.unique(v))
    print(newreg_name,'**********************')
    
for mol in data.molecules:
    for regions in newreg_name:
        reg_index=[i for i ,word in enumerate(data.output_labels['region'][mol].split()) if regions in word][0]


reg_name=set()#{reg:[] for reg in range (num_region)}
for reg_spine in data.output_labels['region'].values():
    for reg in reg_spine.split():
        reg_name.add(reg.split('_')[-1])
    for mol in data.molecules:
        for regions in reg_name:
            reg_index=[i for i ,word in enumerate(data.output_labels['region'][mol].split()) if regions in word][0]


#def dend_data ():
reg_name=set()
for reg_dend in data.output_labels['struct'].values():
    for reg in reg_dend.split():
        reg_name.add(reg.split('_')[-1])
    for mol in data.molecules:
        for regions in reg_name:
            reg_index=[i for i ,word in enumerate(data.output_labels['struct'][mol].split()) if regions in word][0]
            info=np.mean(data.means['region'][mol][:,-10:,:],axis=1)


#read in the xml file
#get initial conditions file
IC_filename=args[4]
#print(IC_filename)
tree=ET.parse(IC_filename+'.xml')
root=tree.getroot()

species = set()

submembrane_species=root.findall('.//NanoMolarity')
cytosol_species=root.findall('.//PicoSD')
for specie_sb in submembrane_species:
    species.add(specie_sb.get("specieID"))
for specie in cytosol_species:
    species.add(specie.get("specieID"))
#print(species)
'''
