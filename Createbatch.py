import os

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


outfname=args[0]#'test.bat'
f=open(outfname,'w')

Dneurord=args[1]#'Dneurord=3'
time=args[2]#'-t 36000000'

suffix=args[3]#'random'
suffix2=args[4]'Model'



fileNames=os.listdir(PATH)

for file in fileNames:
    if suffix2 in file and suffix in file:
        pattern=file
        textline='java -jar'+' '+prog_path_name+'  '+Dneurord+'  '+time+'   '+pattern+'\n'
        f.write(textline)
f.close()
'''



suffix='random'


pattern=dir+'*.py'
filenames=glob.glob(pattern)




for fullname in filenames:
    fname=fullname.split('/')[1]
    textline='java -jar /home/Nadia/Softwares/neurord-3.2.4-all-deps.jar'+' '+'-t 5000'+' '+fname+'\n'
    f.write(textline)
f.close()

'''

#myBat=open(r'/home/Nadia/ERK/test2.py','w+')
#myBat.write(
###[0:find(fname,suffix)]+
