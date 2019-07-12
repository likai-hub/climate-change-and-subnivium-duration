library(ggplot2)


#************************************************************************************************
# Multiple plot function
#
# ggplot objects can be passed in ..., or to plotlist (as a list of ggplot objects)
# - cols:   Number of columns in layout
# - layout: A matrix specifying the layout. If present, 'cols' is ignored.
#
# If the layout is something like matrix(c(1,2,3,3), nrow=2, byrow=TRUE),
# then plot 1 will go in the upper left, 2 will go in the upper right, and
# 3 will go all the way across the bottom.
#
multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  library(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}

#************************************************************************************************


rm(list = ls())
setwd('E:/backup2/revision-results')

ds.lats<-read.csv('zonal_stats_lats_4.27_2019.txt',header = TRUE)

ds.dws.lats<-ds.lats[c(7,8,5),2:6]

vec.dws.lats<-as.vector(as.matrix(ds.dws.lats))

df.dws.lats<-data.frame(v=vec.dws.lats,periods=rep(c('1982-1986','2010-2014','2071-2100'),times=5),lats=rep(c('1','2','3','4','5'),each=3))


p1<-ggplot(df.dws.lats,aes(lats,v))+
  geom_bar(stat = 'identity',aes(fill=periods),position='dodge')+
  
  scale_fill_manual("legend", values = c("#a6bddb",  "#3690c0",  "#045a8d"))+
  # scale_fill_manual("legend", values = c("#252525",  "#969696",  "#d9d9d9"))+
  scale_x_discrete(labels = c('<40','40~50','50~60','>60','Global'))+
  scale_y_continuous(limits=c(0,225),breaks=seq(0,225,25),labels = c(0,"",50,"",100,"",150,"",200,""),expand = c(0,0))+
  # xlab(expression(paste('Latitude (',''^{o},')',sep="")))+
  ylab('Dsc(days)')+
  theme(panel.grid =element_blank())+
  # theme(panel.background=element_rect(colour = 'black',linetype = 'solid',fill = 'white'))  +
  # theme(axis.line=element_line(color = 'black',linetype = 1,size=0.4))+
  theme(axis.text=element_text(color='black',size=7))+
  theme(axis.title.y =element_text(color='black',size=7))+
  theme(axis.title.x =element_blank())+
  # theme(axis.ticks = element_line(color = 'black',size=0.4))+
  # theme(panel.background=element_rect(colour = 'black',linetype = 'solid',fill = 'white'))  +
  theme(legend.position = c(0.21,0.78))+
  theme(legend.text=element_text(size=6))+
  theme(legend.key.size = unit(0.55,"line"))+
  theme(legend.title = element_blank())+
  theme(axis.ticks = element_line(color = 'black',size=0.4))+
  
  theme(axis.line=element_line(color = 'black',linetype = 1,size = 0.4))+
  theme(panel.background=element_rect(colour = 'black',fill='white',size=0.4))


p1



ds.dwos.lats<-ds.lats[c(3,4,1),2:6]

vec.dwos.lats<-as.vector(as.matrix(ds.dwos.lats))

df.dwos.lats<-data.frame(v=vec.dwos.lats,periods=rep(c('1982-1986','2010-2014','2071-2100'),times=5),lats=rep(c('1','2','3','4','5'),each=3))

df.l1<-data.frame(x=c(2.5,2.5),y=c(0,50))

