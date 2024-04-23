'''
This is an exemplary usage of the "drama" script.
It loops through the files in the current directory and produces a plot of the sum of absolute values.
For testing, you can use the accompanying .xvg input files that it's set up to work with. 
'''


from dramaApr22p import drama 
deviation = 0

import os 

direct = os.path.join(os.getcwd(),'example')            # creating path 
print(direct)
os.chdir(direct)
import time

newDirSave = "r1"
deviations = []

for i in range(2,71):                          # loops throuth the files in the "example" directory
    start = time.time()
    nameSS = "t_"+ str(i) + ".xvg"
    nameRR = "t_" +str(1)+ ".xvg"   
    #nameRR = "t_1.xvg"
    bins = 3
    devo = drama(nameSS,nameRR,binSize=3,saveDir= newDirSave,borderline=0.003,animatedGif=False,plotRaw=True,plotData=True,tfs=15)           # this is the usage of the dramam function 
    deviations.append([i,devo])
    end = time.time()
    print("time=" + str(end - start))    

import numpy as np 
deviationsc = np.array(deviations)

print(deviations)

import csv

def saveTsv(tsvfilename,arraytosave):                      # function that  saSes the data as tsv text file
    fileTSV = open(tsvfilename,"w")        
    tsvW =  csv.writer(fileTSV, delimiter='\t')  
    #tsvW.writerows(arraytosave)         
    for linia in arraytosave:    
        tsvW.writerow(linia)            
    fileTSV.close()
    
scaleAxis = 30  
import matplotlib.pyplot as plt       # used to plot the data       
tfs = 18 
lfs = tfs + 2
print(deviationsc[:,1]) 
jadrodewiacji = np.ones(3)/3
runigDevatios = np.convolve(deviationsc[:,1], jadrodewiacji, mode='valid')  
runingX = np.convolve(deviationsc[:,0],jadrodewiacji,mode = 'valid')
plt.scatter(deviationsc[:,0]+scaleAxis,deviationsc[:,1],s=5,c="black")
plt.plot(runingX+scaleAxis,runigDevatios,color="black")
#plt.gca().set_aspect(210)
#plt.xticks([40,60,80,100],fontsize = tfs)
#plt.xlim(29, 101)
#plt.yticks([.24,.32,.40],fontsize = tfs)
plt.xlabel(u'T [\u00B0]', fontsize = lfs)
plt.ylabel("SAD", fontsize = lfs)
#plt.subplots_adjust(left=0.19)

fileDirSave = os.path.join(direct,newDirSave,"SAD_plot.png")

plt.savefig(fileDirSave ,bbox_inches='tight') 
plt.cla()
print("Saved under: " + fileDirSave)
