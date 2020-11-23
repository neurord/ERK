import os
import numpy as np
import glob
from lxml import etree
from xml.etree import ElementTree as ET


mol_change={'ERK':'ERK', 'MEK':'MEK','MKP1':'MKP1','PP2A':'PP2A','Raf':'Raf1','bRaf':'bRaf','dRaf1Ras':'dRaf1Ras','cAMP':'cAMP','PDE2':'PDE2','PDE4':'PDE4','PKA':'PKA','PKAc':'PKAc','Src':'Src','Cbl':'Cbl','CRKC3G':'CRKC3G','CamCa4':'CamCa4','CKpCamCa4':'CKpCamCa4','CKpCamCa4SynGap':'CKpCamCa4SynGap','PP1':'PP1','IP35':'Ip35','NgCam':'NgCam','Grb2':'Grb2','Sos':'Sos','Shc':'Shc','RasGRF':'RasGRF','Epac':'Epac','RasGDP':'RasGDP','Rap1GDP':'Rap1GDP','Ca':'Ca','Leak':'Leak','pmca':'pmca','ncx':'ncx','Calbin':'Calbin','CB':'CB','rasGap':'rasGap','rapGap':'rap1Gap','SynGap':'SynGap'}


####find ccontrol data first
crtl_raw=[5.286,5.917,6.395,7.489,6.747]##cAMPCa1000
crtl_data=(max (crtl_raw)-min(crtl_raw))/max(crtl_raw)

#trials and param
num_trials=3 #change if more than 3 trials 
ITIs=[3,20,40,80,300]


fil='cAMPCaC1000_randomold.txt'
#def RandomData_file(infile)
results={}
with open (fil,'r') as infile:
    alldata=infile.readlines()
    for line in alldata[1:]:
        items=line.split()
        frange=items[0]
        tmp=items[1:]
        trialdata=np.array(tmp).reshape(num_trials,len(ITIs))
        results[frange]={trialnum:trialdata[trialnum] for trialnum in range(len(trialdata))}

summary={f: {} for f  in results.keys()}
for random in results.keys():
    for trial,rows in results[random].items():
        summary[random][trial]={}
        best=np.argmax(rows)
        summary[random][trial]['bestITI']=ITIs[best]
        min_index=np.argmin(rows)
        summary[random][trial]['slope']=(float(rows[best])-float(rows[min_index]))/float(rows[best])
        summary[random][trial]['slope_norm']=((float(rows[best])-float(rows[min_index]))/float(rows[best]))/crtl_data

#def RandomMol_file(mol_change, all_list)            
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



#analysis
import pandas as pd
from matplotlib import pyplot as plt
import math
plt.ion()
total={}
'''
for f in all_list.keys():
    for mol,val in all_list[f].items():
        fnew=f.split('-')[-1].split('.')[0]
        total[fnew]={}
        total[fnew]=val
        #total.append((f.split('-')[-1].split('.')[0],mol,val))
'''
df_all=pd.DataFrame.from_dict(all_list,orient='index')


for files, data in summary.items():
    df=pd.DataFrame.from_dict(data,orient='index')
    #count bestITI to assess favored 
    count_best=pd.DataFrame(df.groupby('bestITI').count())
    best=count_best.rename(columns={'slope':'bestITI'}).pop('slope_norm')
   # print(files,best)
    #correlation
    #corr_df = df.corr()[['slope_norm','slope','bestITI']].sort_values('bestITI',axis=0)#why do we need that???
    #print(corr_df)
    #get mean and std
    df_all['sn_mean']=df['slope_norm'].mean()
    df_all['sm_std']=df['slope_norm'].std()
    df_all.to_csv('slope_list.txt')
    #plot data for slope

    

