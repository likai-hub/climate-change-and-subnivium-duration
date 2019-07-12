# snow cover extent and freeze/thaw status combination
import os
from gdalconst import *
import gdal
import numpy as np
import glob
import osr
import datetime

# environmental variables
#0: duration of frozen season
#1: duration of thawed season
#2: duration of snow covered ground
#3: duration of dry snow-covered ground
#4: duration of wet snow-coverd ground
#5: duration of snow-covered frozen ground
#6: duration of snow-free frozen ground
#7: duration of dry snow-covered frozen ground
#8 duration of wet snow-covered frozen ground
#9 duration of wet snow-covered thawed ground
#10: duration of snow-free thawed ground

#*************************************************************************************
# generate all week ranges within file names

def allsundays(year):
   d = datetime.date(year, 1, 1)                    # January 1st
   d += datetime.timedelta(days = 6 - d.weekday())  # First Sunday
   while d.year == year:
      yield d
      d += datetime.timedelta(days = 7)

# generate all time ranges of weeks for each year from 1982 to 2015
week_ranges=[]
for y in range(1982,2016):
    for d in allsundays(y):
        sunday=d.strftime('%Y%m%d')
        monday=(d-datetime.timedelta(days=6)).strftime('%Y%m%d')
        week_ranges.append(monday+'_'+sunday)
#*************************************************************************************
# calendar date to julian date
def ToDayOfYear(d):
    # d format: yyyymmdd (e.g., 20101001)
    dt=datetime.datetime.strptime(d,"%Y%m%d")
    doy=dt.strftime('%j')
    return int(doy)
#*************************************************************************************
def IdentifyingDatesWithinWeek(ele):
    # format of ele: 19811221_19811227
    startd=datetime.datetime.strptime(ele[0:ele.index('_')],'%Y%m%d')
    endd=datetime.datetime.strptime(ele[ele.index('_')+1:len(ele)],'%Y%m%d')
    date_delta=endd-startd
    years=[]
    doys=[]
    for i in range(date_delta.days+1):
        dt=startd+datetime.timedelta(days=i)
        # the year and doy each date
        years.append(dt.year)
        doys.append(dt.strftime('%j'))
    return dict(year=years,doy=doys)

#*************************************************************************************
def CheckStatus(ele,startval,endval,year):
    # ele: %Y%m%d_%Y%m%d
    startd=datetime.datetime.strptime(ele[0:ele.index('_')],'%Y%m%d')
##    endd=datetime.datetime.strptime(ele[ele.index('_'):len(ele)],'%Y%m%d')
    middt=startd+datetime.timedelta(days=3)
    # start of the frozen season after September
    if startval>=245:
        st=datetime.date(year,1,1)+datetime.timedelta(days=(startval-1))
    else:
        st=datetime.date(year+1,1,1)+datetime.timedelta(days=(startval-1))
    if endval==-1:
        if (year+1)%4==0:
            et=datetime.date(year+1,1,1)+datetime.timedelta(days=243)
        else:
            et=datetime.date(year+1,1,1)+datetime.timedelta(days=242)
    else:
        et=datetime.date(year+1,1,1)+datetime.timedelta(days=(endval-1))
    # middt is datetime, using date only
    if st<=middt.date()<=et:
        return True
    else:
        return False

#*************************************************************************************
def Calculation(pixelSnow,pixelFreeze):
    pixelRes=np.zeros((11),dtype=int)
    pixelRes[0]=np.sum((pixelFreeze==0) | (pixelFreeze==2)|(pixelFreeze==3))
    pixelRes[1]=np.sum(pixelFreeze==1)
    if pixelSnow==-1:
        return pixelRes
    else:
        if pixelSnow in [11,13,17]:
            pixelRes[2]=7
            pixelRes[3]=7
            pixelRes[5]=np.sum((pixelFreeze==0) | (pixelFreeze==2)|(pixelFreeze==3))
            pixelRes[7]=np.sum((pixelFreeze==0) | (pixelFreeze==2)|(pixelFreeze==3))

        elif pixelSnow in [211,213]:
            pixelRes[2]=7
            pixelRes[4]=7
            pixelRes[5]=np.sum((pixelFreeze==0) | (pixelFreeze==2)|(pixelFreeze==3))
            pixelRes[8]=np.sum((pixelFreeze==0) | (pixelFreeze==2)|(pixelFreeze==3))
            pixelRes[9]=np.sum((pixelFreeze==1))

        elif pixelSnow in [10,15]:
            pixelRes[6]=np.sum((pixelFreeze==0) | (pixelFreeze==2)|(pixelFreeze==3))
            pixelRes[10]=np.sum((pixelFreeze==1))
        else:
            return pixelRes
    return pixelRes

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
    outRaster=None
