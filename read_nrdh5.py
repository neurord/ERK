import glob
import os
outfname="analysis"+".bat"
PATH="./"
pattern=PATH+"*.h5"
fileNames=glob.glob(pattern)
for fullname in fileNames:
    fname=os.path.basename(fullname).split('.')[0]
    fileroot=fname.split('-')[0]
    print(fileroot)
    par_change=fname.split('-')[-1]
    #print(par_change)
    f=open(outfname,'w')
    textline='python3 '+"/home/nadia/NeuroRDanal/NeuroRDanal/nrdh5_anal.py "+fileroot+" [inter "+par_change+"]"+" "+"[ppERK]"+"\n"
    #print(textline)
    f.write(textline)
    f.close()
