# library('ppcor')
library('raster')


rm(list = ls())
# set the working directory

setwd('E:/backup2/new_processing_12_30_2017')

# folder for frozen season temperature
folder.tmp<-'./frozen_season_temp/nh_reclassified'
# folder for frozen season precipitation
folder.pre<-'./frozen_season_precip/nh_reclassified'
# folder for snow cover and freeze status variables
folder.snow.vars<-'./metrics_05degree_nh'

# output path
outputFolder<-'./statistical_analysis/revision_2/temp_precip_effects'
if (! file.exists(outputFolder)){
  dir.create(outputFolder)
  
}


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
year.len<-dim(temp.array)[3]
# correlation between temperature and dws, precip and dws, frozen season length and dws 
coef.temp<-matrix(data = -99,nrow = rows,ncol =cols)
coef.pre<-matrix(data=-99,nrow = rows,ncol=cols)
c.se.temp<-matrix(data=-99,nrow = rows,ncol=cols)
c.se.pre<-matrix(data=-99,nrow = rows,ncol=cols)
lrt.pre<-matrix(data=-99,nrow = rows,ncol=cols)
lrt.temp<-matrix(data=-99,nrow = rows,ncol=cols)
ratio.pre.temp<-matrix(data=-99,nrow = rows,ncol=cols)
coef.pre.temp.inter<-matrix(data=-99,nrow = rows,ncol=cols)
c.se.inter<-matrix(data=-99,nrow = rows,ncol=cols)

for (r in 1:rows){
  for (c in 1:cols){
    # length 
    temp.ts<-temp.array[r,c,]
    pre.ts<-pre.array[r,c,]
    dfws.ts<-dfws.array[r,c,]
    
    if (all(dfws.ts==-4) | all(dfws.ts==-3)| all(dfws.ts==-2)| all(dfws.ts==-1))
    {
      next
    }else
    {
      if (sum(dfws.ts>=0)>length(dfws.ts)*0.8)
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
          
          next
        }
        temp.std=(temp.ts-mean(temp.ts,na.rm=TRUE))/sd(temp.ts,na.rm = TRUE)
        precip.std=(pre.ts-mean(pre.ts,na.rm=TRUE))/sd(pre.ts,na.rm = TRUE)        
        
        if (sum(abs(precip.std-temp.std),na.rm = TRUE)<1e-6){
          next          
        }        
        
        z.env <- arima(dfws.ts, order=c(1,0,0), xreg=cbind(temp.std, precip.std))
        z0.env.temp <- arima(dfws.ts, order=c(1,0,0), xreg=precip.std)
        z0.env.precip <- arima(dfws.ts, order=c(1,0,0), xreg=temp.std)  
        coef.temp[r,c] <- z.env$coef[3]/sd(temp.ts,na.rm = TRUE)
        coef.pre[r,c] <- z.env$coef[4]/sd(pre.ts,na.rm = TRUE)
        c.se.temp[r,c] <- z.env$coef[3]/z.env$var.coef[3,3]^.5
        c.se.pre[r,c] <- z.env$coef[4]/z.env$var.coef[4,4]^.5
        lrt.temp[r,c] <- 2*(logLik(z.env) - logLik(z0.env.temp))
        lrt.pre[r,c] <- 2*(logLik(z.env) - logLik(z0.env.precip))
        ratio.pre.temp[r,c] <- (abs(z.env$coef[3])-abs(z.env$coef[4]))/(abs(z.env$coef[3])+abs(z.env$coef[4]))
        
        z.env.interaction <- arima(dfws.ts, order=c(1,0,0), xreg=cbind(temp.std, precip.std, temp.std*precip.std))
        coef.pre.temp.inter[r,c] <- z.env.interaction$coef[5]/z.env.interaction$var.coef[5,5]^.5 
        c.se.inter[r,c]<-z.env.interaction$coef[5]/z.env.interaction$var.coef[5,5]^.5
        
      } 
    }
    
  }
  print(r)
}




coef.temp.test<-matrix(data = -99,nrow = rows,ncol =cols)
coef.pre.test<-matrix(data=-99,nrow = rows,ncol=cols)

for (r in 1:rows){
  for (c in 1:cols){

    test.val.t<-c.se.temp[r,c]
    test.val.p<-c.se.pre[r,c]

    if ((test.val.t<2.04& test.val.t>(-2.04)) | is.na(test.val.t)){
      coef.temp.test[r,c]<-0
    } else
    {
      coef.temp.test[r,c]<-coef.temp[r,c]
    }


    if ((test.val.p<2.04 & test.val.p>(-2.04)) | is.na(test.val.p)){
      coef.pre.test[r,c]<-0
    } else
    {
      coef.pre.test[r,c]<-coef.pre[r,c]
    }


  }
}

ras<-raster(coef.temp.test,xmn=xmin.val,xmx=xmax.val,ymn=ymin.val,ymx=ymax.val,crs=proj.info)
writeRaster(ras,filename=file.path(outputFolder,"coef_temp_test_dwos_nh.tif"),format='GTiff',overwrite=TRUE)

# coef.pre<-coef.pre/10.0
ras<-raster(coef.pre.test,xmn=xmin.val,xmx=xmax.val,ymn=ymin.val,ymx=ymax.val,crs=proj.info)
writeRaster(ras,filename=file.path(outputFolder,"coef_pre_test_dwos_nh.tif"),format='GTiff',overwrite=TRUE)
