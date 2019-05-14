import os
import pandas as pd
import matplotlib.pyplot as plt

### Set your path to the folder containing the .csv files
PATH = './'

### Fetch all files in path
fileNames = os.listdir(PATH)

### Filter file name list for files ending with .csv only
fileNames = [file for file in fileNames if '.csv' in file]

###create a figure
fig=plt.figure()

### Loop over all files
for file in fileNames:
    df = pd.read_csv(PATH + file, index_col = 0)### Read .csv file and append to list
    plt.plot(df,label=file)  ### Create line for every file

plt.legend()
plt.show()

