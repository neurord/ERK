#in python, type ARGS="Input_filename,find_filename,find_name" then exec(open('path/to/file/Updatemodel_robustness.py')
##DO NOT PUT ANY SPACES NEXT TO THE COMMAS, DO NOT USE TABS
#input_filename is the initial model filename
#find_filename is the specific file name that needed to be replaced (here is the IC)
#suffix_name is the specific tag name find in the replace filename
#file_type is the type of model. e.g: IC or Rxn, or Model

import os
##############################################

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


#args for file to change IC 
input_filename=args[0]#'Model_ERK-d.xml'
find_filename='IC_ERK-Test.xml'#cannot use agrs ????
suffix_name=args[2]#'random'
file_type=args[3]#'IC_ERK'

#set path then fetch all files in path then filter require files
PATH='./'
fileNames=os.listdir(PATH)
for file in fileNames:
    if file_type in file and suffix_name in file:
        replace_filename=file
        with open (input_filename,'r') as input:
            filedata=input.read()
            filedata=filedata.replace(find_filename,replace_filename)
            out_filename=input_filename.split('.')[0]+'-'+replace_filename.split('-')[-1]
        with open (out_filename,'w') as out:
            out.write(filedata)
        
  

   


