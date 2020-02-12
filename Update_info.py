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
randon=1 #if change conc randomly
frange=10 #range for random
modelrobust=1 #create model from change conc 
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



############################## change IC file randomly and print or set a specific factor ##########################
def random_file(frange,find_filename):
    for i in range(frange):
        find_name=os.path.split(find_filename)[-1]
        outfile=find_name.split('.')[0]+'-'+'random'+str(i)+'.xml'
        root=ET.parse(find_filename+'.xml').getroot()
        for mol in mol_change.keys():
            for molecules in mol_change[mol]:  
                for elem in root:
                    for subelem in elem:
                        oldval=float(subelem.attrib['value'])
                        newval=str(np.random.uniform(.9,1.1)*oldval) #np.random(low, high)
                        subelem.attrib['value']=newval     
                        with open(outfile, 'wb') as out:
                            out.write(ET.tostring(root))

def set_file(find_filenames,factor):  
    root=ET.parse(find_filename+'.xml').getroot()
    find_name=os.path.split(find_filename)[-1]
    for mol in mol_change.keys():
        for molecules in mol_change[mol]: 
                for elem in root:
                    for subelem in elem:
                         if molecules== subelem.attrib['specieID']:
                             oldval=float(subelem.attrib['value'])
                             newval=str(oldval*factor)
                             subelem.attrib['value']=newval
                             outfile=find_name.split('.')[0]+'-'+'set'+subelem.attrib['specieID']+str(factor)+'.xml'
                             with open(outfile, 'wb') as out:
                                out.write(ET.tostring(root))
          
############################create model file with replace one line######################################
def modelrobust_file(fileNames_model,replace_filename):
    for replace_filename in fileNames_model:
        with open (input_filename+'.xml','r') as input:
            filedata=input.read()
            filedata=filedata.replace(find_filename+'.xml',replace_filename)
            out_filename=input_filename+'-'+replace_filename.split('-')[-1]
        with open (out_filename,'w') as out:
            out.write(filedata)


##################################### create batch file #############################3
def bat_file(text,fileNames_batch):
    outfname=suffix_name+'.bat'
    f=open(outfname,'w')
    for files in fileNames_batch:
        #print(files)
        textline=text+'   '+files.split('/')[-1]+'\n'
        f.write(textline)
    f.close()
#################################################################

################################################################ main   ############################
#args 
input_filename=args[0].split('.')[0]#Model
find_filename=args[1].split('.')[0]#'IC
suffix_name=args[2]#'random'
PATH='./'

replace_filename=[]
pattern_model=PATH+'IC'+'*'+suffix_name+'*.xml'
fileNames_model=sorted(glob.glob(pattern_model))


if randon==1:
    random_file(frange,find_filename)
else:
    set_file(find_filename,factor)

modelrobust_file(fileNames_model,replace_filename)


pattern_batch=PATH+'Model'+'*'+suffix_name+'*.xml'
fileNames_batch=sorted(glob.glob(pattern_batch))
bat_file(text,fileNames_batch)
