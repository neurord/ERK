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



################## GET MOL Value Change ##########################3
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

          
#find the files 
PATH='./'
pattern_IC=PATH+'IC'+'*'+'random*'+'*.xml'
IC_filename=sorted(glob.glob(pattern_IC)) 
all_list={}
#now do the math to calculate the change of value
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



###########analysis
import pandas as pd
from matplotlib import pyplot as plt
import math
plt.ion()
import pickle
import csv

df_all=pd.DataFrame.from_dict(all_list,orient='index')

mean=[]
std=[]
for files, data in summary.items():
    df=pd.DataFrame.from_dict(data,orient='index')
    #count bestITI  
    count_best=pd.DataFrame(df.groupby('bestITI').count())
    best=count_best.rename(columns={'slope':'bestITI'}).pop('slope_norm')
    print(files,best)
    #get mean and std
    mean.append(df['slope_norm'].mean())
    std.append(df['slope_norm'].std())
df_all['sn_mean']=mean
df_all['sn_std']=std
#df_all.plot.bar()

##########RandomForest#############

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR

X = df_all.drop(['sn_mean'],axis=1)# can't add bestITI and auc 
Yslope=df_all['sn_mean']# mean of three trials
Yiti=df['bestITI']#nope, gives last results and three trials 

for y,label in zip([Yslope,Yiti],['slope','bestITI']):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    regr = RandomForestRegressor(n_estimators=100)
    regr.fit(X_train, y_train)
    y_pred = regr.predict(X_test)
    #print & plot some results
    print('train',regr.score(X_train,y_train),'test',regr.score(X_test,y_test))
    feature_importance_df = pd.DataFrame(regr.feature_importances_,X.columns,columns=['Random_Forest_Feature_Importance']).sort_values('Random_Forest_Feature_Importance',ascending=False)
    axes = feature_importance_df.plot.barh()
    axes.legend_.set_visible(False)
    f = plt.gcf()
    f.set_size_inches((6,6))
    axes.set_xlim([0,feature_importance_df.max()[0]])
    plt.title('Feature Importance for'+label)
    
######## Substitute important features for nmda_gbar ######  
num_plots=2
mols=[feature_importance_df_all.index[int(feature_importance_df_all.iloc[i])] for i in range(num_plots)]
plt.figure()
for mol in mols:
    plt.scatter(X_test[mol], y_test,alpha=.4)
    plt.scatter(X_test[mol], y_pred,alpha=.4)
    