#*************************************************************************************
# set working direcotory
##os.chdir('S:/lzhu68/global_snow_soil_freeze_project2')

os.chdir('S:/lzhu68/global_snow_soil_freeze_project2')

# daily freeze/thaw records
inputFreeze='./freeze_thaw_dataset/filtered_freeze_thaw_record79_16'
# frozen start and end
inputStart='./freeze_thaw_dataset/frozen_season/season_start_nh'
inputEnd='./freeze_thaw_dataset/frozen_season/season_end_nh'
# input weekly snow
inputSnow='./weekly_snow_cover_extent/filtered_snow_cover_extent_nh_modis'
# output
outputPath='./outputs_snow_cover_freeze_variables00_14/modis_nh'
if not os.path.exists(outputPath):
    os.makedirs(outputPath)
#**************************
snowTemplate=inputSnow+'/sc20000228_20000305.tif'
ds1=gdal.Open(snowTemplate)
rows1=ds1.RasterYSize
cols1=ds1.RasterXSize
geotrans1=ds1.GetGeoTransform()
originX1=geotrans1[0]
originY1=geotrans1[3]
pixelWidth1=geotrans1[1]
pixelHeight1=geotrans1[5]
proj1=ds1.GetProjection()
ds1=None
sourceSR=osr.SpatialReference()
sourceSR.ImportFromWkt(proj1)

#**************************
# template for freeze/thaw data at global scale
tempFreeze=inputFreeze+'/2014/frz2014001.tif'
ds2=gdal.Open(tempFreeze)
rows2=ds2.RasterYSize # 586
cols2=ds2.RasterXSize #
geotrans2=ds2.GetGeoTransform()
originX2=geotrans2[0]
originY2=geotrans2[3]
pixelWidth2=geotrans2[1]
pixelHeight2=geotrans2[5]
proj2=ds2.GetProjection()
ds2=None
targetSR=osr.SpatialReference()
targetSR.ImportFromWkt(proj2)
#**************************
coordTrans = osr.CoordinateTransformation(sourceSR,targetSR)

offsets=np.zeros((2,rows1,cols1),dtype=int)
for r in range(rows1):
    for c in range(cols1):
        pixelY=r*pixelHeight1+originY1+(pixelHeight1*0.05)
        pixelX=c*pixelWidth1+originX1+(pixelWidth1*0.05)
        (newX,newY,h)=coordTrans.TransformPoint(pixelX,pixelY,0)
        offsetX=int((newX-originX2)/pixelWidth2)
        offsetY=int((newY-originY2)/pixelHeight2)
        if offsetX<0 or offsetX>=(cols2) or offsetY<0 or offsetY>=(rows2/2):
            offsets[:,r,c]=np.repeat(-99,2)
        else:
            offsets[:,r,c]=np.array((offsetX,offsetY))
