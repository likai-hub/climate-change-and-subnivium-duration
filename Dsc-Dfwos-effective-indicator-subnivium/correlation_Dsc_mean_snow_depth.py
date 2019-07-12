# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 13:41:22 2019

@author: Administrator
"""
# The unit for snot depth is cm
import os
import numpy as np
import datetime
#*************************************************************************************
# calendar date to julian date
def ToDayOfYear(d):
    # d format: yyyymmdd (e.g., 20101001)
    dt=datetime.datetime.strptime(d,"%Y%m%d")
    doy=dt.strftime('%j')
    return int(doy)

#*************************************************************************************
def CheckStatus(ele,startval,endval,year):
    # ele: %Y%m%d_%Y%m%d
    startd=datetime.datetime.strptime(ele,'%Y%m%d')
##    endd=datetime.datetime.strptime(ele[ele.index('_'):len(ele)],'%Y%m%d')
#    middt=startd+datetime.timedelta(days=3)
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
    if st<=startd.date()<=et:
        return True
    else:
        return False

#*************************************************************************************
outputFolder=r'G:\in_situ_measurements_snow\processing\snowdepth_dsc_coupling\correlation'
if not os.path.exists(outputFolder):
    print('exists, do not create')
    os.makedirs(outputFolder)        
#  frozen season
fstart=r'G:\in_situ_measurements_snow\processing\snowdepth_dsc_coupling\frozen_season_stations_txt\ghcn_start.txt'
fend=r'G:\in_situ_measurements_snow\processing\snowdepth_dsc_coupling\frozen_season_stations_txt\ghcn_end.txt'
# soil temperature of stations
stFolder=r'G:\in_situ_measurements_snow\ghcn\selected_stations_snowdepth'
# snow status folder
#snowFolder=r'G:\in_situ_measurements_snow\processing\snow_status_stations_snotel_txt'

stnList=[f[0:f.index('_snowdepth.txt')] for f in os.listdir(stFolder) if f.endswith('.txt')]
#snowStnList=[f[0:f.index('.txt')] for f in os.listdir(snowFolder) if f.endswith('.txt')]

stnSeries=[]
fid1=open(fstart,'r')
line=fid1.readline()
lineIndex=1
while line:
    line=line.rstrip().split(',')
    stnSeries.append(line[0])
    linec=map(lambda x: float(x),line[1:])
    if lineIndex==1:
        arrStart=np.array(linec)
        lineIndex=lineIndex+1
        line=fid1.readline()
    else:
        arrStart=np.vstack((arrStart,np.array(linec)))
        line=fid1.readline()
fid1.close()

fid2=open(fend,'r')
line=fid2.readline()
lineIndex=1
while line:
    linec=map(lambda x: float(x),line.rstrip().split(',')[1:])
    if lineIndex==1:
        arrEnd=np.array(linec)
        lineIndex=lineIndex+1
        line=fid2.readline()
    else:
        arrEnd=np.vstack((arrEnd,np.array(linec)))
        line=fid2.readline()
fid2.close()

outFid=open(os.path.join(outputFolder,'cor_dsc_depth_ghcn.txt'),'w')
outFid.write('stn,cor\n')
for stn in stnList:
    if not stn in stnSeries:
        continue
#for stn in ['1000']:
#    print(stn)
#    yearlyDiff=np.empty((0))
    yearlyDsc=np.empty((0))
    yearlySd=np.empty((0))
    fid=open(os.path.join(stFolder,stn+'_snowdepth.txt'),'r')
    stArr=np.empty((0,4))
    line=fid.readline()
    while line:
        linec=map(lambda x:float(x),line.rstrip().split(','))
        stArr=np.vstack((stArr,np.array(linec[0:4])))
        line=fid.readline()
    fid.close()
    
    yearList=sorted(np.unique(stArr[:,0]))
#    weeks=[]
#    snowArr=np.empty((0))
#    if not stn in snowStnList:
#        continue
#    else:
#        fid=open(os.path.join(snowFolder,stn+'.txt'),'r')
##        snowArr=np.empty((0,4))
#        line=fid.readline()
#        while line:
#            linec=line.rstrip().split(',')
#            wk=linec[0]
#            if int(wk[0:4]) in yearList or int(wk[wk.index('_')+1:wk.index('_')+5]) in yearList:
#                weeks.append(wk)
#                snowArr=np.hstack((snowArr,float(linec[1])))
#            line=fid.readline()
#        fid.close()
    # y should be in integer format
    for y in map(lambda x:int(x),yearList[0:len(yearList)-1]):
#    for y in [2004,2005,2006]:    
        startVal=arrStart[stnSeries.index(stn),int((y-1981))]
        endVal=arrEnd[stnSeries.index(stn),int((y-1981))]
#        startVal=[335]
#        endVal=[60]        
        if startVal in [-4,-3,-2,-1] or endVal in [-4,-3,-2] and startVal.size<1 and endVal.size<1:
            continue
        else:
            stSnow=np.empty((0))
#            stNosnow=np.empty((0))
            
            months=range(9,13)+range(1,9)
            # get the dateList
            startd=datetime.date(y,9,1)
            endd=datetime.date(y+1,8,31)
            delta=endd-startd
#            dateList=[]
            for i in range(delta.days+1):
                newDate=startd+datetime.timedelta(i)
#                dateList.append(str(newDate.year)+str(newDate.month).zfill(2)+str(newDate.day).zfill(2)) 
                dt=str(newDate.year)+str(newDate.month).zfill(2)+str(newDate.day).zfill(2)
                checkRes=CheckStatus(dt,startVal,endVal,y)
                if checkRes:
                    sdvalue=stArr[(stArr[:,0]==newDate.year) &(stArr[:,1]==newDate.month)&(stArr[:,2]==newDate.day),3]
#                    atvalue=stArr[(stArr[:,0]==newDate.year) &(stArr[:,1]==newDate.month)&(stArr[:,2]==newDate.day),4]
#                    sdvalue=stArr[(stArr[:,0]==newDate.year) &(stArr[:,1]==newDate.month)&(stArr[:,2]==newDate.day),5]
                    if sdvalue.size==1:
                        if sdvalue[0]>2 and sdvalue!=-999.9:
#                        if atvalue[0]<0 and atvalue[0]!=-999 and sdvalue[0]>5 and stvalue[0]!=-999:
                            stSnow=np.hstack((stSnow,sdvalue))
            if len(stSnow)>10:
                yearlyDsc=np.hstack((yearlyDsc,len(stSnow)))
                yearlySd=np.hstack((yearlySd,np.mean(stSnow)))

    if len(yearlyDsc)>=18:
        corrValue=np.corrcoef(yearlyDsc,yearlySd)[0,1]
        outFid.write(stn+','+str(corrValue)+'\n')
        
    print(stn)        
outFid.close()                   
                