import gdal
from gdalconst import *
import numpy as np
import os
import glob
import osr
import datetime
import shutil

#*************************************************************************************
def array2raster(array,newRasterfn,geotrans,projection):

    cols = array.shape[1]
    rows = array.shape[0]

    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_UInt16)

    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRaster.SetGeoTransform(geotrans)
##    outRasterSRS = osr.SpatialReference()
##    outRasterSRS.ImportFromEPSG(3410)
    outRaster.SetProjection(projection)
    outband.FlushCache()
    outRaster=None
#*************************************************************************************
# calendar date to julian date
def ToDayOfYear(d):
    # d format: yyyymmdd (e.g., 20101001)
    dt=datetime.datetime.strptime(d,"%Y%m%d")
    doy=dt.strftime('%j')
    return int(doy)
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

start_mon=week_ranges[0][0:week_ranges[0].index('_')]
last_ele=week_ranges[len(week_ranges)-1]
end_mon=last_ele[last_ele.index('_')+1:len(week_ranges)]
# add one more at the start and end of week list
left_edge_sun=(datetime.datetime.strptime(start_mon,'%Y%m%d')-datetime.timedelta(days=1)).strftime('%Y%m%d')
left_edge_mon=(datetime.datetime.strptime(start_mon,'%Y%m%d')-datetime.timedelta(days=7)).strftime('%Y%m%d')

right_edge_sun=(datetime.datetime.strptime(end_mon,'%Y%m%d')+datetime.timedelta(days=7)).strftime('%Y%m%d')
right_edge_mon=(datetime.datetime.strptime(end_mon,'%Y%m%d')+datetime.timedelta(days=1)).strftime('%Y%m%d')

week_ranges.insert(0,left_edge_mon+'_'+left_edge_sun)
week_ranges.insert(len(week_ranges),right_edge_mon+'_'+right_edge_sun)

#*************************************************************************************
def FilterCloudPixels(arr):
    rows=arr.shape[1]
    cols=arr.shape[2]
    filteredArr=np.zeros((rows,cols),dtype='uint16')
    if arr.shape[0]==2:
        for r in range(1,rows-1):
            for c in range(1,cols-1):
                if arr[0,r,c]==10:
                    sub=arr[0,(r-1):(r+2),(c-1):(c+2)]
                    inds=np.sum((sub==17) | (sub==11)| (sub==13)| (sub==211)| (sub==213))

                    if inds>=4:
                        inds_dry=np.sum((sub==17) | (sub==11)| (sub==13))
                        inds_wet=np.sum((sub==211)| (sub==213))
                        if inds_dry>=inds_wet:
                            filteredArr[r,c]=11
                        else:
                            filteredArr[r,c]=211
                    else:
                        if arr[1,r,c]==10:
                            subNear=arr[1,(r-1):(r+2),(c-1):(c+2)]
                            indsNear=np.sum((subNear==17) | (subNear==11)| (subNear==13)| (subNear==211)| (subNear==213))
                            if indsNear>=4:
                                indsNear_dry=np.sum((subNear==17) | (subNear==11)| (subNear==13))
                                indsNear_wet=np.sum((subNear==211)| (subNear==213))
                                if indsNear_dry>=indsNear_wet:
                                    nearVal=11
                                else:
                                    nearVal=211
                            else:
                                filteredArr[r,c]=10
                                continue
                        elif arr[1,r,c]==17:
                            nearVal=11
                        else:
                            nearVal=arr[1,r,c]
                        if nearVal in [11, 211]:
                            filteredArr[r,c]=nearVal
                        else:
                            filteredArr[r,c]=10

                elif arr[0,r,c]==17:
                    filteredArr[r,c]=11
                else:
                    filteredArr[r,c]=arr[0,r,c]

    if arr.shape[0]==3:
        for r in range(1,rows-1):
            for c in range(1,cols-1):
                if arr[1,r,c]==10:
                    sub=arr[1,(r-1):(r+2),(c-1):(c+2)]
                    inds=np.sum((sub==17) | (sub==11)| (sub==13)| (sub==211)| (sub==213))

                    if inds>=4:
                        inds_dry=np.sum((sub==17) | (sub==11)| (sub==13))
                        inds_wet=np.sum((sub==211)| (sub==213))
                        if inds_dry>=inds_wet:
                            filteredArr[r,c]=11
                        else:
                            filteredArr[r,c]=211
                    else:
                        if arr[0,r,c]==10:
                            subL=arr[0,(r-1):(r+2),(c-1):(c+2)]
                            indsL=np.sum((subL==17) | (subL==11)| (subL==13)| (subL==211)| (subL==213))
                            if indsL>=4:
                                indsL_dry=np.sum((subL==17) | (subL==11)| (subL==13))
                                indsL_wet=np.sum((subL==211)| (subL==213))
                                if indsL_dry>=indsL_wet:
                                    leftVal=11
                                else:
                                    leftVal=211
                            else:
                                filteredArr[r,c]=10
                                continue
                        else:
                            leftVal=arr[0,r,c]

                        if arr[2,r,c]==10:
                            subR=arr[2,(r-1):(r+2),(c-1):(c+2)]
                            indsR=np.sum((subR==17) | (subR==11)| (subR==13)| (subR==211)| (subR==213))
                            if indsR>=4:
                                indsR_dry=np.sum((subR==17) | (subR==11)| (subR==13))
                                indsR_wet=np.sum((subR==211)| (subR==213))
                                if indsR_dry>=indsR_wet:
                                    rightVal=11
                                else:
                                    rightVal=211
                            else:
                                filteredArr[r,c]=10
                                continue
                        else:
                            rightVal=arr[2,r,c]

                        if leftVal in [11,211] and rightVal in [11,211]:
                            if leftVal==11 or rightVal==11:
                                filteredArr[r,c]=11
                            else:
                                filteredArr[r,c]=211
                        else:
                            filteredArr[r,c]=10

                elif arr[1,r,c]==17:
                    # assign areas with polar night as snow cover
                    filteredArr[r,c]=11
                else:
                    filteredArr[r,c]=arr[1,r,c]

    return filteredArr
