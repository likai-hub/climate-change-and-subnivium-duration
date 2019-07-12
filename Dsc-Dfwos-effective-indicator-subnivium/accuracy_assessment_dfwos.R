library(ggplot2)
# library(viridis)
library(hydroGOF) # rmse function
rm(list=ls())

output.folder<-'F:/projects/global_snow_frozen_project/avhrr_modis/new_processing_10_12_2017/in-situ/results_processing/assessment_mod_avh_seperate/'

if (! dir.exists(output.folder)){
  dir.create(output.folder)
}
setwd('F:/projects/global_snow_frozen_project/avhrr_modis/new_processing_10_12_2017/in-situ/results_processing')


# ghcn
data<-load('./assessment_mod_avh_seperate/ghcn_dwos.RData')
data.all<-data.frame(dataset=1,validation.df)
# china
data<-load('./assessment_mod_avh_seperate/china_dwos.RData')
data.all<-rbind(data.all,data.frame(dataset=2,validation.df))
# russia
data<-load('./assessment_mod_avh_seperate/russia_dwos.RData')
data.all<-rbind(data.all,data.frame(dataset=3,validation.df))
# snotel
data<-load('./assessment_mod_avh_seperate/snotel_dwos_simple.RData')
data.all<-rbind(data.all,data.frame(dataset=4,validation.df))

cor.all<-cor(data.all$stn,data.all$rs)
slope.all<-lm(rs~stn,data.all)$coefficients[2]

ggplot(data.all,aes(stn,rs))+
  geom_point(size=0.4)

lats<-unique(data.all$lat)
quantile(lats)
# (,40),(40,50),(50,)

data.40.less<-data.all[data.all$lat<=40,]
cor.40.less<-cor(data.40.less$stn,data.40.less$rs)
lm.40.less<-lm(rs~stn,data.40.less)$coefficients[2]

data.40.45<-data.all[(data.all$lat>40) & (data.all$lat<=45),]
cor.40.45<-cor(data.40.45$stn,data.40.45$rs)
lm.40.45<-lm(rs~stn,data.40.45)$coefficients[2]

data.45.50<-data.all[(data.all$lat>45) & (data.all$lat<=50),]
cor.45.50<-cor(data.45.50$stn,data.45.50$rs)
lm.45.50<-lm(rs~stn,data.45.50)$coefficients[2]

data.50.more<-data.all[(data.all$lat>50),]
cor.50.more<-cor(data.50.more$stn,data.50.more$rs)
lm.50.more<-lm(rs~stn,data.50.more)$coefficients[2]

c(cor.40.less,cor.40.45,cor.45.50,cor.50.more)
c(lm.40.less,lm.40.45,lm.45.50,lm.50.more)

rmse.40.less<-rmse(data.40.less$stn,data.40.less$rs)
rmse.40.45<-rmse(data.40.45$stn,data.40.45$rs)
rmse.45.50<-rmse(data.45.50$stn,data.45.50$rs)
rmse.50.more<-rmse(data.50.more$stn,data.50.more$rs)
c(rmse.40.less,rmse.40.45,rmse.45.50,rmse.50.more)
####################################################
# BY ELEVATION
# accuracy assessment by elevation (150,300,700)
# quantile(val.data$elev)

val.data.0.300<-data.all[(data.all$elev>=0)&(data.all$elev<=300),]
val.data.300.600<-data.all[(data.all$elev>300)&(data.all$elev<=600),]
val.data.600.900<-data.all[(data.all$elev>600)&(data.all$elev<=900),]
val.data.900.more<-data.all[(data.all$elev>900),]

# correlation
cor.0.300<-cor(val.data.0.300$stn,val.data.0.300$rs)
cor.300.600<-cor(val.data.300.600$stn,val.data.300.600$rs)
cor.600.900<-cor(val.data.600.900$stn,val.data.600.900$rs)
cor.900.more<-cor(val.data.900.more$stn,val.data.900.more$rs)
c(cor.0.300,cor.300.600,cor.600.900,cor.900.more)

# slope
lm.0.300<-lm(rs~stn,data=val.data.0.300)$coefficients[2]
lm.300.600<-lm(rs~stn,data=val.data.300.600)$coefficients[2]
lm.600.900<-lm(rs~stn,data=val.data.600.900)$coefficients[2]
lm.900.more<-lm(rs~stn,data=val.data.900.more)$coefficients[2]
c(lm.0.300,lm.300.600,lm.600.900,lm.900.more)

