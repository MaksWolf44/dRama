'''
This is an exemplary usage of the "drama" script.
It loops through the files in the current directory and produces a plot of som of absolute values.
For testing, you can use the accompanying .xvg input files that its set up to work with. 
'''


from dramaApr19 import drama 
deviation = 0

import os 
katalog = "C:\\Users\\ysrtxn\\Desktop\\barys\\gify\\" 
#katalog = os.getcwd()
os.chdir(katalog)
import time

deviations = []

for i in range(2,71):
    start = time.time()
    nameSS = "t_"+ str(i) + ".xvg"
    nameRR = "t_" +str(1)+ ".xvg"   
    #nameRR = "t_1.xvg"
    bins = 3
    devo = drama(nameSS,nameRR,binSize=3,saveDir= "B2",borderline=0.003,animatedGif=False,plotRaw=False,plotData=False,tfs=15)
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
plt.gca().set_aspect(210)
plt.xticks([40,60,80,100],fontsize = tfs)
plt.xlim(29, 101)
plt.yticks([.24,.32,.40],fontsize = tfs)
plt.xlabel("$T[^o C]$", fontsize = lfs)
plt.ylabel("SAD", fontsize = lfs)
#plt.subplots_adjust(left=0.19)

plt.savefig(katalog+ "SAD_PlotB1.png",bbox_inches='tight') 
plt.cla()