p2<-ggplot(df.dwos.lats,aes(lats,v))+
  geom_bar(stat = 'identity',aes(fill=periods),position='dodge')+
  geom_segment(aes(x=1.5,xend=2.5,y=50,yend=50),linetype='dashed',size=0.3)+
  geom_segment(aes(x=1.5,xend=1.5,y=0,yend=50),linetype='dashed',size=0.3)+
  geom_segment(aes(x=2.5,xend=2.5,y=0,yend=50),linetype='dashed',size=0.3)+
  # geom_vline(xintercept=1.5,linetype='dashed',size=0.3)+
  # geom_hline(yintercept=50,linetype='dashed',size=0.3)+
  scale_fill_manual("legend", values = c("#a6bddb",  "#3690c0",  "#045a8d"))+
  scale_x_discrete(labels = c('<40','40~50','50~60','>60','Global'))+
  scale_y_continuous(limits=c(0,90),breaks=seq(0,90,10),labels = c(0,"","",30,"","",60,"","",90),expand = c(0,0))+
  xlab(expression(paste('Latitude (',''^{o},')',sep="")))+
  ylab('Dfwos(days)')+
  theme(panel.grid =element_blank())+
  
  # theme(axis.line=element_line(color = 'black',linetype = 1,size=0.4))+
  theme(axis.text=element_text(color='black',size=7))+
  theme(axis.title=element_text(color='black',size=7))+
  # theme(axis.ticks = element_line(color = 'black',size=0.4))+
  theme(axis.ticks = element_line(color = 'black',size=0.4))+
  
  theme(axis.line=element_line(color = 'black',linetype = 1,size = 0.4))+
  theme(panel.background=element_rect(colour = 'black',fill='white',size=0.4))  +
  theme(legend.position="none")

p2

### by elevation

ds.elev<-read.csv('zonal_stats_by_dem_4.27.2019.txt',header = TRUE)

ds.dws.elev<-ds.elev[c(7,8,5),2:5]

vec.dws.elev<-as.vector(as.matrix(ds.dws.elev))

df.dws.elev<-data.frame(v=vec.dws.elev,periods=rep(c('1982-1986','2010-2014','2071-2100'),times=4),elev=rep(c('1','2','3','4'),each=3))


p3<-ggplot(df.dws.elev,aes(elev,v))+
  geom_bar(stat = 'identity',aes(fill=periods),position='dodge')+
  scale_fill_manual("legend", values = c("#a6bddb",  "#3690c0",  "#045a8d"))+
  scale_x_discrete(labels = c('<300','300~600','600~900','>900'))+
  scale_y_continuous(limits=c(0,175),breaks=seq(0,175,25),labels = c(0,"",50,"",100,"",150,""),expand = c(0,0))+
  # xlab(expression(paste('Latitude (',''^{o},')',sep="")))+
  ylab('')+
  theme(panel.grid =element_blank())+
  # theme(panel.background=element_rect(colour = 'black',linetype = 'solid',fill = 'white'))  +
  # theme(axis.line=element_line(color = 'black',linetype = 1,size=0.4))+
  theme(axis.text=element_text(color='black',size=7))+
  theme(axis.title.y =element_text(color='black',size=7))+
  theme(axis.title.x =element_blank())+
  theme(axis.ticks = element_line(color = 'black',size=0.4))+
  
  theme(axis.line=element_line(color = 'black',linetype = 1,size = 0.4))+
  theme(panel.background=element_rect(colour = 'black',fill='white',size=0.4))  +
  theme(legend.position = "none")

p3

ds.dwos.elev<-ds.elev[c(3,4,1),2:5]

vec.dwos.elev<-as.vector(as.matrix(ds.dwos.elev))

df.dwos.elev<-data.frame(v=vec.dwos.elev,periods=rep(c('1982-1986','2010-2014','2071-2100'),times=4),elev=rep(c('1','2','3','4'),each=3))

p4<-ggplot(df.dwos.elev,aes(elev,v))+
  geom_bar(stat = 'identity',aes(fill=periods),position='dodge')+
  scale_fill_manual("legend", values = c("#a6bddb",  "#3690c0",  "#045a8d"))+
  scale_x_discrete(labels = c('<300','300~600','600~900','>900'))+
  scale_y_continuous(limits=c(0,70),breaks=seq(0,70,10),labels = c(0,"",20,"",40,"",60,""),expand = c(0,0))+
  xlab("Elevation (m)")+
  ylab('')+
  theme(panel.grid =element_blank())+
  # theme(axis.line=element_line(color = 'black',size=0.4,linetype = 1))+
  theme(axis.text=element_text(color='black',size=7))+
  theme(axis.title.y =element_text(color='black',size=7))+
  theme(axis.title.x =element_text(color='black',size=7))+
  theme(axis.ticks = element_line(color = 'black',size=0.4))+
  
  theme(axis.line=element_line(color = 'black',linetype = 1,size = 0.4))+
  theme(panel.background=element_rect(colour = 'black',fill='white',size=0.4))  +
  theme(legend.position = "none")

