import numpy as np
import glob

fileNames=glob.glob('./'+'Model'+'*'+'analysis-d'+'*')

norm_list=[]
cdata='Model_ERK-analysis-crtl.txt'
with open (cdata,'r') as crtl:
    #print(crtl)
    for y in crtl.readlines()[1:]:
        crtl_data=y.strip() 
        #print(crtl_data)


for each in fileNames:
    with open (each,'r') as input:
        for x in input.readlines()[1:]:
            fdata=x.strip()
            norm_auc=[float(fdata.split(' ')[1])/float(crtl_data.split(' ')[1])]
            norm_peak=[float(fdata.split(' ')[2])/float(crtl_data.split(' ')[2])]
            for a in norm_auc:
                for b in norm_peak:
                    norm_list.append((a,b))
                    outfname='analysis-triald.txt'
                    header='parval  ' 
                    header+='auc_norm  '#'           '.join(plot_molecules)+'_'+'auc_norm  '
                    header+='peak_norm'+'\n'#'           '.join(plot_molecules)+'_'+'peak_norm'+'\n'
                    f=open(outfname, 'w')
                    f.write(header)
                    np.savetxt(f,norm_list,fmt='%.4f', delimiter='   ')
                    #np.savetxt(f,np.column_stack((parval,np.round(auc,3),np.round(peakval,3))),fmt='%1s', delimiter='    , ')#changed from .4f to 1s and it worked
                f.close()  
