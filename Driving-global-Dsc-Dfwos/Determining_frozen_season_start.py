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
outFolder='./frozen_season/season_start_nh'
if not os.path.exists(outFolder):
    os.makedirs(outFolder)
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

for year in range(1982,2016):
    # leap year for current year
    if (year)%4==0:
##        arr=numpy.zeros([181,int(rows/2),cols],dtype=int)
        inputSubFolder=os.path.join(inputFolder,str(year))
        idx=0

        for day in range(245,367):
            filePath=os.path.join(inputSubFolder,'frz'+str(year)+str(day).zfill(3)+'.tif')
            inDS=gdal.Open(filePath)
            band=inDS.GetRasterBand(1)
            arr=numpy.concatenate((arr,band.ReadAsArray(0,0,cols,int(rows/2)).reshape(1,int(rows/2),cols)),0)
            inDS=None
            band=None
            print ('frz'+str(year)+str(day).zfill(3)+'.tif')
            idx=idx+1

        inputSubFolder=os.path.join(inputFolder,str(year+1))
        for day in range(1,60):
            filePath=os.path.join(inputSubFolder,'frz'+str(year+1)+str(day).zfill(3)+'.tif')
            inDS=gdal.Open(filePath)
            band=inDS.GetRasterBand(1)
            arr=numpy.concatenate((arr,band.ReadAsArray(0,0,cols,int(rows/2)).reshape(1,int(rows/2),cols)),0)
            inDS=None
            band=None
            print ('frz'+str(year+1)+str(day).zfill(3)+'.tif')
            idx=idx+1

        startArr=numpy.ones([int(rows/2),cols],dtype=int)*(-4)
        for r in range(arr.shape[1]):
            for c in range(arr.shape[2]):
                pixelVals=arr[:,r,c]

                if numpy.all(pixelVals==1):
                    # all days are non-frozen (-1)
                    startArr[r,c]=-2
                elif numpy.any(pixelVals==4):
                    # non-cold constaint (-2)
                    startArr[r,c]=-3
                elif numpy.any(pixelVals==99):
                    # freeze-thaw status not available or open water (-3)
                    continue
                else:
                    for i in range(7,arr.shape[0]-7):
                        sub=pixelVals[(i-7):(i+8)]
                        if len(sub[numpy.where((sub==0)|(sub==2)|(sub==3))])>=8:
                            if i<122:
                                startDate=245+i
                                startArr[r,c]=startDate
                                break
                            else:
                                startDate=i-121
                                startArr[r,c]=startDate
                                break

                        if i==(arr.shape[0]-8):
                            # no evident frozen season
                            startArr[r,c]=-1

        array2raster(startArr,os.path.join(outFolder,'start'+str(year)+'.tif'),geotransform,sr)
        print('The start of frozen season for year '+str(year)+' has been derived')
        arr=numpy.empty([0,int(rows/2),cols],dtype=int)
    else:
        # the next year is leap year
        if (year+1)%4==0:
##            arr=numpy.zeros([182,int(rows/2),cols],dtype=int)
            inputSubFolder=os.path.join(inputFolder,str(year))
            idx=0
            for day in range(244,366):
                filePath=os.path.join(inputSubFolder,'frz'+str(year)+str(day).zfill(3)+'.tif')
                inDS=gdal.Open(filePath)
                band=inDS.GetRasterBand(1)
                arr=numpy.concatenate((arr,band.ReadAsArray(0,0,cols,int(rows/2)).reshape(1,int(rows/2),cols)),0)
##                arr[idx]=band.ReadAsArray(0,0,cols,int(rows/2))
                inDS=None
                band=None
                print ('frz'+str(year)+str(day).zfill(3)+'.tif')
                idx=idx+1

            inputSubFolder=os.path.join(inputFolder,str(year+1))
            for day in range(1,61):
                filePath=os.path.join(inputSubFolder,'frz'+str(year+1)+str(day).zfill(3)+'.tif')
                inDS=gdal.Open(filePath)
                band=inDS.GetRasterBand(1)
                arr=numpy.concatenate((arr,band.ReadAsArray(0,0,cols,int(rows/2)).reshape(1,int(rows/2),cols)),0)
