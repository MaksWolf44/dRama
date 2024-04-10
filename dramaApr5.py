import argparse
parser = argparse.ArgumentParser(description='My Parser')
parser.add_argument('fileS',help = 'Input data file containing two columns of angles') 
parser.add_argument('fileR',help = 'Refernce data file containing two columns of angles. Reference data is subtracted from the imput data') 
parser.add_argument('--borderline', type=float, help='Maxumum brighness level for difference plot')
parser.add_argument('--vMax', type=float, help='Maximum brightnrss level for density polts') 
parser.add_argument('--dontSaveAsTif', action=argparse.BooleanOptionalAction, help='Prevents saving 32 bit floating point tiff readeable by Fiji')
parser.add_argument('--dontPlotData', action=argparse.BooleanOptionalAction, help='Prevents saving graphical data plots')
parser.add_argument('--animatedGif',action = argparse.BooleanOptionalAction, help='Saves as amimeted Gif file.  Each run of the script adds one frame to the animation.gif file')
parser.add_argument('--saveDir',default='', help='The directory to witch the results are saved ')
parser.add_argument('--saveName',default='', help='File name for saved autoput')
parser.add_argument('--binSize',type = int,default=2, help='Bin size in degrees')

#args = parser.parse_args()
#print(args)

def  drama(fileSys,fileRef, /, *,binSize = 1,saveDir = '',saveName='',borderline = None,vMax=None,saveAsTif = True, plotData = True, animatedGif=False, mixt=False,tfs=18,plotRaw=False):
    
    import time
    tstart = time.time()
    import os                           #  used to for file manipulation 
    import csv 
    import io
    import numpy as np                                # used for numerical calculations      
                                              
    if saveAsTif:                                   #  used save data to the text file
        import tifffile
        print("savinf tiff")                        #  used to save data as image  
        
    if animatedGif:        
        from PIL import Image as im  
        from PIL import  ImageFilter         
        
    if plotData:
        import matplotlib.pyplot as plt             # used to plot the data       
        import matplotlib.colors 
        print("ploting data")             
   
    if saveName == "":                              # if saveName not provided it saves the date under the name of of the first of the input files.
        saveName =  os.path.splitext( os.path.basename(fileSys) )[0]
    print("Starting file:" + saveName)  
    
    if saveDir == "":                                                  # if  saveDir not specified  creates new directory 
        saveDir =  "results"        
           
    timport = tstart - time.time() 
       
#----------------------------------------------Reading data -----------------------------    
    homeDir = os.getcwd()                    # creates a directory saveDir
    print(homeDir)
    newDir = os.path.join(homeDir,saveDir)               
    print("newDir: " + newDir)
    try: 
        os.mkdir(newDir)
    except :
        print("Directory not created !!!")    
     
    saveDirName = os.path.join( os.getcwd(),saveDir,saveName)                       # 
    print('Saving under:' + saveDirName  )                   # 
    refo = np.loadtxt(fileRef, comments=["#", "@", "^"],usecols=(0,1) )     # reads data from input  file treats  # and * as comments, take only first two columns. 
    syso = np.loadtxt(fileSys, comments=["#", "@", "^"],usecols=(0,1) )     
    
    plikRlen =  refo[:,0].size 
    plikSlen =  syso[:,0].size 
    print("File length: " + str(plikRlen) +"-"+ str(plikSlen) + "=" +str(plikRlen-plikSlen) )   
        
    ksx = syso[:,0]                  #splits input data into x and y column 
    ksy = syso[:,1]
    krx = refo[:,0]
    kry = refo[:,1]    
    
    topen = tstart - time.time()  
    
