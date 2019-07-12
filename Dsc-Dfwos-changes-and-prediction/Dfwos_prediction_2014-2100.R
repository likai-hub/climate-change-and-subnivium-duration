library('raster')


rm(list = ls())
# set the working directory

setwd('H:/likai_folder/projects/global_snow_cover_freeze_change/new_processing_12_30_2017')

# folder for frozen season temperature
folder.tmp<-'./frozen_season_temp/nh_reclassified'
# folder for frozen season precipitation
folder.pre<-'./frozen_season_precip/nh_reclassified'
# folder for snow cover and freeze status variables
folder.snow.vars<-'./metrics_05degree_nh'

# output path
outputFolder<-'H:/likai_folder/projects/global_snow_cover_freeze_change/new_processing_12_30_2017/prediction_dws_dwos'
outputPath1<-paste(outputFolder,'/lrt/dwos_nh',sep='')
if (! dir.exists(outputPath1)) {dir.create(outputPath1)}
outputPath2<-paste(outputFolder,'/predicted',sep = '')
if (! dir.exists(outputPath2)) {dir.create(outputPath2)}

inputFolder<-'H:/likai_folder/projects/global_snow_cover_freeze_change/new_processing_12_30_2017/prediction'
folderList<-list.dirs(inputFolder,recursive = FALSE)
#--------------------------------------------------
# array to save frozen season 
index<-1
for (y in seq(1982,2014)){
  
  if (index == 1){
    file.path<-paste(folder.tmp,'/tmp',toString(y),'.tif',sep='')
    temp.rasters<-raster(file.path)
    proj.info<-projection(temp.rasters)
    xmin.val<-xmin(temp.rasters)
    xmax.val<-xmax(temp.rasters)
    ymin.val<-ymin(temp.rasters)
    ymax.val<-ymax(temp.rasters)    
    file.path<-paste(folder.pre,'/pre',toString(y),'.tif',sep='')
    pre.rasters<-raster(file.path) 
    file.path<-paste(folder.snow.vars,'/dfwos',toString(y),'.tif',sep='')
    dfws.rasters<-raster(file.path) 
    index<-index+1
    
    
  }else{
    file.path<-paste(folder.tmp,'/tmp',toString(y),'.tif',sep='')
    temp.rasters<-addLayer(temp.rasters,raster(file.path))
    file.path<-paste(folder.pre,'/pre',toString(y),'.tif',sep='')
    pre.rasters<-addLayer(pre.rasters,raster(file.path))
    file.path<-paste(folder.snow.vars,'/dfwos',toString(y),'.tif',sep='')
    dfws.rasters<-addLayer(dfws.rasters,raster(file.path))
    index<-index+1
    
  }
  
}

temp.array<-as.array(temp.rasters)
pre.array<-as.array(pre.rasters)
dfws.array<-as.array(dfws.rasters)

rows<-dim(temp.array)[1]
cols<-dim(temp.array)[2]

#--------------------------------------------------

