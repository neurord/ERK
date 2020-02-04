#in python, type ARGS="Input_filename,find_filename,suffix_name" then exec(open('path/to/file/Update_info.py')
##DO NOT PUT ANY SPACES NEXT TO THE COMMAS, DO NOT USE TABS
#input_filename is the initial model filename
#find_filename is the specific file name that needed to be replaced or update initial concentration (here is the IC)
#suffix_name is the specific tag name find in the files


import glob
import os
from lxml import etree
from xml.etree import ElementTree as ET
import os
import numpy as np
##############################################
randon=0 #if change conc randomly
frange=10 #range for random
set_file=1
modelrobust=1 #create model from change conc 
batch=1 #create a bacth file
factor=.9#write desire factor for set change
prog_path_name='/home/Nadia/neurord-3.2.4-all-deps.jar' #change for specific program 
text='java -jar'+' '+prog_path_name+'   '+'-t 36000000'+'   '+'-Dneurord.trials=3'#update for desire textline

mol_change={'ERK':['ERK'], 'MEK':['MEK'],'MKP1':['MKP1'],'PP2A':['PP2A'],'Raf1':['Raf1'],'bRaf':['bRaf']}

##########################################################################################3333
#set up args
try:
    args = ARGS.split(",")
    print("ARGS =", ARGS, "commandline=", args)
    do_exit = False
except NameError: #NameError refers to an undefined variable (in this case ARGS)
    args = sys.argv[1:]
    print("commandline =", args)
    do_exit = True

try:
    data.close()
except Exception:
    pass


#args 
input_filename=args[0].split('.')[0]#Model
find_filename=args[1].split('.')[0]#'IC
find_name=os.path.split(find_filename)[-1]
suffix_name=args[2]#'random'
PATH='./'

#################################################################
#change IC file randomly and print

def random_file():
    for i in range(frange):
        outfile=find_name.split('.')[0]+'-'+'random'+str(i)+'.xml'
        root=ET.parse(find_filename+'.xml').getroot()
        for elem in root:
            for subelem in elem:
                oldval=float(subelem.attrib['value'])
                newval=str(np.random.uniform(.9,1.1)*oldval) #np.random(low, high)
                subelem.attrib['value']=newval     
                with open(outfile, 'wb') as out:
                    out.write(ET.tostring(root))
if randon==1:
    random_file()


#################################################################
#change IC file and print
def set_file():  
    root=ET.parse(find_filename+'.xml').getroot()
    for mol in mol_change.keys():
        for molecules in mol_change[mol]: 
                for elem in root:
                    for subelem in elem:
                         if molecules== subelem.attrib['specieID']:
                             oldval=float(subelem.attrib['value'])
                             newval=str(oldval*1.1)
                             subelem.attrib['value']=newval
                             outfile=find_name.split('.')[0]+'-'+'set-'+subelem.attrib['specieID']+str(factor)+'.xml'
                             with open(outfile, 'wb') as out:
                                out.write(ET.tostring(root))
                                subelem.attrib['value']=str(oldval)
#if set_file==1:
set_file()
                        
#################################################################
#create model file with replace one line
pattern_model=PATH+'IC'+'*'+suffix_name+'*.xml'
fileNames=glob.glob(pattern_model)

def modelrobust_file(fileNames):
    for replace_filename in fileNames:
        with open (input_filename+'.xml','r') as input:
            filedata=input.read()
            filedata=filedata.replace(find_filename+'.xml',replace_filename)
            out_filename=input_filename+'-'+replace_filename.split('-')[-1]
        with open (out_filename,'w') as out:
            out.write(filedata)
        
if modelrobust==1:
    modelrobust_file(fileNames)



#################################################################3
#create batch file
pattern_batch=PATH+'Model'+'*'+suffix_name+'*.xml'
fileNames=glob.glob(pattern_batch)


def bat_file():
    outfname=suffix_name+'.bat'
    f=open(outfname,'w')
    for files in fileNames:
        #print(files)
        textline=text+'   '+files.split('/')[-1]+'\n'
        f.write(textline)
    f.close()
   
if batch==1:       
    bat_file()

