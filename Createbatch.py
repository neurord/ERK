import os
import glob

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



PATH="./"
prog_path_name='/home/Nadia/Softwares/neurord-3.2.4-all-deps.jar'

text='java -jar'+' '+prog_path_name+'  '+'-Dneurord.trial=3'+'  '+'-t 36000000'
outfname='test.bat'
f=open(outfname,'w')


suffix_name=args[2]#'random' already in randon, in set is called factor

pattern_batch=PATH+'Model'+'*'+suffix_name+'*.xml'

fileNames=glob.glob(pattern_batch)

def bat_file(fileNames,text,file):
    for files in fileNames:
        print(files)
        textline=text+'   '+files.split('/')[-1]+'\n'
        f.write(textline)
    f.close()
        
bat_file(fileNames,text,files)