p4

### by land cover

ds.land<-read.csv('zonal_stats_by_landcover1.11.2018.txt',header = TRUE)

ds.dws.land<-ds.land[c(7,8,5),2:5]

vec.dws.land<-as.vector(as.matrix(ds.dws.land))

df.dws.land<-data.frame(v=vec.dws.land,periods=rep(c('1982-1986','2010-2014','2071-2100'),times=4),land=rep(c('1','2','3','4'),each=3))



p5<-ggplot(df.dws.land,aes(land,v))+
  geom_bar(stat = 'identity',aes(fill=periods),position='dodge')+
  scale_fill_manual("legend", values = c("#a6bddb",  "#3690c0",  "#045a8d"))+
  scale_x_discrete(labels = c('forest','grassland','cropland','barren'))+
  scale_y_continuous(limits=c(0,175),breaks=seq(0,175,25),labels = c(0,"",50,"",100,"",150,""),expand = c(0,0))+
  # xlab(expression(paste('Latitude (',''^{o},')',sep="")))+
  ylab('')+
  theme(panel.grid =element_blank())+
  # theme(axis.line=element_line(color = 'black',size=0.4,linetype = 1))+
  theme(axis.text=element_text(color='black',size=7))+
  theme(axis.title.y =element_text(color='black',size=7))+
  theme(axis.title.x =element_blank())+
  theme(axis.ticks = element_line(color = 'black',size=0.4))+
  
  theme(axis.line=element_line(color = 'black',linetype = 1,size = 0.4))+
  theme(panel.background=element_rect(colour = 'black',fill='white',size=0.4))  +
  theme(legend.position = "none")

p5


ds.dwos.land<-ds.land[c(3,4,1),2:5]

vec.dwos.land<-as.vector(as.matrix(ds.dwos.land))

df.dwos.land<-data.frame(v=vec.dwos.land,periods=rep(c('1982-1986','2010-2014','2071-2100'),times=4),land=rep(c('1','2','3','4'),each=3))



p6<-ggplot(df.dwos.land,aes(land,v))+
  geom_bar(stat = 'identity',aes(fill=periods),position='dodge')+
  scale_fill_manual("legend", values = c("#a6bddb",  "#3690c0",  "#045a8d"))+
  scale_x_discrete(labels = c('forest','grassland','cropland','barren'))+
  scale_y_continuous(limits=c(0,125),breaks=seq(0,125,25),labels = seq(0,125,25),expand = c(0,0))+
  xlab("Land-cover type")+
  ylab('')+
  theme(panel.grid =element_blank())+
  # theme(axis.line=element_line(color = 'black',linetype = 1,size = 0.4))+
  theme(axis.text=element_text(color='black',size=7))+
  theme(axis.title.y =element_text(color='black',size=7))+
  theme(axis.title.x =element_text(color='black',size=7))+
  theme(axis.ticks = element_line(color = 'black',size=0.4))+
  
  theme(axis.line=element_line(color = 'black',linetype = 1,size = 0.4))+
  theme(panel.background=element_rect(colour = 'black',fill='white',size=0.4))  +
  theme(legend.position = "none")

p6

output.filename<-'C:/Users/lzhu68/Desktop/revision-2/test2.tiff'
tiff(file=output.filename,width=17.8,height=8,units='cm',res = 300)
ps<-multiplot(p1, p2, p3,p4,p5,p6,cols=3)


print(ps)
dev.off()


