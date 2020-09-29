# change file and crtlfile directories


import numpy as np
import glob
import os

#args
file_data=args[0]#'-LTPGbgC100CaC500inter.txt'
cdata=args[1]#'Model_ERK-analysis-LTPGbgC100CaC500inter.txt'

#directories
file_dir='/home/nadia/ERK/Experiment/simulation/3_Train/LTP_h5_2'
crtlfile_dir='/home/nadia/ERK/Experiment/simulation/4_Robustness/analysis/Randon'


fileNames=glob.glob(file_dir+'Model'+'*'+'analysis'+args[0])
norm_list=[]

with open (crtlfile_dir+cdata,'r') as crtl:
    crtl_data=[]
    for y in crtl.readlines()[1:]:
        crtl_data.append(y.strip())
       
            
for each in fileNames:
    with open (each,'r') as input:
        norm_temp=os.path.basename(each).split('.')[0].split('-')[-1]+' '
        parval=[]
        headers=input.readline().split()
        auc_index=[i for i,j in enumerate (headers) if j.endswith('auc')]
        peak_index=[i for i,j in enumerate (headers) if j.endswith('peak')]
        parval_index=[i for i,j in enumerate (headers) if j.startswith('parval')][-1]
        for ln,x in enumerate(input.readlines()): 
            fdata=x.strip()
            if fdata[0]==crtl_data[ln][0]:
                norm_auc=float(fdata.split()[auc_index[0]])/float(crtl_data[ln].split()[auc_index[0]])
                norm_peak=float(fdata.split()[peak_index[0]])/float(crtl_data[ln].split()[peak_index[0]])
                norm_temp+='  '.join([str(norm_auc),str(norm_peak)])+' '
            else:
                print('**********************************',each,fdata)
            parval.append(fdata.split()[parval_index])
        norm_list.append(norm_temp)
    outfname='analysis-triald.txt'
    header='mol_change '
for par in parval:
    header+=' norm_auc'+par+' peak_norm'+par
    f=open(outfname, 'w')
    f.write(header+'\n')
    np.savetxt(f,norm_list,fmt='%s', delimiter='   ')
    f.close()  
   