#*************************************************************************************
def FilterCloudPixels2(arr):
    rows=arr.shape[1]
    cols=arr.shape[2]
    filteredArr=np.zeros((rows,cols),dtype='uint16')
    if arr.shape[0]==2:
        filteredArr[0,:]=arr[0,0,:]
        filteredArr[rows-1,:]=arr[0,rows-1,:]
        filteredArr[:,0]=arr[0,:,0]
        filteredArr[:,cols-1]=arr[0,:,cols-1]
        for r in range(1,rows-1):
            for c in range(1,cols-1):
                if arr[0,r,c]==10:
                    sub=arr[0,(r-1):(r+2),(c-1):(c+2)]
                    inds=np.sum((sub==17) | (sub==11)| (sub==13)| (sub==211)| (sub==213))

                    if inds>=4:
                        inds_dry=np.sum((sub==17) | (sub==11)| (sub==13))
                        inds_wet=np.sum((sub==211)| (sub==213))
                        if inds_dry>=inds_wet:
                            filteredArr[r,c]=11
                        else:
                            filteredArr[r,c]=211
                    else:
                        if arr[1,r,c]==10:
                            subNear=arr[1,(r-1):(r+2),(c-1):(c+2)]
                            indsNear=np.sum((subNear==17) | (subNear==11)| (subNear==13)| (subNear==211)| (subNear==213))
                            if indsNear>=4:
                                indsNear_dry=np.sum((subNear==17) | (subNear==11)| (subNear==13))
                                indsNear_wet=np.sum((subNear==211)| (subNear==213))
                                if indsNear_dry>=indsNear_wet:
                                    nearVal=11
                                else:
                                    nearVal=211
                            else:
                                filteredArr[r,c]=10
                                continue
                        elif arr[1,r,c]==17:
                            nearVal=11

                        else:
                            nearVal=arr[1,r,c]
                        if nearVal in [11, 211]:
                            filteredArr[r,c]=nearVal
                        else:
                            filteredArr[r,c]=10

                elif arr[0,r,c]==17:
                    filteredArr[r,c]=11
                else:
                    filteredArr[r,c]=arr[0,r,c]

    if arr.shape[0]==3:

        filteredArr[0,:]=arr[1,0,:]
        filteredArr[rows-1,:]=arr[1,rows-1,:]
        filteredArr[:,0]=arr[1,:,0]
        filteredArr[:,cols-1]=arr[1,:,cols-1]
        for r in range(1,rows-1):
            for c in range(1,cols-1):
                if arr[1,r,c]==10:
                    sub=arr[1,(r-1):(r+2),(c-1):(c+2)]
                    inds=np.sum((sub==17) | (sub==11)| (sub==13)| (sub==211)| (sub==213))

                    if inds>=4:
                        inds_dry=np.sum((sub==17) | (sub==11)| (sub==13))
                        inds_wet=np.sum((sub==211)| (sub==213))
                        if inds_dry>=inds_wet:
                            filteredArr[r,c]=11
                        else:
                            filteredArr[r,c]=211
                    else:
                        if arr[0,r,c]==10:
                            subL=arr[0,(r-1):(r+2),(c-1):(c+2)]
                            indsL=np.sum((subL==17) | (subL==11)| (subL==13)| (subL==211)| (subL==213))
                            if indsL>=4:
                                indsL_dry=np.sum((subL==17) | (subL==11)| (subL==13))
                                indsL_wet=np.sum((subL==211)| (subL==213))
                                if indsL_dry>=indsL_wet:
                                    leftVal=11
                                else:
                                    leftVal=211
                            else:
                                leftVal=10
