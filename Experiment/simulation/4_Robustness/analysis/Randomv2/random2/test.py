
import os
import numpy as np
import glob
import csv
#from matplotlib import pyplot as plt

####find ccontrol data first
crtl_raw=[5.286,5.917,6.395,7.489,6.747]##cAMPCa1000
crtl_data=(max (crtl_raw)-min(crtl_raw))/max(crtl_raw)

#trials and param
num_trials=3 #change if more than 3 trials 
ITIs=[3,20,40,80,300]


fil='cAMPCaC1000_random.txt'
results={}
with open (fil,'r') as infile:
    alldata=infile.readlines()
    for line in alldata[1:]:
        items=line.split()
        frange=items[1]
        tmp=items[2:]
        trialdata=np.array(tmp).reshape(len(ITIs),num_trials).T
        results[frange]={trialnum:trialdata[trialnum] for trialnum in range(len(trialdata))}
