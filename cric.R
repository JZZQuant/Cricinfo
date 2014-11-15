#get all data and format it and typecast it correctly
df.raw<-read.csv('Cricket.csv',stringsAsFactors=F)
df.all<-transform(df.raw,Player=as.factor(Player),Country=as.factor(gsub('([[:punct:]])|\\s+','',Country)),Inns=as.factor(Inns),Opposition=as.factor(Opposition),Ground=as.factor(Ground))
#cric info fucks up date time formatting
fault<-transform(df.all[2636:25724,],Start.Date=as.Date(Start.Date,"%d-%b-%y",origin = "1899-12-30"))$Start.Date
fault<-as.POSIXlt(fault)
fault$year<-fault$year-100
dates<-c(transform(df.all[1:2635,],Start.Date=as.Date(Start.Date,"%d %b %Y"))$Start.Date,
         as.Date(fault),
         transform(df.all[25725:85520,],Start.Date=as.Date(Start.Date,"%d-%b-%y",origin = "1899-12-30"))$Start.Date)

df.all<-transform(df.all,Start.Date=dates)
df.all<-transform(df.all,Minutes=as.numeric(gsub('([[:punct:]])|\\s+','',Minutes)))
df.all<-transform(df.all,Runs=as.numeric(gsub('([[:punct:]])|\\s+','',Runs)))
df.all<-transform(df.all,Balls.Faced=as.numeric(gsub('([[:punct:]])|\\s+','',Balls.Faced)))
df.all<-transform(df.all,Fours=as.numeric(gsub('([[:punct:]])|\\s+','',Fours)))
df.all<-transform(df.all,Sixes=as.numeric(df.all$Country<-as.factor(gsub('([[:punct:]])|\\s+','',df.raw$Country))
))
df.all<-transform(df.all,Strike.Rate=as.numeric(gsub('([[:punct:]])|\\s+','',Strike.Rate)))

#add new columns for important data lost during grepping
df.all$Not.Out=grepl('\\*$',df.raw$Runs)
df.all$DNB<-grepl('.*DNB.*',df.raw$Runs)
# uniform factoring throughout all columns
levels(df.all$Opposition)=levels(df.all$Country)

# unsupervised learning algo to figureout which city is in which country
venue<-lapply(levels(df.all$Ground),function(x) names(sort(table(subset(df.all,Ground==x)$Opposition)+table(subset(df.all,Ground==x)$Country),decreasing=T)[1]))
city.map<-cbind(City=levels(df.all$Ground),Venue=venue)

# find possible errors in ML algo above
lapply(levels(df.all$Ground),function(x) 
{
  y<-table(subset(df.all,Ground==x)$Opposition)+table(subset(df.all,Ground==x)$Country)
  if(y[[1]]==y[[2]])
  {
    #write(x,stdout())
  }
})

#set the city - country map manually where the machine learning algo couldnt figure out correctly
city.map[36,2]<-'Ban'
city.map[5,2]<-'Pak'
city.map[76,2]<-'SA'
city.map<-as.data.frame(city.map)

df.all$Venue<-as.factor(unlist(lapply(df.all$Ground,function(x) city.map[city.map$City==x,'Venue'][[1]])))
# reorder factors so that icc goes to the laast
df.all$Country<-factor(df.all$Country,levels(df.all$Country)[c(1:3,5:11,4)])
# reuse the county factor group for venue as well
levels(df.all$Venue)=levels(df.all$Country)
df.all$Home<-df.all$Country==df.all$Venue
#verify if the player is from subcontinent
df.all$SubC<-df.all$Country %in% levels(df.all$Country)[c(2,4,6,8)]
#verify if the venue being played is in subcontinent
df.all$VSubC<-df.all$Venue %in% levels(df.all$Country)[c(2,4,6,8)]
# generate random rows just to verify everything looks good
df.all[c(1,75,788,78878,5644,34345,34555),]

# get a smaller subset of major league players
players<-c('gavaskar','tendulkar','kallis','botham','lara','iva richards','dravid','ponting','laxman','sehwag','hanif','inzamam','bradman','sobers','border','hayden','dpmd jayawardene','sangakkara','md crowe')
players.id<-sapply(players,function(x) grep(x,tolower(as.character(levels(df.all$Player)))))
df.majorleague<-df.all[df.all$Player %in% levels(df.all$Player)[players.id],]

#now we are ready for actual analytics and plotting
require(ggplot2)
qplot(Player,data=df.majorleague,geom='bar',fill=Opposition,weight=Runs)
qplot(Player,data=df.majorleague,geom='bar',fill=Venue,weight=Runs)
qplot(Player,data=df.majorleague,geom='bar',fill=Venue==Opposition,weight=Runs)

qplot(Player,data=df.majorleague,geom='bar',fill=Opposition,facets=Venue~.,weight=Runs)
qplot(Player,data=df.majorleague,geom='bar',fill=Opposition,facets=Home~.,weight=Runs)
qplot(Player,data=df.majorleague,geom='bar',fill=Opposition,facets=SubC~VSubC,weight=Runs)

# let us see which venues are most easiset to score hundreds , the flat wicket myth
qplot(Venue,data=df.all[df.all$Runs>300 & !is.na(df.all$Runs),],geom='bar')
qplot(Venue,data=df.all[df.all$Runs>200 & !is.na(df.all$Runs),],geom='bar')

qplot(Venue,data=df.all[df.all$Runs>100 & !is.na(df.all$Runs),],geom='bar')
qplot(Venue,data=df.all[df.all$Runs>100 & !is.na(df.all$Runs) & df.all$Start.Date>"1959-01-01",],geom='bar')
qplot(Venue,data=df.all[df.all$Runs>100 & !is.na(df.all$Runs) & df.all$Start.Date>"1959-01-01" & df.all$Opposition==df.all$Venue,],geom='bar')

qplot(df.all$Start.Date,df.all$Runs)
#now a small unsupervised cluster algorithm to identify matches and batting orders

