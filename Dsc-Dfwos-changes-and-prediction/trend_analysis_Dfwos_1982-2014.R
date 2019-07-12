library(raster)
library(forecast)
setwd('E:/backup2/new_processing_12_30_2017')
rm(list=ls())

# read snow cover variables

index<-1
for (y in seq(1982,2014))
{
  file.path<-paste(getwd(),'/avhrr_82_07_mod_02_08_14_nh/','dfwos',toString(y),'.tif',sep = '')
  ras.obj<-raster(file.path)
  if (index==1) 
  {
    proj.info<-projection(ras.obj)
    xmin.val<-xmin(ras.obj)
    xmax.val<-xmax(ras.obj)
    ymin.val<-ymin(ras.obj)
    ymax.val<-ymax(ras.obj)
    ras.stack<-stack(ras.obj)
    index<-index+1
  } else
  {
    ras.stack<-addLayer(ras.stack,ras.obj)
    index<-index+1
  }
}

dws.array<-as.array(ras.stack)

dim.arr<-dim(dws.array)

mat.c<-matrix(-99,nrow=dim.arr[1],ncol = dim.arr[2])
mat.lrt<-matrix(-99,nrow=dim.arr[1],ncol = dim.arr[2])
mat.c.se<-matrix(-99,nrow=dim.arr[1],ncol = dim.arr[2])
mat.c.test<-matrix(-99,nrow=dim.arr[1],ncol = dim.arr[2])
time <- 1:33
time <- (time-mean(time))/sd(time)

for (r in 1:(dim.arr[1]))
{
  for (c in 1:(dim.arr[2]))
  {
    pixel.values<-dws.array[r,c,]
    if (all(pixel.values==-4) | all(pixel.values==-3)| all(pixel.values==-2)| all(pixel.values==-1)){
      next
    } else
    {
      if (sum(pixel.values==0)>=20 ){
        mat.c[r,c]<-0
        mat.lrt[r,c]<-0
        mat.c.se[r,c]<-0
        mat.c.test[r,c]<-0
      } else
      {
        if (sum(pixel.values>=0)>32*0.8 ){
          # predict the value for 1994
          
            if ((pixel.values[12]>=0) & (pixel.values[14]>=0))
            {
              pixel.values[13]<-(pixel.values[12]+pixel.values[14])/2
            }else
            {
              pixel.values[13]<-NA
            }
            pixel.values[pixel.values<0]<-NA
            # if all elements are the same, there will be some errors
            if (length(unique(pixel.values))<=2){
              mat.c[r,c]<-0
              mat.c.se[r,c]<-0
              mat.lrt[r,c]<-0
              mat.c.test[r,c]<-0
              
              next
            }  
        
          z <- arima(pixel.values, order=c(1,0,0), xreg=time)
          mat.c[r,c]<-z$coef[3]/sd(1:33)
          cse.val<-z$coef[3]/(z$var.coef[3,3]^.5)
          mat.c.se[r,c]<-cse.val
          z0<-arima(pixel.values, order=c(1,0,0))
          mat.lrt[r,c] <- 2*(logLik(z) - logLik(z0))  
          
          
          if (is.na(cse.val) | (cse.val>(-2.04) & cse.val<2.04)){
            mat.c.test[r,c]<-0
            
          } else
          {
            mat.c.test[r,c]<-z$coef[3]/sd(1:33)
          }

        } else
        {
          next
        }
      }
    }
    
  }
  print(r)

}
# mat.c[mat.c==-99]<-NA
# mat.c.se[mat.c.se==-99]<-NA
# mat.lrt[mat.lrt==-99]<-NA

outputFolder<-'E:/backup2/new_processing_12_30_2017/statistical_analysis/trend_results_revision2'
if (! dir.exists(outputFolder)){dir.create(outputFolder)}

# save matrix to raster
# slope
c.ras<-raster(mat.c,xmn=xmin.val,xmx=xmax.val,ymn=ymin.val,ymx=ymax.val,crs=proj.info)
writeRaster(c.ras,filename=file.path(outputFolder,"slp_dwos_nh.tif"),format='GTiff',overwrite=TRUE)
# C/SE(C)
c.se.ras<-raster(mat.c.se,xmn=xmin.val,xmx=xmax.val,ymn=ymin.val,ymx=ymax.val,crs=proj.info)
writeRaster(c.se.ras,filename=file.path(outputFolder,"c_se_dwos_nh.tif"),format='GTiff',overwrite=TRUE)

# Likelihood ratio test
lrt.ras<-raster(mat.lrt,xmn=xmin.val,xmx=xmax.val,ymn=ymin.val,ymx=ymax.val,crs=proj.info)
writeRaster(lrt.ras,filename=file.path(outputFolder,"lrt_dwos_nh.tif"),format='GTiff',overwrite=TRUE)

slope.ras<-raster(mat.c.test,xmn=xmin.val,xmx=xmax.val,ymn=ymin.val,ymx=ymax.val,crs=proj.info)
writeRaster(slope.ras,filename=file.path(outputFolder,"slope_dwos_nh.tif"),format='GTiff',overwrite=TRUE)



mat.c.sig<-matrix(-99,nrow=dim.arr[1],ncol = dim.arr[2])

for (r in 1:(dim.arr[1]))
{
  for (c in 1:(dim.arr[2]))
  {
    test.val<-mat.c.se[r,c]
    if ((test.val<2.04 & test.val>(-2.04)) | is.na(test.val) )
    {
      mat.c.sig[r,c]<-0
    }else
    {
      mat.c.sig[r,c]<-mat.c[r,c]
    }
  }
}

slope.ras.sig<-raster(mat.c.sig,xmn=xmin.val,xmx=xmax.val,ymn=ymin.val,ymx=ymax.val,crs=proj.info)
writeRaster(slope.ras.sig,filename=file.path(outputFolder,"slope_dwos_nh_sig.tif"),format='GTiff',overwrite=TRUE)


