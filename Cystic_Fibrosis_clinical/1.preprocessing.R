library(xlsx)
myData <- read.xlsx('CF Data.xlsx', 1)
unique(myData$DISCH_DISPSTN)

# data entry error
which(myData$DISCH_DISPSTN=='IVACAFTOR 150 MG TABLET')

# missing data
which(is.na(myData$BMI))

# remove these data
myData[c(168,432),]
myData.clean <- myData[-c(168,432),-1]

# transform to prescription data
myData.clean$PRES <- as.factor(pres.or + pres.and)
levels(myData.clean$PRES) <- c('None', 'Kalydeco', 'Orkambi')

# classify BMI types and add to data
bmi.class <- function(bmi) {
  if(bmi<18)
    return('under')
  else if (bmi>22)
    return('over')
  return('normal')
}
myData.clean$BMICLASS <- sapply(myData.clean$BMI, bmi.class)
myData.clean$BMICLASS <-  as.factor(myData.clean$BMICLASS)
head(myData.clean$BMICLASS)

# export data to file
write.csv(myData.clean, file='CF_Data_Cleaned.csv')
