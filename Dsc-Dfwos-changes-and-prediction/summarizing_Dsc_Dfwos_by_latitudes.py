# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import gdal
from gdalconst import *
import os
import numpy as np

inputFolder=r'H:\likai_folder\projects\global_snow_cover_freeze_change\new_processing_12_30_2017\statistical_analysis\mean_82_86_10_14_91_98_clipby_countries'

outputFolder=r'H:\likai_folder\projects\global_snow_cover_freeze_change\new_processing_12_30_2017\zonal_statistics'
fileList=[f for f in os.listdir(inputFolder) if f.endswith('.tif')]

fid=open(os.path.join(outputFolder,'zonal_stats_lats_7_11_2018.txt'),'w')
fid.write('name,20_40,40_50,50_60,60_75,30_75\n')

vals=[(20,40),(40,50),(50,60),(60,75),(30,75)]
for f in fileList:
    ds=gdal.Open(os.path.join(inputFolder,f))
    geotrans=ds.GetGeoTransform()
    originX=geotrans[0]
    pixelWidth=geotrans[1]
    originY=geotrans[3]
    pixelHeight=geotrans[5]
    cols=ds.RasterXSize
    rows=ds.RasterYSize
    meanArr=[f]
    for ind in range(len(vals)):
#        print(vals[ind],vals[ind+1])
        r1=int((vals[ind][0]-originY)/pixelHeight)
        r2=int((vals[ind][1]-originY)/pixelHeight)
        arr=ds.ReadAsArray(0,r2,cols,r1-r2)
        arr=arr[arr>=0]
#        per2=np.percentile(arr,1)
#        per98=np.percentile(arr,99)
#        arr=arr[(arr>=per2) & (arr<=per98)]
        meanArr.append(str(np.mean(arr)))
    ds=None
    fid.write(','.join(meanArr)+'\n')
    print(f)
    
fid.close()
        
        
        
        
    