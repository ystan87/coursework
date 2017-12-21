library(MASS)

myData.revise <- myData.clean[myData.clean$LOS>14,]
nrow(myData.revise)
fit <- glm(LOS-14 ~ BMI + SOI + ROM, data=myData.revise)
boxcox(fit)
hist(log(myData.revise$LOS-14))
myData.revise$logLOS <- log(myData.revise$LOS-14)
fit <- glm(logLOS ~ BMI + SOI + ROM, data=myData.revise)
fit$coefficients

#nullFit <- glm(logLOS ~ 1, data=myData.revise)
#R2 <- 1-logLik(fit)/logLik(nullFit)
#R2
plot(fit)

# KS, Shapiro, and  test show goodness-of-fit with normality plot
distTest <- fit$residuals
#refTest <- rnorm(n=30000, mean=mean(distTest), sd=sd(distTest))
#ks.test(distTest, refTest, alternative='two.sided')
shapiro.test(distTest)
library(nortest)
ad.test(distTest)

library(ggplot2)
ggplot(data.frame(x=distTest), aes(x)) + stat_ecdf(geom='step', col='red') +
  stat_function(fun = pnorm, n=100, args=list(mean=mean(distTest), sd=sd(distTest))) +
  scale_y_continuous(breaks=NULL) +
  geom_hline( yintercept=1, lty=2) + geom_hline( yintercept=0, lty=2) +
  ggtitle('ECDF plot of residuals for Length of Stay over 14') +
  ylab('Residue of log(Length of Stay - 14)') + xlab('Normally distributed values')