##                                continue
                        elif arr[0,r,c]==17:
                            leftVal==11
                        else:
                            leftVal=arr[0,r,c]

                        if arr[2,r,c]==10:
                            subR=arr[2,(r-1):(r+2),(c-1):(c+2)]
                            indsR=np.sum((subR==17) | (subR==11)| (subR==13)| (subR==211)| (subR==213))
                            if indsR>=4:
                                indsR_dry=np.sum((subR==17) | (subR==11)| (subR==13))
                                indsR_wet=np.sum((subR==211)| (subR==213))
                                if indsR_dry>=indsR_wet:
                                    rightVal=11
                                else:
                                    rightVal=211
                            else:
                                rightVal=10
                        elif arr[2,r,c]==17:
                            rightVal=11
                        else:
                            rightVal=arr[2,r,c]

                        if leftVal in [11,211] or rightVal in [11,211]:
                            if leftVal==11 or rightVal==11:
                                filteredArr[r,c]=11
                            else:
                                filteredArr[r,c]=211
                        else:
                            filteredArr[r,c]=10

                elif arr[1,r,c]==17:
                    # assign areas with polar night as snow cover
                    filteredArr[r,c]=11
                else:
                    filteredArr[r,c]=arr[1,r,c]

    return filteredArr



#*************************************************************************************
os.chdir('/mnt/stratus/lzhu68/global_snow_soil_freeze_project2/weekly_snow_cover_extent')

##os.chdir('S:/lzhu68/global_snow_soil_freeze_project2/weekly_snow_cover_extent')
outputFolder='./filtered_snow_cover_extent_nh_modis'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
##os.chdir('S:/lzhu68/global_snow_soil_freeze_project2/weekly_snow_cover_extent/unzip')
sr=osr.SpatialReference()
sr.ImportFromEPSG(4326)
new_sr=sr.ExportToWkt()

geotrans=tuple((0,0.05,0,90,0,-0.05))

##rows=3601
##cols=7200

fid=open('./missed_avhrr_sc_file.txt','w')
months_to_consider=[12,1,2]
index=0

# save the file coresponding to the element of week ranges
wk1="20000228_20000305"
yearFolder=wk1[wk1.index('_')+1:wk1.index('_')+5]
filepath=glob.glob('./unzip/'+yearFolder+'/M5C*'+wk1+'*hdf')
outputPath=outputFolder+'/sc'+wk1+'.tif'
ds=gdal.Open(gdal.Open(filepath[0]).GetSubDatasets()[0][0])
arr=ds.ReadAsArray(0,0,7200,1801)
ds=None
array2raster(arr,outputPath,geotrans,new_sr)

