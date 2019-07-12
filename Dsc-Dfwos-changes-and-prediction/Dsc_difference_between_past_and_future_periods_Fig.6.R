library(raster)
library(forecast)
setwd('E:/backup2/new_processing_12_30_2017')
rm(list=ls())

outputFolder<-'E:/backup2/new_processing_12_30_2017/statistical_analysis/difference_past_future'
if (! dir.exists(outputFolder)){dir.create(outputFolder)}
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

dws.array.past<-as.array(ras.stack)

dim.arr<-dim(dws.array.past)

mat.c<-matrix(-99,nrow=dim.arr[1],ncol = dim.arr[2])



# 2071-2098

# read snow cover variables

index<-1
for (y in seq(2071,2098))
{
  file.path<-paste(getwd(),'/prediction_dws_dwos/aggregation/dws_nh/','mean_dws',toString(y),'.tif',sep = '')
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

dws.array.future<-as.array(ras.stack)



mat.c<-matrix(-999,nrow=dim.arr[1],ncol = dim.arr[2])
arr_future<-c()
arr_current<-c()
arr_diff<-c()

for (r in 1:(dim.arr[1]))
{
  for (c in 1:(dim.arr[2]))
  {
    pixel.values1<-dws.array.past[r,c,]
    pixel.values2<-dws.array.future[r,c,]
    if (all(pixel.values1==-4) | all(pixel.values1==-3)| all(pixel.values1==-2)| all(pixel.values1==-1)){
      mat.c[r,c]<-unique(pixel.values1)*(1000)
    } else
    {
      if (sum(pixel.values1==0)>=15 ){
        mat.c[r,c]<-0
        
      } else
      {
        if (sum(pixel.values1>=0)>33*0.5 & sum(pixel.values2>=0)>28*0.5 ){
          

            ts1=pixel.values1[pixel.values1>=0]
            ts2=pixel.values2[pixel.values2>=0]
            arr_future<-c(arr_future,mean(ts2))
            arr_current<-c(arr_current,mean(ts1))
            
            diff=mean(ts2)-mean(ts1)
            var.res<-var.test(ts1,ts2)
            
            if (var.res$p.value<0.05){
              ttest<-t.test(ts1,ts2,var.equal = FALSE)
              if (ttest$p.value<0.05){
                mat.c[r,c]=diff
              }else
              {
                mat.c[r,c]=0
              }
            }else
            {
              ttest<-t.test(ts1,ts2,var.equal = TRUE)
              if (ttest$p.value<0.05){
                mat.c[r,c]=diff
              }else
              {
                mat.c[r,c]=0
              }              
            }
          
        } else
        {
          # test.arr<-pixel.values1
          pixel.values1<-pixel.values1[pixel.values1<0]
          if (length(pixel.values1)>0){
            mat.c[r,c]<-as.integer(names(sort(summary(as.factor(pixel.values1)),decreasing = T))[1])*(1000)
          }else
          {
            pixel.values2<-pixel.values2[pixel.values2<0]
            mat.c[r,c]<-as.integer(names(sort(summary(as.factor(pixel.values2)),decreasing = T))[1])*(1000)
          }
          
        }
      }
    }
    
  }
  
  print (r)  
}



future.ras<-raster(mat.c,xmn=xmin.val,xmx=xmax.val,ymn=ymin.val,ymx=ymax.val,crs=proj.info)
writeRaster(future.ras,filename=file.path(outputFolder,"dif_dws_nh_past_future.tif"),format='GTiff',overwrite=TRUE)

