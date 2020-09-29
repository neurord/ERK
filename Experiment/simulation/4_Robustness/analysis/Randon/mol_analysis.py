mol_change={'ERK':'ERK', 'MEK':'MEK','MKP1':'MKP1','PP2A':'PP2A','Raf':'Raf1','bRaf':'bRaf','dRaf1Ras':'dRaf1Ras','cAMP':'cAMP','PDE2':'PDE2','PDE4':'PDE4','PKA':'PKA','PKAc':'PKAc','Src':'Src','Cbl':'Cbl','CRKC3G':'CRKC3G','CamCa4':'CamCa4','CKpCamCa4':'CKpCamCa4','CKpCamCa4SynGap':'CKpCamCa4SynGap','PP1':'PP1','IP35':'Ip35','NgCam':'NgCam','Grb2':'Grb2','Sos':'Sos','Shc':'Shc','RasGRF':'RasGRF','Epac':'Epac','RasGDP':'RasGDP','Rap1GDP':'Rap1GDP','Ca':'Ca','Leak':'Leak','pmca':'pmca','ncx':'ncx','Calbin':'Calbin','CB':'CB','rasGap':'rasGap','rapGap':'rap1Gap','SynGap':'SynGap'}

import glob
import os
from lxml import etree
from xml.etree import ElementTree as ET
import numpy as np

crtl_list={}
filename='IC_ERK-Test_basald.xml'
root=ET.parse(filename).getroot()
for mol in mol_change.keys():
     for elem in root:
          for subelem in elem:
               if mol==subelem.attrib['specieID']:
                    val=float(subelem.attrib['value'])
          crtl_list[mol]=val

PATH='./'
pattern_IC=PATH+'IC'+'*'+'random*'+'*.xml'
IC_filename=sorted(glob.glob(pattern_IC)) 
all_list={}
#
for file_name in IC_filename:
     root=ET.parse(file_name).getroot()
     f=file_name.split('-')[-1].split('.')[0]
     all_list[f]={}
     for mol in crtl_list.keys():
          for elem in root:
               for subelem in elem:
                    if mol== subelem.attrib['specieID']:
                         change_val=float(subelem.attrib['value'])/crtl_list[mol]
                         all_list[f][mol]=change_val
outfname='RandomAnalysis_mol.npy'
np.save(outfname,all_list)

'''
#to check data
dat=np.load(outfname+'.npz',allow_pickle=True)
dat.keys()
dat['ctrl'].item()  
'''

import pandas as pd
from matplotlib import pyplot as plt
plt.ion()
import math

df=pd.DataFrame.from_dict(all_list,orient='index')
df.to_csv('mol_list.txt')


ncols=6
nrows=math.ceil(len(df.columns)/ncols)

fig,axes=plt.subplots(nrows,ncols)
for i, col in enumerate(df.columns):
     for r in range(nrows):
          for c in range(ncols):
               df[col].plot.bar(ax=axes[r,c],title=col)
               ###plt.title(col)