for i in range(1,len(week_ranges)-1):
    # target file
    wk=week_ranges[i]
    yearFolder=wk[wk.index('_')+1:wk.index('_')+5]
    mon=wk[wk.index('_')+5:wk.index('_')+7]
    # adjacent files for intepolating cloud pixels
    wk_b1=week_ranges[i-1]
    yearFolder_b1=wk_b1[wk_b1.index('_')+1:wk_b1.index('_')+5]
    mon_b1=wk_b1[wk_b1.index('_')+5:wk_b1.index('_')+7]
    wk_a1=week_ranges[i+1]
    yearFolder_a1=wk_a1[wk_a1.index('_')+1:wk_a1.index('_')+5]
    mon_a1=wk_a1[wk_a1.index('_')+5:wk_a1.index('_')+7]
    
    filepath=glob.glob('./unzip/'+yearFolder+'/M5C*'+wk+'*.hdf')
    if len(filepath)==0:
        fid.write(wk+'\n')
        print('The file for the week '+wk+' is not available.')
        continue
        
#    filepath=glob.glob('./unzip/'+yearFolder+'/MER*'+wk+'*.tif')
#    if len(filepath)==0:
#        filepath=glob.glob('./unzip/'+yearFolder+'/GHR*'+wk+'*.hdf')
#        if len(filepath)==0:
#            filepath=glob.glob('./unzip/'+yearFolder+'/M5C*'+wk+'*.hdf')
#    if len(filepath)==0:
#        fid.write(wk+'\n')
#        print('The file for the week '+wk+' is not available.')
#        continue

    # output
    outputPath=outputFolder+'/sc'+wk+'.tif'
    if os.path.exists(outputPath):
        continue
    if int(mon) in months_to_consider:
        filepath_b1=glob.glob(outputFolder+'/*'+wk_b1+'*.tif')
        filepath_a1=glob.glob('./unzip/'+yearFolder_a1+'/M5C*'+wk_a1+'*.hdf')
#        filepath_a1=glob.glob('./unzip/'+yearFolder_a1+'/MER*'+wk_a1+'*.tif')
#        if len(filepath_a1)==0:
#            filepath_a1=glob.glob('./unzip/'+yearFolder_a1+'/GHR*'+wk_a1+'*.hdf')
#            if len(filepath_a1)==0:
#                filepath_a1=glob.glob('./unzip/'+yearFolder_a1+'/M5C*'+wk_a1+'*.hdf')
        if (len(filepath_b1)==0 and len(filepath_a1)==0):
#            if filepath[0].endswith('.tif'):
#                ds_target=gdal.Open(filepath[0])
#                weekArr=ds_target.ReadAsArray(0,0,7200,1801)
#                weekArr[weekArr==17]=11
#                array2raster(weekArr,outputPath,geotrans,new_sr)
#                print(os.path.basename(filepath[0])+' is copied to target folder without filtering')
#                ds_target=None
#            if filepath[0].endswith('.hdf'):
            ds_target=gdal.Open(gdal.Open(filepath[0]).GetSubDatasets()[0][0])
            weekArr=ds_target.ReadAsArray(0,0,7200,1801)
            weekArr[weekArr==17]=11
            array2raster(weekArr,outputPath,geotrans,new_sr)
            ds_target=None
            print(os.path.basename(filepath[0])+' is copied to target folder without filtering')
        else:
            if len(filepath_a1)==1 and len(filepath_b1)==1:
                scArr=np.empty((0,1801,7200),dtype='uint16')
                ds_b1=gdal.Open(filepath_b1[0])
                scArr=np.concatenate((scArr,ds_b1.ReadAsArray(0,0,7200,1801).reshape(1,1801,7200)),0)
                ds_b1=None
#                if filepath[0].endswith('.tif'):
#                    ds_target=gdal.Open(filepath[0])
#                    scArr=np.concatenate((scArr,ds_target.ReadAsArray(0,0,7200,1801).reshape(1,1801,7200)),0)
#                    ds_target=None
#                else:
                ds_target=gdal.Open(gdal.Open(filepath[0]).GetSubDatasets()[0][0])
                scArr=np.concatenate((scArr,ds_target.ReadAsArray(0,0,7200,1801).reshape(1,1801,7200)),0)
                ds_target=None