##                arr[idx]=band.ReadAsArray(0,0,cols,int(rows/2))
                inDS=None
                band=None
                print ('frz'+str(year+1)+str(day).zfill(3)+'.tif')
                idx=idx+1

            startArr=numpy.ones([int(rows/2),cols],dtype=int)*(-4)
            for r in range(arr.shape[1]):
                for c in range(arr.shape[2]):
                    pixelVals=arr[:,r,c]

                    if numpy.all(pixelVals==1):
                        # all days are non-frozen
                        startArr[r,c]=-2
                    elif numpy.any(pixelVals==4):
                        # non-cold constaint
                        startArr[r,c]=-3
                    elif numpy.any(pixelVals==99):
                        continue
                    else:
                        for i in range(7,arr.shape[0]-7):
                            sub=pixelVals[(i-7):(i+8)]
                            if len(sub[numpy.where((sub==0)|(sub==2)|(sub==3))])>=8:
                                if i<122:
                                    startDate=244+i
                                    startArr[r,c]=startDate
                                    break
                                else:
                                    startDate=i-121
                                    startArr[r,c]=startDate
                                    break

                            if i==(arr.shape[0]-8):
                                # no evident frozen season
                                startArr[r,c]=-1

            array2raster(startArr,os.path.join(outFolder,'start'+str(year)+'.tif'),geotransform,sr)
            print('The start of frozen season for year '+str(year)+' has been derived')
            arr=numpy.empty([0,int(rows/2),cols],dtype=int)
        else:
##            arr=numpy.zeros([181,int(rows/2),cols],dtype=int)
            inputSubFolder=os.path.join(inputFolder,str(year))
            idx=0
            for day in range(244,366):
                filePath=os.path.join(inputSubFolder,'frz'+str(year)+str(day).zfill(3)+'.tif')
                inDS=gdal.Open(filePath)
                band=inDS.GetRasterBand(1)
                arr=numpy.concatenate((arr,band.ReadAsArray(0,0,cols,int(rows/2)).reshape(1,int(rows/2),cols)),0)
                inDS=None
                band=None
                print ('frz'+str(year)+str(day).zfill(3)+'.tif')
                idx=idx+1

            inputSubFolder=os.path.join(inputFolder,str(year+1))
            for day in range(1,60):
                filePath=os.path.join(inputSubFolder,'frz'+str(year+1)+str(day).zfill(3)+'.tif')
                inDS=gdal.Open(filePath)
                band=inDS.GetRasterBand(1)
                arr=numpy.concatenate((arr,band.ReadAsArray(0,0,cols,int(rows/2)).reshape(1,int(rows/2),cols)),0)
                inDS=None
                band=None
                print ('frz'+str(year+1)+str(day).zfill(3)+'.tif')
                idx=idx+1

            startArr=numpy.ones([int(rows/2),cols],dtype=int)*(-4)
            for r in range(arr.shape[1]):
                for c in range(arr.shape[2]):
                    pixelVals=arr[:,r,c]

                    if numpy.all(pixelVals==1):
                        # all days are non-frozen
                        startArr[r,c]=-2
                    elif numpy.any(pixelVals==4):
                        # non-cold constaint
                        startArr[r,c]=-3
                    elif numpy.any(pixelVals==99):
                        continue
                    else:
                        for i in range(7,arr.shape[0]-7):
                            sub=pixelVals[(i-7):(i+8)]
                            if len(sub[numpy.where((sub==0)|(sub==2)|(sub==3))])>=8:
                                if i<122:
                                    startDate=244+i
                                    startArr[r,c]=startDate
                                    break
                                else:
                                    startDate=i-121
                                    startArr[r,c]=startDate
                                    break

                            if i==(arr.shape[0]-8):
                                # no evident frozen season
                                startArr[r,c]=-1

            array2raster(startArr,os.path.join(outFolder,'start'+str(year)+'.tif'),geotransform,sr)
            print('The start of frozen season for year '+str(year)+' has been derived')
            arr=numpy.empty([0,int(rows/2),cols],dtype=int)






