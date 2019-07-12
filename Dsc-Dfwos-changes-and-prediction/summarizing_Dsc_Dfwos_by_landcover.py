# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import gdal
from gdalconst import *
import os
import numpy as np

#inputFolder=r'H:\likai_folder\projects\global_snow_cover_freeze_change\new_processing_12_30_2017\statistical_analysis\mean82to14_71_98_clipby_countries'
inputFolder=r'E:\backup2\new_processing_12_30_2017\statistical_analysis\mean_82_84_10_14_82_14_2100'

outputFolder=r'E:\backup2\revision-results'
fileList=[f for f in os.listdir(inputFolder) if f.endswith('.tif')]

global_dem=r'E:\backup2\new_processing_12_30_2017\zonal_statistics\landcover\landcover_countries.tif'

ds=gdal.Open(global_dem)
rows=ds.RasterYSize
cols=ds.RasterXSize
dem_band=ds.GetRasterBand(1)
demNoData=dem_band.GetNoDataValue()
demArr=dem_band.ReadAsArray()
ds=None
dem_band=None

fid=open(os.path.join(outputFolder,'zonal_stats_by_landcover1.11.2018.txt'),'w')
fid.write('name,1,2,3,4\n')

for f in fileList:
    ds=gdal.Open(os.path.join(inputFolder,f))
    bd=ds.GetRasterBand(1)
    bdArr=bd.ReadAsArray(0,0,cols,rows)
    ds=None
    meanArr=[f]
    # <300
    subset=bdArr[(demArr==1)]
    subset=subset[subset>=0]
#    per2=np.percentile(subset,2)
#    per98=np.percentile(subset,98)
#    subset=subset[(subset>=per2) & (subset<=per98)]
    meanArr.append(str(np.mean(subset)))
    # 300-600
    subset=bdArr[(demArr==2)]
    subset=subset[subset>=0]
#    per2=np.percentile(subset,2)
#    per98=np.percentile(subset,98)
#    subset=subset[(subset>=per2) & (subset<=per98)]
    meanArr.append(str(np.mean(subset)))    
    # 600-900
    subset=bdArr[(demArr==3)]
    subset=subset[subset>=0]
#    per2=np.percentile(subset,2)
#    per98=np.percentile(subset,98)
#    subset=subset[(subset>=per2) & (subset<=per98)]
    meanArr.append(str(np.mean(subset)))     
    # >900
    subset=bdArr[(demArr==4)]
    subset=subset[subset>=0]
#    per2=np.percentile(subset,2)
#    per98=np.percentile(subset,98)
#    subset=subset[(subset>=per2) & (subset<=per98)]
    meanArr.append(str(np.mean(subset)))    
    print(meanArr)
#    geotrans=ds.GetGeoTransform()
#    originX=geotrans[0]
#    pixelWidth=geotrans[1]
#    originY=geotrans[3]
#    pixelHeight=geotrans[5]
#    cols=ds.RasterXSize
##    rows=ds.RasterYSize
#    
#    meanArr=[f]
#    for ind in range(len(vals)-1):
#        print(vals[ind],vals[ind+1])
#        r1=int((vals[ind]-originY)/pixelHeight)
#        r2=int((vals[ind+1]-originY)/pixelHeight)
#        arr=ds.ReadAsArray(0,r2,cols,r1-r2)
#        arr=arr[arr>=0]
#        per2=np.percentile(arr,2)
#        per98=np.percentile(arr,98)
#        arr=arr[(arr>=per2) & (arr<=per98)]
#        meanArr.append(str(np.mean(arr)))
#    ds=None
    fid.write(','.join(meanArr)+'\n')
    print(f)
    
fid.close()