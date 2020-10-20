import os
import numpy as np
import glob
#import csv

save=0
#need this because can't plot together 
plot_slope=0
plot_best=0


####find ccontrol data first
conc=1### need to be change if Ca 1000 is used

if conc==0.5:
    crtl_raw=[1.213,1.557,1.719,1.916,2.512]##cAMPCa500
    f='analysisfactor500'
    pattern='./'+'cAMPCaC500_mol-*'+"*.txt"
else:
    crtl_raw=[5.286,5.917,6.395,7.489,6.747]##cAMPCa1000
    f='analysisfactor1000'
    pattern='./'+'cAMPCaC1000_mol-*'+"*.txt"
crtl_data=(max (crtl_raw)-min(crtl_raw))/max(crtl_raw)

#where and how to find the experiment files from pattern (up)
files_set=glob.glob(pattern)

######calculate experiment/simulation data#############


#trials and param
num_trials=3 #change if more than 3 trials 
ITIs=[3,20,40,80,300]
 #extract data 
results={}
for each in files_set:
    fname=os.path.basename(each).split('.')[0].split('-')[-1]
    results[fname]={}
    #read data and rearange data into correct format
    with open (each,'r') as infile:
        alldata=infile.readlines()
        header=alldata[0].split()
        for line in alldata[1:]:
            items=line.split()
            mol=items[0]
            tmp=items[1:]
            trialdata=np.array(tmp).reshape(len(ITIs),num_trials).T.astype(np.float) #reshap and transpose data based on lengh of ITI and number of trials
            results[fname][mol]={trialnum:trialdata[trialnum] for trialnum in range(len(trialdata))}

 #perform calculation
summary={f: {} for f  in results.keys()}
for files in results.keys():
    for molecules in results[files].keys():
        for trial,rows in results[files][molecules].items():
            summary[files][(molecules,trial)]={}
            best=np.argmax(rows)
            summary[files][(molecules,trial)]['bestITI']=ITIs[best]
            min_index=np.argmin(rows)
            summary[files][(molecules,trial)]['slope']=((float(rows[best])-float(rows[min_index]))/float(rows[best]))
            summary[files][(molecules,trial)]['slope_norm']=(((float(rows[best])-float(rows[min_index]))/float(rows[best]))/crtl_data)
           
np.savez(f,summary)


#to open and read 
#np.load(f)                                            

#analysis
import pandas as pd
from matplotlib import pyplot as plt
plt.ion()

for files,data in summary.items():
    df=pd.DataFrame.from_dict(data,orient='index')
    df.index.set_names(['mol','trial'])
    #count bestITI to assess favored 
    count_best=pd.DataFrame(df.groupby('bestITI').count())
    best=count_best.rename(columns={'slope':'bestITI'}).pop('slope_norm')
    print(files,best)
    #correlation
    #corr_df = df.corr()[['slope_norm','slope','bestITI']].sort_values('bestITI',axis=0)#why do we need that???
    #print(corr_df)
    #get mean and std
    sm_mean=pd.DataFrame(df['slope_norm'].mean(level=0))
    sm_mean['std']=df['slope_norm'].std(level=0)
    #df.plot.bar(y='bestITI',title=files)

    #plot data for slope
    if plot_slope==1:
        sm_mean.plot(y='slope_norm',kind='bar',yerr='std',capsize=2,title=files)
        plt.ylabel("norm/crtl_slope")
    #plot data for bestITI
    if plot_best==1:
        plt.figure()
        best.plot.bar(y='bestITI',title=files)
        #plt.show()
    outfname=files+'.txt'
    outfname2=files+'_best.txt'
    if save==1:
        sm_mean.to_csv(outfname)###it is only saving one file 
        best.to_csv(outfname2)
        
 

