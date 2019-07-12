# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 15:18:01 2017

@author: likai
"""

import os
import numpy as np
import copy
import operator
from itertools import groupby


inputFolder=r'G:\in_situ_measurements_snow\russia_climate\snow'
outputFolder=r'G:\in_situ_measurements_snow\russia_climate\snow_selected'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

fileList=[f for f in os.listdir(inputFolder) if not f.endswith('.txt')]

for f in fileList:
    outputName=f+'.txt'
    filePath=os.path.join(inputFolder,f)
    fid=open(filePath)
    line=fid.readline()
    dataArray=np.empty((0,4))
    index=0
    while line:
#        print ('here')
        line=(line.rstrip()).split(';')
#        print(line)
        if int(line[1])<1982 or int(line[1])>2015:
            line=fid.readline()
#            print ('co#ntinue')
            continue
        line=[float(ele) for ele in line[1:5]]
        dataArray=np.vstack((dataArray,np.array(line)))
#        print (dataArray[index,:])
        index=index+1
#        print(index)
        line=fid.readline()
        

#    dataArray=np.array(sorted(dataArray,key=operator.itemgetter(0,1,2)))
#    unique_years=np.unique(dataArray[:,0])
    cleanArray=np.empty((0,4))
    for y in range(1982,2016):
        subset1=dataArray[dataArray[:,0]==y,:]
        if subset1.shape[0]<365 or (np.sum(subset1[0:90,3]==9999)+np.sum(subset1[300:365,3]==9999))>60:
            continue  
        else:    
            backup=copy.copy(subset1)
            for r in range(subset1.shape[0]):
                if subset1[r,3]==9999:
                    if r>=2 and r<subset1.shape[0]-2:
                        if subset1[r-1,3]!=9999 and subset1[r+1,3]!=9999:
                            backup[r,3]=int((subset1[r-1,3]+subset1[r+1,3])/2.0)
                        else:
                            if subset1[r-1,3]!=9999:
                                backup[r,3]=subset1[r-1,3]
                            elif subset1[r+1,3]!=9999:
                                backup[r,3]=subset1[r+1,3]
                            else:
                                if subset1[r-2,3]!=9999 and subset1[r+2,3]!=9999:
                                    backup[r,3]=int((subset1[r-1,3]+subset1[r+1,3])/2.0)
                                else:
                                    if subset1[r-2,3]!=9999:
                                        backup[r,3]=subset1[r-2,3]
                                    elif subset1[r+2,3]!=9999:
                                        backup[r,3]=subset1[r+2,3] 
                                    else:
                                        backup[r,3]=0
                    elif r==0:
                        if subset1[1,3]!=9999:
                            backup[r,3]=subset1[1,3]
                        elif subset1[2,3]!=9999:
                            backup[r,3]=subset1[2,3]
                        else:
                            backup[r,3]=0
                    elif r==1:
                        if subset1[0,3]!=9999 and subset1[2,3]!=9999:
                            backup[r,3]=int((subset1[0,3]+subset1[2,3])/2.0)
                        else:
                            if subset1[0,3]!=9999:
                                backup[r,3]=subset1[0,3]
                            elif subset1[2,3]!=9999:
                                backup[r,3]=subset1[2,3]
                            else:      
                                backup[r,3]=0
                    elif r==subset1.shape[0]-1:
                        if subset1[subset1.shape[0]-2,3]!=9999:
                            backup[subset1.shape[0]-1,3]=subset1[subset1.shape[0]-2,3]
                        elif subset1[subset1.shape[0]-3,3]!=9999:
                            backup[subset1.shape[0]-1,3]=subset1[subset1.shape[0]-3,3]
                        else:
                            backup[subset1.shape[0]-1,3]=0 
                    else:
                        if subset1[subset1.shape[0]-3,3]!=9999 and subset1[subset1.shape[0]-1,3]!=9999:
                            backup[r,3]=int((subset1[subset1.shape[0]-3,3]+subset1[subset1.shape[0]-1,3])/2.0)
                        else:
                            if subset1[subset1.shape[0]-1,3]!=9999:
                                backup[r,3]=subset1[subset1.shape[0]-1,3]
                            elif subset1[subset1.shape[0]-3,3]!=9999:
                                backup[r,3]=subset1[subset1.shape[0]-3,3]
                            else:      
                                backup[r,3]=0                        
            cleanArray=np.vstack((cleanArray,backup))   
    uniqueYears=np.unique(cleanArray[:,0])
#    cleanArr[:,3]=cleanArr[:,3]*0.1
        # remove the station which often has snowy days less than 10 days
    if np.sum(cleanArray[:,0]>0)<len(uniqueYears)*15:
        continue
    diff=list(uniqueYears[1:len(uniqueYears)]-uniqueYears[0:len(uniqueYears)-1])
    pos, max_len, cum_pos = 0, 0, 0
    
    for k, g in groupby(diff):
        if k == 1:
            pat_size = len(list(g))
            pos, max_len = (pos, max_len) if pat_size < max_len else (cum_pos, pat_size)
            cum_pos += pat_size
        else:
            cum_pos += len(list(g))
    if max_len<20:
        continue
    else:
        seqYears=uniqueYears[pos:pos+max_len+1]
        selectedArr=np.empty((0,4))
        for y in seqYears:
            selectedArr=np.vstack((selectedArr,cleanArray[cleanArray[:,0]==y,:]))  
                  
    
    outputFile=os.path.join(outputFolder,outputName)
    fid2=open(outputFile,'w')

    for r in range(selectedArr.shape[0]):
        lineContent=map(lambda x: str(x),selectedArr[r,:])
        lineContent=[str(x) for x in selectedArr[r,:]] 
        lineContent=','.join(lineContent)
        fid2.write(lineContent+'\n')
    fid2.close()
    print(f+' has been selected and filtered for further use')                  
        

#                