sphere='nh'
for (fd in folderList)
{
  file.name<-basename(fd)
  outputPath22<-paste(outputPath2,'/',file.name,'/dwos',sep = '')
  if (! dir.exists(outputPath22)) {dir.create(outputPath22,recursive = TRUE)}
  if (file.exists(file.path(outputPath22,paste('dwos',as.character(2098),".tif",sep = ''))))
  {
    next
  }
  index<-1
  for (yr in seq(2015,2098))
  {
    full.path.t<-paste(fd,'/RCP85/tas_frozen_season_',sphere,'/tmp',as.character(yr),'.tif',sep = '')
    full.path.p<-paste(fd,'/RCP85/pr_frozen_season_',sphere,'/pr',as.character(yr),'.tif',sep = '')
    if (index==1)
    {
      newpre.ras<-raster(full.path.p)
      newtmp.ras<-raster(full.path.t)
      index<-index+1
    }else
    {
      newpre.ras<-addLayer(newpre.ras,raster(full.path.p))
      newtmp.ras<-addLayer(newtmp.ras,raster(full.path.t))
      index<-index+1
    }
  }
  newpre.arr<-as.array(newpre.ras)
  newtmp.arr<-as.array(newtmp.ras)
  
  # prediction
  lrt.arr<-matrix(data=-99,nrow = rows,ncol=cols)
  newx<-array(dim=dim(newtmp.arr))
  for (r in 1:rows){
    for (c in 1:cols){
      # length 
      temp.ts<-temp.array[r,c,]
      pre.ts<-pre.array[r,c,]
      dfws.ts<-dfws.array[r,c,]
      # print(dfws.ts)
      newtemp.ts<-newtmp.arr[r,c,]
      newpre.ts<-newpre.arr[r,c,]
      
      if (all(dfws.ts==-4) | all(dfws.ts==-3)| all(dfws.ts==-2)| all(dfws.ts==-1))
      {
        newx[r,c,]<-rep(unique(dfws.ts),time=dim(newtmp.arr)[3])
        lrt.arr[r,c]<-unique(dfws.ts)
        
      }else
      {
        if (sum(dfws.ts>=0)>length(dfws.ts)*0.9 & all(newtemp.ts>-99) & all(newpre.ts>=0))
        {
          se.conditions<-(temp.ts>-99) & (pre.ts>=0) & (dfws.ts>=0)
          
          
          
          if ((dfws.ts[12]>=0) & (dfws.ts[14]>=0))
          {
            dfws.ts[13]<-(dfws.ts[12]+dfws.ts[14])/2
          }else
          {
            dfws.ts[13]<-NA
          }
          dfws.ts[!se.conditions]<-NA
          
          # dfws.std=dfws.ts-mean(dfws.ts,na.rm=TRUE)/sd(dfws.ts,na.rm =TRUE)
          temp.ts[!se.conditions]<-NA
          
          pre.ts[!se.conditions]<-NA
          if (length(unique(pre.ts))<=2 | length(unique(temp.ts))<=2 |length(unique(dfws.ts))<=2){
            
            newx[r,c,]<-rep(-4,time=dim(newtmp.arr)[3])
            lrt.arr[r,c]<-(-4)
            next
          }
          
          mean.tem<-mean(c(temp.ts,newtemp.ts),na.rm = TRUE)
          sd.temp<-sd(c(temp.ts,newtemp.ts),na.rm = TRUE)
          tem<-(temp.ts-mean.tem)/sd.temp
          new.tem<-(newtemp.ts-mean.tem)/sd.temp
          
          mean.pre<-mean(c(pre.ts,newpre.ts),na.rm = TRUE)
          sd.pre<-sd(c(pre.ts,newpre.ts),na.rm = TRUE)
          pre<-(pre.ts-mean.pre)/sd.pre
          new.pre<-(newpre.ts-mean.pre)/sd.pre
          
          
          if (sum(abs(tem-pre),na.rm = TRUE)<1e-6){
            newx[r,c,]<-rep(-4,time=dim(newtmp.arr)[3]) 
            lrt.arr[r,c]<-(-4)
            next
          }        
          
          z.env <- arima(dfws.ts, order=c(1,0,0), xreg=cbind(tem, pre))
          z0.env <- arima(dfws.ts, order=c(1,0,0))
          preds<-predict(z.env, newxreg=cbind(new.tem, new.pre))$pred
          preds[preds<0]=0
          preds[preds>365]=365
          newx[r,c,]<- preds
          
          lrt.arr[r,c] <- 2*(logLik(z.env) - logLik(z0.env))
          
        } else
        {
          newx[r,c,]<-rep(-4,times=dim(newtmp.arr)[3])
          lrt.arr[r,c]<-(-4)
        }
      }
      
    }
    print(paste(file.name,':',r,sep=''))
  }
  
  lrt.arr[lrt.arr==--4]<-NA
  
  ras<-raster(lrt.arr,xmn=xmin.val,xmx=xmax.val,ymn=ymin.val,ymx=ymax.val,crs=proj.info)
  writeRaster(ras,filename=file.path(outputPath1,paste(file.name,".tif",sep = '')),format='GTiff',overwrite=TRUE)
  for (l in 1:dim(newx)[3])
  {
    ras<-raster(newx[,,l],xmn=xmin.val,xmx=xmax.val,ymn=ymin.val,ymx=ymax.val,crs=proj.info)
    writeRaster(ras,filename=file.path(outputPath22,paste('dwos',as.character(2014+l),".tif",sep = '')),format='GTiff',overwrite=TRUE)
  }
}

