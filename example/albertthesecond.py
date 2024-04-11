'''
This is an exemplary usage of the "drama" script.
 It loops through the files in the current directory and produces a plot of average absolute values.
For testing, you can use the accompanying .xvg input files that its set up to work with. 
'''


from dramaApr5 import * 
deviation = 0
import os
          
katalog = "C:\\Users\\ysrtxn\\Desktop\\barys\\gify\\" 
os.chdir(katalog)
import time

deviations = []

for i in range(2,70):
    start = time.time()
    nameSS = "t_"+ str(i) + ".xvg"
    nameRR = "t_" +str(1)+ ".xvg"   
    #nameRR = "t_1.xvg"
    bins = 3
    devo = drama(nameSS,nameRR,binSize=3,saveDir= "PIcture19",borderline=20,animatedGif=True,plotData=True,tfs=15)
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
    
  
import matplotlib.pyplot as plt       # used to plot the data       
tfs = 20  
lfs = tfs + 2
print(deviationsc[:,1]) 
jadrodewiacji = np.ones(3)/3
runigDevatios = np.convolve(deviationsc[:,1], jadrodewiacji, mode='valid')  
runingX = np.convolve(deviationsc[:,0],jadrodewiacji,mode = 'valid')
plt.scatter(deviationsc[:,0]+25,deviationsc[:,1],s=5,c="black")
plt.plot(runingX+25,runigDevatios,color="black")
#plt.gca().set_aspect(420)
plt.xticks(fontsize = tfs)
#plt.xlim(24, 96)
plt.yticks(fontsize = tfs)
plt.xlabel("X axis title", fontsize = lfs)
plt.ylabel("Absolute average", fontsize = lfs)

plt.savefig(katalog+ "absolutPlotR19.jpg") 
plt.cla()
