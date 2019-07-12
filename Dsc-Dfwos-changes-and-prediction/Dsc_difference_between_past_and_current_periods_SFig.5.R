library(raster)
library(forecast)
setwd('E:/backup2/new_processing_12_30_2017')
rm(list=ls())

# read snow cover variables

index<-1
for (y in seq(1982,2014))
{
  file.path<-paste(getwd(),'/metrics_05degree_nh/','dfws',toString(y),'.tif',sep = '')
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

# mat.cur<-matrix(-99,nrow=dim.arr[1],ncol = dim.arr[2])
# mat.past<-matrix(-99,nrow=dim.arr[1],ncol = dim.arr[2])

mat.diff<-matrix(-999,nrow=dim.arr[1],ncol = dim.arr[2])
curr_dsc<-c()
past_dsc<-c()

# time <- 1:33
# time <- (time-mean(time))/sd(time)

for (r in 1:(dim.arr[1]))
{
  for (c in 1:(dim.arr[2]))
  {
    # 1982-1986
    pixel.values<-dws.array[r,c,1:5]
    # pixel.values2<-dws.array[r,c,29:33]
    if (all(pixel.values==-4) | all(pixel.values==-3)| all(pixel.values==-2)| all(pixel.values==-1)){
      past.val<-unique(pixel.values)
    } else
    {
      if (sum(pixel.values>=0)>=1 ){
        pixel.values[pixel.values<0]<-NA
        past.val<-mean(pixel.values,na.rm = TRUE)
        
      } else
      {
        pixel.values<-pixel.values[pixel.values<0]
        past.val<-as.integer(names(sort(summary(as.factor(pixel.values)),decreasing = T))[1])
      }
    }
    
    pixel.values<-dws.array[r,c,29:33]
    if (all(pixel.values==-4) | all(pixel.values==-3)| all(pixel.values==-2)| all(pixel.values==-1)){
      cur.val<-unique(pixel.values)
    } else
    {
      if (sum(pixel.values>=0)>=1 ){
        pixel.values[pixel.values<0]<-NA
        cur.val<-mean(pixel.values,na.rm = TRUE)
        
      } else
      {
        pixel.values<-pixel.values[pixel.values<0]
        cur.val<-as.integer(names(sort(summary(as.factor(pixel.values)),decreasing = T))[1])
      }
    }
    
    if (cur.val<0 | past.val<0){
      mat.diff[r,c]<-min(c(cur.val,past.val))*(1000)
    }else
    {
      mat.diff[r,c]<-cur.val-past.val
      curr_dsc<-c(curr_dsc,cur.val)
      past_dsc<-c(past_dsc,past.val)
    }
    
    
  }
  
  
  print (r)  
}


# mat.c[mat.c==-99]<-NA
# mat.c.se[mat.c.se==-99]<-NA
# mat.lrt[mat.lrt==-99]<-NA

outputFolder<-'E:/backup2/new_processing_12_30_2017/statistical_analysis/difference_past_cur'
if (! dir.exists(outputFolder)){dir.create(outputFolder)}

c.ras<-raster(mat.diff,xmn=xmin.val,xmx=xmax.val,ymn=ymin.val,ymx=ymax.val,crs=proj.info)
writeRaster(c.ras,filename=file.path(outputFolder,"dif_dws_nh82_14.tif"),format='GTiff',overwrite=TRUE)


