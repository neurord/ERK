import os
import numpy as np
import glob
import csv
#from matplotlib import pyplot as plt

####find ccontrol data first
crtl_raw=[5.286,5.917,6.395,7.489,6.747]##cAMPCa1000
crtl_data=(max (crtl_raw)-min(crtl_raw))/max(crtl_raw)
crtlMaxMin=max(crtl_raw)-min(crtl_raw)
crtlbest=crtl_raw[4]-crtl_raw[3]
#trials and param
num_trials=3 #change if more than 3 trials 
ITIs=[3,20,40,80,300]


fil='cAMPCaC1000_random.txt'
results={}
with open (fil,'r') as infile:
    alldata=infile.readlines()
    for line in alldata[1:]:
        items=line.split()
        frange=items[0]
        tmp=items[1:]
        trialdata=np.array(tmp).reshape(num_trials,len(ITIs))
        results[frange]={trialnum:trialdata[trialnum] for trialnum in range(len(trialdata))}
        
summary={}#{f: {} for f  in results.keys()}
for random in results.keys():
    summary[random]={}
    worstITI[random]={}
    for trial,rows in results[random].items():
        summary[random][trial]={}
        worstITI[random][trial]={}
        best=np.argmax(rows)
        summary[random][trial]['bestITI']=ITIs[best]
        min_index=np.argmin(rows)
        summary[random][trial]['slope']=(float(rows[best])-float(rows[min_index]))/float(rows[best])
        summary[random][trial]['slope_norm']=((float(rows[best])-float(rows[min_index]))/float(rows[best]))/crtl_data
        summary[random][trial]['deltabest']=((float(rows[4])-float(rows[3])))/crtlbest
        summary[random][trial]['deltaMaxMin']=((float(rows[best])-float(rows[min_index])))/crtlMaxMin
        summary[random][trial]['MinITI']=ITIs[min_index]
        
outfname='RandomAnalysis_data'
np.savez(outfname,summary)

'''
#analysis
import pandas as pd
from matplotlib import pyplot as plt
import math
plt.ion()

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
    sm_mean=df['slope_norm'].mean()
    sm_std=df['slope_norm'].std()
    #sm_mean.to_csv('slope_list.txt')
    #plot data for slope

ncols=3
nrows=math.ceil(len(df.columns)/ncols)
fig,axes=plt.subplots(nrows,ncols)
for r in range(nrows):
    for c in range(ncols):
        sm_mean.plot(y='slope_norm',kind='bar',yerr='std',capsize=2,title=files,ax=axes[r,c])
        plt.ylabel("norm/crtl_slope")
        #plot data for bestITI
        plt.figure()
        best.plot(y='bestITI',kind='bar',title=files,ax=axes[r,c])
        plt.show()
'''