#------------------------------------------  Plotting raw data ------------------------------------        
    lfs = tfs+2                                # font sizes 
    bfs=lfs
    
    if plotRaw:
        plt.subplots(layout="constrained")           # plots raw data 
        plt.scatter(ksx,ksy,s=1,c="black")         
        plt.gca().set_aspect('equal')
        plt.xlim(-180, 181)
        plt.ylim(-180, 181)        
        plt.xlabel("$\\phi [^{\circ}]$", fontsize = bfs)
        plt.ylabel("$\\psi [^{\circ}]$", fontsize = bfs)
        plt.xticks(range(-180,240,90),fontsize = bfs)
        plt.yticks(range(-180,240,90),fontsize = bfs)
        plt.savefig(saveDirName+ "_sysRam_plot.jpg")     
        plt.scatter(krx,kry,s=1,c="black")       
        plt.savefig(saveDirName + "_refRam_plot.jpg")     
        plt.clf()   
    
#-------------!!!!! Calculating differential Ramachndran - the esence of the script -------------------   
    
                
    binNumber = int(360/binSize)   #  calculates  number of bins. Bin size have to be specified in degrees 
    
    hir = np.histogram2d(kry,krx,binNumber ,range = [[-180, 180], [-180, 180]])    # the core of the program  -  calculates the number of hits in the bin
    his = np.histogram2d(ksy,ksx,binNumber,range = [[-180, 180], [-180, 180]])    
   
    normRefo = sum(sum(hir[0])) /binNumber**2       # calculates number of data points. it is  needed for normalization                 # 
    hirn = np.flip(hir[0],0)/normRefo               # normalization      
    normSyso = sum(sum(his[0])) /(binNumber**2)     # the same for reference data      
    hisn =  np.flip(his[0],0)/normSyso    
    
    diframa = hisn-hirn            # calculates the difference between the system and the reference data 
  
    flatRama = diframa.flatten()
   
    absolut =  np.average( np.abs(flatRama))/2     # 
    trama = tstart - time.time()   
    
    
