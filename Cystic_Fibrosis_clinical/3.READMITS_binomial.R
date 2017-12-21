table(DISCH_DISPSTN, READMITS)

# these two DISCH_DISPSTN have most of the information
homeCare <- which(DISCH_DISPSTN=='Home Health Care Svc' | DISCH_DISPSTN=='Home or Self Care')

# try fitting binomial regression of DISCH_DISPSTN on IVACAFTOR and LUMICAFTOR
#fit <- glm(READMITS ~ IVACAFTOR + LUMICAFTOR, data=myData.clean, 
#           binomial(probit), subset=homeCare)
#summary(fit)

# other fits with binomial regression
#fit <- glm(READMITS ~ PRES + BMI + SOI + ROM + AGE + GENDER + RACE + ETHNICITY, 
#           family=binomial(probit), data=myData.clean, subset=homeCare)
#summary(fit)
#step(fit)

#fit <- glm(READMITS ~ PRES * BMI + PRES * SOI + PRES * ROM, data=myData.clean, 
#           family=binomial(probit), subset=homeCare)
#summary(fit)
#step(fit)

#fit <- glm(READMITS ~ PRES * SOI * ROM + AGE + BMI, data=myData.clean, 
#           family=binomial(probit), subset=homeCare)
#summary(fit)
#step(fit)

myData.clean$extendedStay <- myData.clean$LOS > 14
myData.clean$dummy <- myData.clean$DISCH_DISPSTN == levels(myData.clean$DISCH_DISPSTN)[6]
fit <- glm(READMITS ~ extendedStay + dummy + PRES + SOI + ROM + BMI, data=myData.clean,
  family=binomial(probit), subset=homeCare)
summary(fit)
nullFit <- glm(READMITS ~  SOI + ROM + BMI, data=myData.clean,
  family=binomial(probit), subset=homeCare)
R2 <- 1-logLik(fit)/logLik(nullFit)
R2
