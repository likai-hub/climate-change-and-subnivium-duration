#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      lzhu68
#
# Created:     21/10/2015
# Copyright:   (c) lzhu68 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import gdal
from gdalconst import *
import numpy
import osr
import os

#*************************************************************************************
def array2raster(array,newRasterfn,geotrans,projection):

    cols = array.shape[1]
    rows = array.shape[0]

    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Int16)

    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRaster.SetGeoTransform(geotrans)
##    outRasterSRS = osr.SpatialReference()
##    outRasterSRS.ImportFromEPSG(3410)
    outRaster.SetProjection(projection)
    outband.FlushCache()
#*************************************************************************************
os.chdir('/mnt/stratus/lzhu68/global_snow_soil_freeze_project2/freeze_thaw_dataset')
inputFolder='./filtered_freeze_thaw_record79_16'
outFolder='./frozen_season/season_end_nh'
##inputFolder=r'N:\likai\global_freeze_snow_project\latest_processing\outliers_filtered79_12'
##outFolder=r'N:\likai\global_freeze_snow_project\latest_processing\frozen_season\season_end_nh'
if not os.path.exists(outFolder):
    os.mkdir(outFolder)

driver=gdal.GetDriverByName('GTiff')
# basic information of raster
temp='./filtered_freeze_thaw_record79_16/2011/frz2011001.tif'
template=gdal.Open(temp)
cols=template.RasterXSize
rows=template.RasterYSize
sr=template.GetProjection()
geotransform=template.GetGeoTransform()
template=None

arr=numpy.empty([0,int(rows/2),cols],dtype=int)
for year in range(1982,2017):
    if year%4==0:
        inputSubFolder=os.path.join(inputFolder,str(year))
        idx=0
        for day in range(61,245):
            filePath=os.path.join(inputSubFolder,'frz'+str(year)+str(day).zfill(3)+'.tif')
            inDS=gdal.Open(filePath)
            band=inDS.GetRasterBand(1)
            arr=numpy.concatenate((arr,band.ReadAsArray(0,0,cols,int(rows/2)).reshape(1,int(rows/2),cols)),0)
##            arr[idx]=band.ReadAsArray(0,0,cols,int(rows/2))
            inDS=None
            band=None
            print ('frz'+str(year)+str(day).zfill(3)+'.tif')
            idx=idx+1
        endArr=numpy.ones([rows/2,cols],dtype=int)*(-4)
        for r in range(arr.shape[1]):
            for c in range(arr.shape[2]):
                pixelVals=arr[:,r,c]
                if numpy.all(pixelVals==1):
                    # all days are non-frozen
                    endArr[r,c]=-2
                elif numpy.any(pixelVals==4):
                    endArr[r,c]=-3
                elif numpy.any(pixelVals==99):
                    continue
                else:
                    for i in range(7,arr.shape[0]-7):
                        sub=pixelVals[(i-7):(i+8)]
                        if len(sub[numpy.where((sub==0)|(sub==2)|(sub==3))])<8:
                            endDate=i+61
                            endArr[r,c]=endDate
                            break

                        if i==(arr.shape[0]-8):
                            # all year frozen
                            endArr[r,c]=-1
        array2raster(endArr,os.path.join(outFolder,'end'+str(year-1)+'.tif'),geotransform,sr)
        print('The end of the frozen for year '+str(year-1)+' has been derived')
        arr=numpy.empty([0,int(rows/2),cols],dtype=int)
    else:
        inputSubFolder=os.path.join(inputFolder,str(year))
        idx=0
        for day in range(60,244):
            filePath=os.path.join(inputSubFolder,'frz'+str(year)+str(day).zfill(3)+'.tif')
            inDS=gdal.Open(filePath)
            band=inDS.GetRasterBand(1)
            arr=numpy.concatenate((arr,band.ReadAsArray(0,0,cols,int(rows/2)).reshape(1,int(rows/2),cols)),0)
            inDS=None
            band=None
            print ('frz'+str(year)+str(day).zfill(3)+'.tif')
            idx=idx+1

        endArr=numpy.ones([rows/2,cols],dtype=int)*(-4)
        for r in range(arr.shape[1]):
            for c in range(arr.shape[2]):
                pixelVals=arr[:,r,c]
                if numpy.all(pixelVals==1):
                    # all days are non-frozen
                    endArr[r,c]=-2
                elif numpy.any(pixelVals==4):
                    endArr[r,c]=-3
                elif numpy.any(pixelVals==99):
                    continue
                else:
                    for i in range(7,arr.shape[0]-7):
                        sub=pixelVals[(i-7):(i+8)]
                        if len(sub[numpy.where((sub==0)|(sub==2)|(sub==3))])<8:
                            endDate=i+60
                            endArr[r,c]=endDate
                            break
                        if i==(arr.shape[0]-8):
                            # all year frozen
                            endArr[r,c]=-1
        array2raster(endArr,os.path.join(outFolder,'end'+str(year-1)+'.tif'),geotransform,sr)
        print('The end of the frozen for year '+str(year-1)+' has been derived')
        arr=numpy.empty([0,int(rows/2),cols],dtype=int)

