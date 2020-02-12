import glob
import os

PATH="./"
suffix="set"
pattern=PATH+"*.h5"
fileNames=glob.glob(pattern)
outfname="analysis"+".bat"
f=open(outfname, "w")
for fullname in fileNames:
    fname=fullname.split("/")[1]
    textline='python3 '+"/home/nadia/NeuroRDanal//NeuroRDanal/nrdh5_anal.py"+" fullname [inter set] [ppERK]"+"\n"
    f.write(textline)
f.close()
  
#looks like it is working.
#now bette way to write the par