vars=['dfd','dtd','dsc','ddsc','dwsc','dfws','dfwos','dfwds','dfwws','dtwws','dtwos']
for y in range(2013,2014):
    #0: duration of frozen days
    #1: duration of thawed days
    #2: duration of snow covered ground
    #3: duration of dry snow-covered ground
    #4: duration of wet snow-coverd ground
    #5: duration of snow-covered frozen ground
    #6: duration of snow-free frozen ground
    #7: duration of dry snow-covered frozen ground
    #8 duration of wet snow-covered frozen ground
    #9 duration of wet snow-covered thawed ground
    #10: duration of snow-free thawed ground
    outputArr=np.zeros((11,rows1,cols1),dtype=int)
    # read start of frozen season information for specific year
    startPath=glob.glob(inputStart+'/*'+str(y)+'*.tif')
    dsStart=gdal.Open(startPath[0])
    startArr=dsStart.ReadAsArray(0,0,cols2,int(rows2*0.5))
    dsStart=None
    # read end of frozen season information for specific year
    endPath=glob.glob(inputEnd+'/*'+str(y)+'*.tif')
    dsEnd=gdal.Open(endPath[0])
    endArr=dsEnd.ReadAsArray(0,0,cols2,int(rows2*0.5))
    dsEnd=None
    # months to consider
    months=range(9,13)+range(1,9)
    for mon in months:
        if mon>=9:
            # time span for each week in this month
            searchPattern='_'+str(y)+str(mon).zfill(2)
        else:
            searchPattern='_'+str(y+1)+str(mon).zfill(2)

        searchedElements=[ele for ele in week_ranges if searchPattern in ele]

        for ele in searchedElements:
            # snow cover for specific week is not available
            snowArr=None
            snowPath=glob.glob(inputSnow+'/*'+ele+'*.tif')
            if len(snowPath)>0:
            # read snow array
                dsSnow=gdal.Open(snowPath[0])
                snowArr=dsSnow.ReadAsArray()
                dsSnow=None
            # get all the dates within the week (return dict data format)
            dts=IdentifyingDatesWithinWeek(ele)
            freezeArr=np.ones((len(dts['year']),int(rows2/2),cols2),dtype=int)*(99)
            for k in range(len(dts['year'])):
                yearfolder=str(dts['year'][k])
                doy=dts['doy'][k]
                freezePath=glob.glob(inputFreeze+'/'+yearfolder+'/*'+yearfolder+doy.zfill(3)+'*.tif')
                if len(freezePath)==0:
                    continue
                else:
                    dsf=gdal.Open(freezePath[0])
                    freezeArr[k]=dsf.ReadAsArray(0,0,cols2,int(rows2/2))
                    dsf=None
            for r in range(rows1):
                for c in range(cols1):
                    xoffset=offsets[0,r,c]
                    yoffset=offsets[1,r,c]
                    if np.any(offsets[:,r,c]==-99):
                        outputArr[:,r,c]=np.repeat(-4,11)
                    else:
                        startval=startArr[yoffset,xoffset]
                        endval=endArr[yoffset,xoffset]
                        if startval==-4 or endval==-4:
                            outputArr[:,r,c]=np.repeat(-4,11)
                        else:
                            if startval==-3 or endval==-3:
                                outputArr[:,r,c]=np.repeat(-3,11)
                            else:
                                if startval==-2 or endval==-2:
                                    outputArr[:,r,c]=np.repeat(-2,11)
                                else:
                                    if startval==-1:
                                        outputArr[:,r,c]=np.repeat(-1,11)
                                    else:
                                        status=CheckStatus(ele,startval,endval,y)
                                        if status:
                                            pixelFreeze=freezeArr[:,yoffset,xoffset]
                                            if snowArr is None:
                                                pixelSnow=-1
                                            else:
                                                pixelSnow=snowArr[r,c]
                                            pixelRes=Calculation(pixelSnow,pixelFreeze)
                                            outputArr[:,r,c]=outputArr[:,r,c]+pixelRes
                                        else:
                                            continue

            print("The data for period: "+ele+' has been processed')
#    outputFileNames=map(lambda x:x+str(y)+'.tif',vars)
    outputFileNames=[x+str(y)+'.tif' for x in vars]
    for v in range(outputArr.shape[0]):
        if not os.path.exists(os.path.join(outputPath,outputFileNames[v])):
            array2raster(outputArr[v],os.path.join(outputPath,outputFileNames[v]),geotrans1,proj1)
    print('The results for year '+str(y)+' has been generated')






