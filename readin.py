import numpy as np
import glob
import os

#def readin():
file_dir='/run/media/nadia/NADIA_BLUE/Paper#2/LTP/ltp/'
fileNames=glob.glob(file_dir+'Model'+'*'+'analysis'+'-LTPGbgC100CaC500inter.txt')

norm_list=[]
crtlfile_dir='/run/media/nadia/NADIA_BLUE/Paper#2/LTP/ltp/'
cdata='Model_ERK-analysis-LTPGbgC100CaC500inter.txt'
 


with open (crtlfile_dir+cdata,'r') as crtl:
    crtl_data=[]
    for y in crtl.readlines()[1:]:
        crtl_data.append(y.strip())
        #print(crtl_data)

            
for each in fileNames:
    with open (each,'r') as input:
        norm_temp=os.path.basename(each).split('.')[0].split('-')[-1]+' '
        parval=[]
        headers=input.readline().split()
        auc_index=[i for i,j in enumerate (headers) if j.endswith('auc')]
        peak_index=[i for i,j in enumerate (headers) if j.endswith('peak')]
        for ln,x in enumerate(input.readlines()[1:]):
            #print(ln)
            fdata=x.strip()
            #print(fdata)
            if fdata[0]==crtl_data[ln][0]:
                print(fdata[0],crtl_data[0])
                norm_auc=float(fdata.split()[auc_index[0]])/float(crtl_data[ln].split()[auc_index[0]])
                # print(norm_auc)
                norm_peak=float(fdata.split()[peak_index[0]])/float(crtl_data[ln].split()[peak_index[0]])
                print(crtl_data[ln],fdata)#,norm_auc,norm_peak)
                norm_temp+='  '.join([str(norm_auc),str(norm_peak)])+' '
            else:
                print('**********************************',each,fdata)
            parval.append(fdata.split()[0])
        norm_list.append(norm_temp)
    outfname='analysis-triald.txt'
    header='mol_change '
for par in parval:
    header+=' norm_auc'+par+' peak_norm'+par
    f=open(outfname, 'w')
    f.write(header+'\n')
    np.savetxt(f,norm_list,fmt='%s', delimiter='   ')
    f.close()  
    #if readin==1:
        #readin()