# RMSE
rmse.all<-rmse(data.all$rs,data.all$stn)
# other method: sqrt(mean((data.all$rs-data.all$stn)^2))
rmse.0.300<-rmse(val.data.0.300$stn,val.data.0.300$rs)
rmse.300.600<-rmse(val.data.300.600$stn,val.data.300.600$rs)
rmse.600.900<-rmse(val.data.600.900$stn,val.data.600.900$rs)
rmse.900.more<-rmse(val.data.900.more$stn,val.data.900.more$rs)

c(rmse.0.300,rmse.300.600,rmse.600.900,rmse.900.more,rmse.all)

####################################################
# BY LAND COVER
# accuracy assessment by land cover type

val.data.forest<-data.all[(data.all$land==1),]
val.data.grassland<-data.all[(data.all$land==2),]
val.data.cropland<-data.all[(data.all$land==3),]
val.data.barren<-data.all[(data.all$land==4),]

# 
# correlation
cor.forest<-cor(val.data.forest$stn,val.data.forest$rs)
cor.grassland<-cor(val.data.grassland$stn,val.data.grassland$rs)
cor.cropland<-cor(val.data.cropland$stn,val.data.cropland$rs)
cor.barren<-cor(val.data.barren$stn,val.data.barren$rs)
c(cor.forest,cor.grassland,cor.cropland,cor.barren)
# slope
slope.forest<-lm(rs~stn,data=val.data.forest)$coefficients[2]
slope.grassland<-lm(rs~stn,data=val.data.grassland)$coefficients[2]
slope.cropland<-lm(rs~stn,val.data.cropland)$coefficients[2]
slope.barren<-lm(rs~stn,val.data.barren)$coefficients[2]
c(slope.forest,slope.grassland,slope.cropland,slope.barren)
# rmse
rmse.forest<-rmse(val.data.forest$stn,val.data.forest$rs)
rmse.grassland<-rmse(val.data.grassland$stn,val.data.grassland$rs)
rmse.cropland<-rmse(val.data.cropland$stn,val.data.cropland$rs)
rmse.barren<-rmse(val.data.barren$stn,val.data.barren$rs)
c(rmse.forest,rmse.grassland,rmse.cropland,rmse.barren)
###################################################################
# mapping
###################################################################

# eatablish linear relationship

lm<-lm(rs~stn,data = data.all)

new.data<-data.frame(stn=seq(0,300,1))
fitted<-predict(lm,newdata = new.data)
fitted.df<-data.frame(fitx=seq(0,300,1),fity=fitted)

ref.line<-data.frame(refx=c(0,300),refy=c(0,300))


d <- densCols(data.all$stn,data.all$rs ,colramp = colorRampPalette(rev(rainbow(10, end = 4/6))))
p3 <- ggplot(data.all) + 
  
  geom_point(aes(stn, rs, col = d), pch=20,size = 0.6)+
  scale_color_identity() +
  scale_x_continuous(limits=c(0,300),breaks = seq(0,300,50),labels = as.character(seq(0,300,50)),expand = c(0, 0))+
  scale_y_continuous(limits=c(0,300),breaks = seq(0,300,50),labels = as.character(seq(0,300,50)),expand = c(0, 0))+
  geom_line(data=fitted.df,aes(x=fitx,y=fity),linetype=1,size=0.5)+
  geom_line(data=ref.line,aes(refx,refy),linetype='dashed',size=0.5)+
  xlab(expression(D[fwos]~(station-based)))+
  ylab(expression(D[fwos]~(remote~sensing-based)))+
  theme(panel.grid =element_blank())+
  theme(axis.line=element_line(color = 'black',size=0.5,linetype = 1))+
  theme(axis.text=element_text(color='black',size=7))+
  theme(axis.title=element_text(color='black',size=7))+
  theme(axis.ticks = element_line(color = 'black'))+
  theme(panel.background=element_rect(colour = 'black',linetype = 'solid',size=0.5,fill = 'white'))+
  # theme(panel.border = element_rect(fill = NULL,color='black',size=0.5))+
  # theme(panel.grid.major =element_line(color='white'),panel.grid.minor =element_line(color='white'))+
  annotate("text", label = "R=0.91, Slope=0.76", x = 80, y = 250, size = 2.5, colour = "black")

p3

output.filename<-paste(output.folder,'/all_datasets_dwos.tiff',sep = '')

tiff(file=output.filename,width=8,5,height=7,units='cm',res = 300)

plot(p3)
dev.off()

