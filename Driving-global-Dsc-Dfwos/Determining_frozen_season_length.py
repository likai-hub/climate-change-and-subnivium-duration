# get the length of frozen season:Northern Hemisphere

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


for year in range(1982,2016):
    if year%4==0:
        input1='./frozen_season/season_start_nh/start'+str(year)+'.tif'
        input2='./frozen_season/season_end_nh/end'+str(year)+'.tif'
        outFolder='./frozen_season/season_length_nh'
        if not os.path.exists(outFolder):
            os.makedirs(outFolder)
        driver=gdal.GetDriverByName('GTiff')

        # basic information of raster
        template=gdal.Open(input1)
        cols=template.RasterXSize
        rows=template.RasterYSize
        sr=template.GetProjection()
        geotransform=template.GetGeoTransform()
        template=None

        outArr=numpy.zeros([2,rows,cols],dtype=int)
        ds1=gdal.Open(input1)
        layer1=ds1.GetRasterBand(1)
        outArr[0]=layer1.ReadAsArray(0,0,cols,rows)
        ds1=None
        layer1=None

        ds2=gdal.Open(input2)
        layer2=ds2.GetRasterBand(1)
        outArr[1]=layer2.ReadAsArray(0,0,cols,rows)
        ds2=None
        layer2=None

        length=numpy.ones([rows,cols],dtype=int)*(-4)
        for r in range(outArr.shape[1]):
            for c in range(outArr.shape[2]):
                subset=outArr[:,r,c]
                if numpy.any(subset==-4):
                    continue
                elif numpy.any(subset==-3):
                    length[r,c]=-3
                elif numpy.any(subset==-2):
                    length[r,c]=-2
                elif subset[0]==-1:
                    length[r,c]=0
                elif subset[0]>=252:
                    if (subset[0]==252 and subset[1]==-1):
                        length[r,c]=365
                    else:
                        length[r,c]=(366-subset[0]+1)+subset[1]
                else:
                    if subset[1]==-1:
                        length[r,c]=244-subset[0]+1
                    else:
                        length[r,c]=subset[1]-subset[0]+1

        array2raster(length,os.path.join(outFolder,'length'+str(year)+'.tif'),geotransform,sr)
        print('The length of the frozen season for year '+str(year)+' has been calculated ')

    else:
        if (year+1)%4==0:
            input1='./frozen_season/season_start_nh/start'+str(year)+'.tif'
            input2='./frozen_season/season_end_nh/end'+str(year)+'.tif'
            outFolder='./frozen_season/season_length_nh'
##            input1=r'N:\likai\global_freeze_snow_project\latest_processing\frozen_season\season_start_nh\start'+str(year)+'.tif'
##            input2=r'N:\likai\global_freeze_snow_project\latest_processing\frozen_season\season_end_nh\end'+str(year)+'.tif'
##            outFolder=r'N:\likai\global_freeze_snow_project\latest_processing\frozen_season\season_length_nh'
            if not os.path.exists(outFolder):
                os.mkdir(outFolder)
            driver=gdal.GetDriverByName('GTiff')

            # basic information of raster
            template=gdal.Open(input1)
            cols=template.RasterXSize
            rows=template.RasterYSize
            sr=template.GetProjection()
            geotransform=template.GetGeoTransform()
            origin=[geotransform[0],geotransform[3]]
            pixelWidth=geotransform[1]
            pixelHeight=geotransform[5]
            template=None

            outArr=numpy.zeros([2,rows,cols],dtype=int)
            ds1=gdal.Open(input1)
            layer1=ds1.GetRasterBand(1)
            outArr[0]=layer1.ReadAsArray(0,0,cols,rows)
            ds1=None
            layer1=None

            ds2=gdal.Open(input2)
            layer2=ds2.GetRasterBand(1)
            outArr[1]=layer2.ReadAsArray(0,0,cols,rows)
            ds2=None
            layer2=None

            length=numpy.ones([rows,cols],dtype=int)*(-4)
            for r in range(outArr.shape[1]):
                for c in range(outArr.shape[2]):
                    subset=outArr[:,r,c]
                    if numpy.any(subset==-4):
                        continue
                    elif numpy.any(subset==-3):
                        length[r,c]=-3
                    elif numpy.any(subset==-2):
                        length[r,c]=-2

                    elif subset[0]==-1:
                        length[r,c]=0
                    elif subset[0]>=251:
                        if (subset[0]==251 and subset[1]==-1):
                            length[r,c]=366
                        else:
                            length[r,c]=(365-subset[0]+1)+subset[1]
                    else:
                        if subset[1]==-1:
                            length[r,c]=244-subset[0]+1
                        else:
                            length[r,c]=subset[1]-subset[0]+1

            array2raster(length,os.path.join(outFolder,'length'+str(year)+'.tif'),geotransform,sr)
            print('The length of the frozen season for year '+str(year)+' has been calculated ')
        else:
            input1='./frozen_season/season_start_nh/start'+str(year)+'.tif'
            input2='./frozen_season/season_end_nh/end'+str(year)+'.tif'
            outFolder='./frozen_season/season_length_nh'
            if not os.path.exists(outFolder):
                os.mkdir(outFolder)
            driver=gdal.GetDriverByName('GTiff')

            # basic information of raster
            template=gdal.Open(input1)
            cols=template.RasterXSize
            rows=template.RasterYSize
            sr=template.GetProjection()
            geotransform=template.GetGeoTransform()
            origin=[geotransform[0],geotransform[3]]
            pixelWidth=geotransform[1]
            pixelHeight=geotransform[5]
            template=None

            outArr=numpy.zeros([2,rows,cols],dtype=int)
            ds1=gdal.Open(input1)
            layer1=ds1.GetRasterBand(1)
            outArr[0]=layer1.ReadAsArray(0,0,cols,rows)
            ds1=None
            layer1=None

            ds2=gdal.Open(input2)
            layer2=ds2.GetRasterBand(1)
            outArr[1]=layer2.ReadAsArray(0,0,cols,rows)
            ds2=None
            layer2=None

            length=numpy.ones([rows,cols],dtype=int)*(-4)
            for r in range(outArr.shape[1]):
                for c in range(outArr.shape[2]):
                    subset=outArr[:,r,c]
                    if numpy.any(subset==-4):
                        continue
                    elif numpy.any(subset==-3):
                        length[r,c]=-3
                    elif numpy.any(subset==-2):
                        length[r,c]=-2
                    elif subset[0]==-1:
                        length[r,c]=0
                    elif subset[0]>=251:
                        if (subset[0]==251 and subset[1]==-1):
                            length[r,c]=365
                        else:
                            length[r,c]=(365-subset[0]+1)+subset[1]
                    else:
                        if subset[1]==-1:
                            length[r,c]=244-subset[0]+1
                        else:
                            length[r,c]=subset[1]-subset[0]+1

            array2raster(length,os.path.join(outFolder,'length'+str(year)+'.tif'),geotransform,sr)
            print('The length of the frozen season for year '+str(year)+' has been calculated ')
