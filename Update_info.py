#in python exec(open('path/to/file/Update_info.py')
##DO NOT PUT ANY SPACES NEXT TO THE COMMAS, DO NOT USE TABS
#find_filename is the specific file name that needed to be replaced or update initial concentration (here is the IC), change if needed 
#suffix_name is the specific tag name find in the files, 2 options given here, either random or set
#input_filename is the initial model filename, define as set of file


import glob
import sys
import robustness_function as rf
##############################################
randon=0 #if change conc randomly
frange=10 #range for random
modelrobust=1 #create model from change conc 
factor=1.1#write desire factor for set change
prog_path_name='/home/nadia/neurord-3.2.4-all-deps.jar' #change for specific program 
text='java -jar  '+prog_path_name+'   '+'-Dneurord.trials=3   '+'-t 3600000'#update for desire textline

mol_change={'ERK':['ERK'], 'MEK':['MEK'],'MKP1':['MKP1'],'PP2A':['PP2A'],'Raf':['Raf1'],'bRaf':['bRaf'],'dRaf1Ras':['dRaf1Ras'],'cAMP':['cAMP'],'PDE2':['PDE2'],'PDE4':['PDE4'],'PKA':['PKA'],'PKAc':['PKAc'],'Src':['Src'],'Cbl':['Cbl'],'CRKC3G':['CRKC3G'],'CamCa4':['CamCa4'],'CKpCamCa4':['CKpCamCa4'],'CKpCamCa4SynGap':['CKpCamCa4SynGap'],'PP1':['PP1'],'IP35':['Ip35'],'NgCam':['NgCam'],'Grb2':['Grb2'],'Sos':['Sos'],'Shc':['Shc'],'RasGRF':['RasGRF'],'Epac':['Epac'],'RasGDP':['RasGDP'],'Rap1GDP':['Rap1GDP'],'Ca':['Ca'],'Leak':['Leak'],'pmca':['pmca'],'ncx':['ncx'],'Calbin':['Calbin'],'CB':['CB'],'rasGap':['rasGap'],'rapGap':['rap1Gap'],'SynGap':['SynGap']}

##########################################################################################3333
#set up args
'''
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
'''


############################## change IC file randomly and print or set a specific factor ##########################

################################################################ main   ############################
#path
PATH='./'

#args
find_filename='IC_ERK-Test_basald'#args[0].split('.')[0]#'IC
pattern_mod=PATH+'Model'+'*'+'inter*'+'*.xml'
input_filename=sorted(glob.glob(pattern_mod)) #set of files
replace_filename=[]

if randon==1:
    suffix_name='random'
    rf.random_file(suffix_name,frange,find_filename,mol_change)
else:
    suffix_name='set'
    rf.set_file(suffix_name,find_filename,factor,mol_change)

   
pattern_model=PATH+'IC'+'*'+suffix_name+'*.xml'
fileNames_model=sorted(glob.glob(pattern_model))
rf.modelrobust_file(fileNames_model,replace_filename,input_filename,find_filename)


pattern_batch=PATH+'Model'+'*'+suffix_name+'*.xml'
fileNames_batch=sorted(glob.glob(pattern_batch))
rf.bat_file(text,fileNames_batch,suffix_name)