#                if filepath_a1[0].endswith('.tif'):
#                    ds_a1=gdal.Open(filepath_a1[0])
#                    scArr=np.concatenate((scArr,ds_a1.ReadAsArray(0,0,7200,1801).reshape(1,1801,7200)),0)
#                    ds_a1=None
#                else:
                ds_a1=gdal.Open(gdal.Open(filepath_a1[0]).GetSubDatasets()[0][0])
                scArr=np.concatenate((scArr,ds_a1.ReadAsArray(0,0,7200,1801).reshape(1,1801,7200)),0)
                ds_a1=None
                # function to filter cloud pixels
                filteredScArr=FilterCloudPixels2(scArr)
                array2raster(filteredScArr,outputPath,geotrans,new_sr)

                scArr=None
            else:
                if len(filepath_b1)==1:
                    scArr=np.empty((0,1801,7200),dtype='uint16')
#                    if filepath[0].endswith('.tif'):
#                        ds_target=gdal.Open(filepath[0])
#                        scArr=np.concatenate((scArr,ds_target.ReadAsArray(0,0,7200,1801).reshape(1,1801,7200)),0)
#                        ds_target=None
#                    else:
                    ds_target=gdal.Open(gdal.Open(filepath[0]).GetSubDatasets()[0][0])
                    scArr=np.concatenate((scArr,ds_target.ReadAsArray(0,0,7200,1801).reshape(1,1801,7200)),0)
                    ds_target=None

                    ds_b1=gdal.Open(filepath_b1[0])
                    scArr=np.concatenate((scArr,ds_b1.ReadAsArray(0,0,7200,1801).reshape(1,1801,7200)),0)
                    ds_b1=None
                    # function to filter cloud pixels
                    filteredScArr=FilterCloudPixels(scArr)
                    array2raster(filteredScArr,outputPath,geotrans,new_sr)
                    scArr=None
                else:
                    scArr=np.empty((0,1801,7200),dtype='uint16')
#                    if filepath[0].endswith('.tif'):
#                        ds_target=gdal.Open(filepath[0])
#                        scArr=np.concatenate((scArr,ds_target.ReadAsArray(0,0,7200,1801).reshape(1,1801,7200)),0)
#                        ds_target=None
#                    else:
                    ds_target=gdal.Open(gdal.Open(filepath[0]).GetSubDatasets()[0][0])
                    scArr=np.concatenate((scArr,ds_target.ReadAsArray(0,0,7200,1801).reshape(1,1801,7200)),0)
                    ds_target=None
#                    if filepath_a1[0].endswith('.tif'):
#                        ds_a1=gdal.Open(filepath_a1[0])
#                        scArr=np.concatenate((scArr,ds_a1.ReadAsArray(0,0,7200,1801).reshape(1,1801,7200)),0)
#                        ds_a1=None
#                    else:
                    ds_a1=gdal.Open(gdal.Open(filepath_a1[0]).GetSubDatasets()[0][0])
                    scArr=np.concatenate((scArr,ds_a1.ReadAsArray(0,0,7200,1801).reshape(1,1801,7200)),0)
                    ds_a1=None
                    # function to filter cloud pixels
                    filteredScArr=FilterCloudPixels2(scArr)
                    array2raster(filteredScArr,outputPath,geotrans,new_sr)
                    scArr=None

    else:
        outputPath=outputFolder+'/sc'+wk+'.tif'
        if os.path.exists(outputPath):
            continue
#        if filepath[0].endswith('.tif'):
#            ds_target=gdal.Open(filepath[0])
#            weekArr=ds_target.ReadAsArray(0,0,7200,1801)
#            weekArr[weekArr==17]=11
#            array2raster(weekArr,outputPath,geotrans,new_sr)
#            ds_target=None
###                shutil.copy(filepath[0],outputPath)
#            print(os.path.basename(filepath[0])+' is copied to target folder without filtering')
#        if filepath[0].endswith('.hdf'):
        ds_target=gdal.Open(gdal.Open(filepath[0]).GetSubDatasets()[0][0])
        weekArr=ds_target.ReadAsArray(0,0,7200,1801)
        weekArr[weekArr==17]=11
        array2raster(weekArr,outputPath,geotrans,new_sr)
        ds_target=None
        print(os.path.basename(filepath[0])+' is copied to target folder without filtering')


fid.close()