#------------------------------------Saving results ----------------------------------------------------                   
                                             
     
       
    
    if plotData:
        
        if vMax == None:                                       #    if max level is not specified by the user,  the value of the maximum level in  plots is calculated 
            rMax = np.max(hirn)
            sMax = np.max(hisn)
            vMax = np.max([rMax,sMax])
            
        if borderline == None:                                          # iF min-max level is not specified by the user,  the value of the extreme level in the diff plot is calculated 
            borderline =  np.max( np.abs(diframa))
        
        def plotPars():                                                 #setting plot params
            fig, ax =  plt.subplots(layout = 'constrained' )
            pozycje = [-1/2,(binNumber-1/2)*0.25,(binNumber-1/2)/2,(binNumber-1/2)*0.75,binNumber-1/2]                     # this is needed for the plot scale 
            podpisyx  = [-180,-90,0,90,180]
            podpisyy  = [180,90,0,-90,-180]
            plt.xticks(pozycje, podpisyx,fontsize = tfs)
            plt.yticks(pozycje, podpisyy,fontsize = tfs)
            plt.xlabel("$\\phi [^{\circ}]$", fontsize = lfs)
            plt.ylabel("$\\psi [^{\circ}]$", fontsize = lfs)
            
            
        plotPars()
        plt.imshow(diframa,interpolation='none',vmin=-borderline, vmax=borderline)       
        #orientation='horizontal',location = "bottom")                
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("gray", [(0, 1, 1),(0, 0.8, 1),(0, 0.5, 1),(0, 0.0, 1),(0, 0.0, 0.666),"white",(0.666, 0.0, 0.0),(1, 0.0, 0),(1, 0.5, 0),(1, .8, 0),(1, 1, 0)],N=256)                                   # color map for the difference plot
        cbar = plt.colorbar()
        cbar.ax.tick_params(labelsize=tfs) 
        plt.set_cmap(cmap)       
        plt.savefig(saveDirName+ "_diff_plot.jpg") 
        plt.clf()        
        
        plotPars()          
        cmapb = matplotlib.colors.LinearSegmentedColormap.from_list("gray", ["white",(0.0, 0.0, 0.666),(0.0, 0.0, 1),(0, 0.5, 1),(0, .8, 1),(0, 1, 1)],N=256)                
        plt.imshow(hirn,interpolation='none',vmin=0,vmax=vMax)     
        plt.set_cmap(cmapb)
        cbar = plt.colorbar()
        cbar.ax.tick_params(labelsize=tfs) 
        plt.savefig(saveDirName+ "_ref_plot.jpg") 
        plt.clf()  
        
        plotPars()
        cmapr = matplotlib.colors.LinearSegmentedColormap.from_list("gray", ["white",(0.666, 0.0, 0.0),(1, 0.0, 0),(1, 0.5, 0),(1, .8, 0),(1, 1, 0)],N=256)
        plt.imshow(hisn,interpolation='none',vmin=0,vmax=vMax)                                           
        plt.set_cmap(cmapr)        
        cbar = plt.colorbar()
        cbar.ax.tick_params(labelsize=tfs) 
        plt.savefig(saveDirName + "_sys_plot.jpg") 
        plt.clf()       
        
        if animatedGif:
            plt.plot()
            img_buf = io.BytesIO()
            plt.savefig(img_buf, format='png')    
            imFromPlot = im.open(img_buf)
            plt.clf()
        
       
            
         
    
    def saveTsv(tsvfilename,arraytosave,how):                      # function that  saves the data as tsv text file
        fileTSV = open(tsvfilename,how)        
        tsvW =  csv.writer(fileTSV, delimiter='\t')           
        for linia in arraytosave:    
            tsvW.writerow(linia)            
        fileTSV.close()
    
    print("Scale=" + str(np.max(hisn)))
     
    saveTsv(saveDirName+ "_diff.tsv",diframa,"w")                  # saving as text files        #  
    saveTsv(saveDirName+ "_sys.tsv",hirn,"w") 
    saveTsv(saveDirName+ "_ref.tsv",hisn,"w")  
    
    #if os.path.isfile(saveDirName+"absolute.tsv"):
    how = "a"
    fileA = open(saveDirName+"_absolute.tsv",how)        
    fileA.write(str(absolut)+"\n")
    fileA.close()
        
    
        
    
    
    if  saveAsTif:                                           # saving as 32 bit floating point tiff images
        tifffile.imwrite(saveDirName+ '_diff.tif', diframa,resolution=(binSize, binSize))
        tifffile.imwrite(saveDirName+ '_ref.tif', hirn,resolution=(binSize, binSize))
        tifffile.imwrite(saveDirName+ '_sys.tif', hisn,resolution=(binSize, binSize))
        
    if animatedGif:                                                # saving as animated gif 
        imDif = im.fromarray(diframa)
        #imDif0 = im.fromarray(hisn)
        giffSaveName = os.getcwd()+saveDir+ 'animated.gif'        
        tempName = os.getcwd()+saveDir+ 'animetedTemp.gif'    
        
        imagesToAppend = []                                                  # creates an array that will be appended  to animated gif       
        imagesToAppend.append(imFromPlot)        
                    
        if os.path.isfile(giffSaveName):                            # if animated file exists  
            imageObject = im.open(giffSaveName)                     # the file is opened            
            imageObject.save(tempName, save_all=True, append_images = imagesToAppend[0:] , optimize=False, fps=2, loop=0) # and saved under temporary  name with a new frame  added            
            imageObject.close()
            os.remove(giffSaveName)           # the original gif file is removed 
            os.rename(tempName, giffSaveName) # and the temporary  file is renamed to the giffSaveName     
        
        else:            

            imagesToAppend[0].save(giffSaveName , append_images = imagesToAppend[0:], save_all=True, optimize=False, fps = 2, loop=0)    
            print("animated giff file created")
    
    tplot = tstart - time.time() 
    
    print('times')
    print(timport,topen,trama,tplot)  
        
    print("Absolute average=" +  str(absolut))
    print("finito V.10apr")
    return(absolut)
    
#drama(args.fileS,args.fileR,binSize = args.binSize,saveName = args.saveName,saveDir = args.saveDir,borderline = args.borderline,vMax = args.vMax ,saveAsTif = not args.dontSaveAsTif,plotData = not args.dontPlotData,animatedGif = args.animatedGif )    
import os

katalog = "C:\\Users\\ysrtxn\\Desktop\\barys\\testy"
os.chdir(katalog)
drama("system.xvg","reference.xvg",plotRaw=True)
