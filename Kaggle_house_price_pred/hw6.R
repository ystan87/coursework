# default model is linear regression model
# change to rf for random forest
available.models <- c('lm','rf')
current.model <- available.models[1]

# Read data
HP <- read.csv('train.csv')
dim(HP)
names(HP)

# Explore for NA
hasNA <- apply(HP, 2, function(x) length(which(is.na(x))))
(hasNA <- hasNA[hasNA>0])

# Deduct misc value from sale price
HP$SalePrice <- HP$SalePrice - HP$MiscVal
HP <- HP[,-c(which(names(HP)=='MiscVal'))]

# Transform the response into logarithms
HP$SalePrice <- log(HP$SalePrice)

# Collect value for correction at a later point
missingBsmtExposure <- which(is.na(HP$BsmtExposure) & 
                               ! is.na(HP$BsmtQual) & 
                               ! is.na(HP$BsmtCond))

# Convert NA into factors
NAConvert <- c(
'Alley', 'BsmtQual', 'BsmtCond', 'BsmtExposure',
'BsmtFinType1', 'BsmtFinType2', 'FireplaceQu',
'GarageType', 'GarageFinish', 'GarageQual', 
'GarageCond', 'PoolQC', 'Fence', 'MiscFeature')
if (current.model=='lm') {
  for (e in NAConvert) { HP[[e]] <- sapply(HP[[e]], addNA) }
} else if (current.model=='rf') {
  for (e in NAConvert) {
    levels(HP[[e]]) <- c(levels(HP[[e]]), 'NA')
    HP[[e]][which(is.na(HP[[e]]))] <- 'NA'
  }
}

# Impute missing values
HP$LotFrontage[is.na(HP$LotFrontage)] <- median(HP$LotFrontage, na.rm=T)
HP$MasVnrArea[is.na(HP$MasVnrArea)] <- as.numeric(names(which.max(table(HP$MasVnrArea))))
HP$MasVnrType[is.na(HP$MasVnrType)] <- 'None'
HP$Electrical[is.na(HP$Electrical)] <- names(which.max(table(HP$Electrical)))
HP$GarageYrBlt[is.na(HP$GarageYrBlt)] <- mean(HP$GarageYrBlt, na.rm=T)

# Correct error values
HP$MasVnrArea[HP$MasVnrType=='None'] <- 0

# Convert to factors
nonFactors <- c(
'LotFrontage', 'LotArea', 'OverallCond', 'OverallQual',
'YearBuilt', 'YearRemodAdd', 
'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 
'TotalBsmtSF', 'X1stFlrSF', 'X2ndFlrSF', 'LowQualFinSF', 
'GrLivArea', 'BsmtFullBath', 'BsmtHalfBath', 'FullBath', 
'HalfBath', 'BedroomAbvGr', 'KitchenAbvGr', 'TotRmsAbvGrd', 
'Fireplaces', 'GarageYrBlt', 'GarageCars', 'GarageArea', 
'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', 'X3SsnPorch', 
'ScreenPorch', 'PoolArea', 'YrSold', 'MoSold', 'SalePrice')
assertthat::are_equal(length(nonFactors), dim(HP[,nonFactors])[2])
factorVars <- setdiff( names(HP), nonFactors)
HP[,factorVars] <- lapply(HP[,factorVars], function(x) as.factor(x))

# Merge month and year
HP$time <- (HP$YrSold-2006)*12 + HP$MoSold
# Drop Id column
HP <- HP[,-c(1, which(names(HP)=='YrSold'), which(names(HP)=='MoSold'))]

# linear regression model
if (current.model=='lm') {
  
# use all variables
HP.lm <- lm(SalePrice ~ . , data=HP)
anova(HP.lm)

# Main feature selection
HP.lm.AIC <- step(HP.lm)
anova(HP.lm.AIC)

FormOneWay <- 'SalePrice ~ 
MSSubClass + MSZoning + LotFrontage + LotArea + Street +
LotConfig + LandSlope + Neighborhood + Condition1 + Condition2 +
OverallQual + OverallCond + YearBuilt + YearRemodAdd + RoofMatl +
Exterior1st + MasVnrArea + ExterCond + Foundation + BsmtExposure +
BsmtFinSF1 + BsmtFinSF2 + BsmtUnfSF + Heating + HeatingQC +
CentralAir + X1stFlrSF + X2ndFlrSF + LowQualFinSF + BsmtFullBath +
FullBath + HalfBath + KitchenAbvGr + KitchenQual + Functional +
Fireplaces + GarageCars + GarageArea + GarageQual + GarageCond +
WoodDeckSF + EnclosedPorch + X3SsnPorch + ScreenPorch + PoolArea +
PoolQC + SaleType + SaleCondition'

# Selection of features of variable interactions
fit <- lm(SalePrice ~ MSSubClass * MSZoning, data=HP)
anova(step(fit))
FormMS <- 'MSSubClass:MSZoning'

fit <- lm(SalePrice ~ LotFrontage * LotConfig + LotArea * LotShape + 
            LotFrontage * Street + Street * Alley, data=HP)
anova(step(fit))
FormLot <- 'LotArea:LotShape'

fit <- lm(SalePrice ~  LotShape * LandContour * LandSlope, data=HP)
anova(step(fit))

fit <- lm(SalePrice ~ BldgType * HouseStyle * OverallQual * OverallCond * 
            YearBuilt * YearRemodAdd, data=HP)
anova(step(fit))
FormStyle <- 'BldgType:HouseStyle + BldgType:OverallQual + 
HouseStyle:OverallQual + BldgType:YearBuilt + BldgType:YearRemodAdd + 
YearBuilt:YearRemodAdd + BldgType:OverallCond:YearBuilt + 
BldgType:OverallCond:YearRemodAdd + 
OverallQual:OverallCond:YearBuilt:YearRemodAdd'

fit <- lm(SalePrice ~ RoofStyle * RoofMatl + 
            Exterior1st * ExterQual * ExterCond + 
            Exterior2nd * ExterQual * ExterCond + 
            MasVnrType * MasVnrArea * Foundation, 
          data=HP)
anova(step(fit))
FormExt <- 'ExterQual:Exterior2nd + ExterCond:Exterior2nd'

fit <- lm(SalePrice ~ Heating * HeatingQC * CentralAir, data=HP)
anova(step(fit))
FormHeat <- 'HeatingQC:CentralAir'

fit <- lm( SalePrice ~ (BsmtQual *BsmtCond * BsmtExposure + 
                          BsmtFinType1 : BsmtFinSF1 + 
                          BsmtFinType2 : BsmtFinSF2 + BsmtUnfSF) * 
             TotalBsmtSF, data=HP )
anova(step(fit))
FormBsmt <- 'BsmtQual:BsmtExposure + BsmtQual:TotalBsmtSF + 
BsmtExposure:TotalBsmtSF + BsmtQual:BsmtExposure:TotalBsmtSF + 
TotalBsmtSF:BsmtFinType1:BsmtFinSF1'

fit <- lm(SalePrice ~ X1stFlrSF * X2ndFlrSF * LowQualFinSF * GrLivArea, data=HP)
anova(step(fit))
FormInt <- 'X1stFlrSF:X2ndFlrSF + X1stFlrSF:GrLivArea + X2ndFlrSF:GrLivArea +
X1stFlrSF:X2ndFlrSF:LowQualFinSF + X1stFlrSF:X2ndFlrSF:LowQualFinSF:GrLivArea'

fit <- lm(SalePrice ~ BsmtFullBath * BsmtHalfBath * FullBath * HalfBath, data=HP)
anova(step(fit))
FormBath <- 'BsmtHalfBath:FullBath + FullBath:HalfBath'

fit <- lm(SalePrice ~ BedroomAbvGr * KitchenAbvGr * TotRmsAbvGrd + 
            KitchenAbvGr * KitchenQual, data=HP)
anova(step(fit))
FormRoom <- 'KitchenAbvGr:KitchenQual'

fit <- lm(SalePrice ~ FireplaceQu * Fireplaces, data=HP)
anova(step(fit))

# divide into two steps because too many variables involved
fit <- step(lm(SalePrice ~ (GarageType + GarageFinish + GarageQual +
                              GarageCond + PavedDrive)^3, data=HP))
# add the variable interactions from second step
fit <- step(lm(SalePrice ~ 
                 (GarageType + GarageFinish + GarageQual + GarageCond + 
                    PavedDrive) * (GarageYrBlt + GarageCars + GarageArea)^2 + 
                 (GarageType:GarageFinish + GarageType:GarageQual + 
                    GarageType:GarageCond + GarageType:PavedDrive + 
                    GarageFinish:PavedDrive + GarageQual:GarageCond + 
                    GarageQual:PavedDrive + GarageCond:PavedDrive) * 
                 (GarageYrBlt + GarageCars + GarageArea) + 
                 GarageQual:GarageCond:PavedDrive, data=HP))
anova(fit)
FormGarage <- 'GarageYrBlt:GarageCars + GarageYrBlt:GarageArea +
GarageType:GarageYrBlt + GarageType:GarageCars + GarageType:GarageArea +
GarageFinish:GarageCars + GarageQual:GarageCars + PavedDrive:GarageYrBlt +
GarageType:GarageQual + GarageType:PavedDrive + GarageQual:GarageCond +
GarageCond:GarageCars:GarageArea + GarageCond:PavedDrive:GarageArea'

fit <- lm(SalePrice ~ PoolArea * PoolQC, data=HP)
anova(step(fit))

fit <- lm(SalePrice ~ SaleType * SaleCondition, data=HP)
anova(step(fit))

formula <- paste(FormOneWay, FormMS, FormLot, FormStyle, FormExt, FormHeat, 
                 FormBsmt, FormInt, FormBath, FormRoom, FormGarage, 
                 sep=' + ')

HP.lm2 <- lm(formula=formula, data=HP)
HP.lm.AIC2 <- step(HP.lm2)
HP.lm.BIC2 <- step(HP.lm.AIC2, k=log(nrow(HP)))
# Tests show that BIC evaluates better than AIC on the test set
plot(HP.lm.BIC2)

# remove high leverage points to reduce overfitting
HP <- HP[-c(584, 667, 1004, 1231, 826, 524, 1299),]
HP.lm3 <- lm(formula=formula, data=HP)
HP.lm.BIC3 <- step(HP.lm3, k=log(nrow(HP)))

# detect multicollinearity
ali <- alias(HP.lm.BIC3)
dim(ali$Complete)
ali.data <- as.data.frame(ali$Complete)
row.names(ali.data)
for (i in 1:nrow(ali.data)) {
print(paste0('(', as.character(i), ',', as.character(which(ali.data[i,]!=0)), ')')) }
HP.lm.BIC3$coefficients[rownames(ali.data)]
# Their coefficients are NA, so they should not have any impact on the result.
trained.model <- HP.lm.BIC3
} else if (current.model=='rf') {
  # random forest model
  library(randomForest)
  library(performanceEstimation)
  res <- performanceEstimation(
    PredTask(SalePrice ~ . , HP, 'randomForest'),
    c(workflowVariants(learner='randomForest', 
                       learner.pars=list(ntree=c(200,500,1200)))),
    EstimationTask(metrics='rmse',method=CV(nReps=5,nFolds=10)))
  summary(res)
  rf <- randomForest(SalePrice ~ ., HP, ntree=1200)
  trained.model <- rf
}

# Evaluation on trained data set, not an objective measure
preds.train <- predict(trained.model, HP)
( rmse.lm.train <- sqrt(mean((preds.train-HP$SalePrice)^2)) ) 


# Read test data
HPTest <- read.csv('test.csv')

# Preprocess test data
hasNATest <- apply(HPTest, 2, function(x) length(which(is.na(x))))
(hasNATest <- hasNATest[hasNATest>0])

NAConvert <- c(
  'Alley', 'BsmtQual', 'BsmtCond', 'BsmtExposure',
  'BsmtFinType1', 'BsmtFinType2', 'FireplaceQu',
  'GarageType', 'GarageFinish', 'GarageQual', 
  'GarageCond', 'PoolQC', 'Fence', 'MiscFeature')
if (current.model=='lm') {
  for (e in NAConvert) { HP[[e]] <- sapply(HP[[e]], addNA) }
  # Impute for removed data
  HPTest$Functional[HPTest$Functional=='Sev'] <-
    names(which.max(table(HP$Functional)))
} else if (current.model=='rf') {
  for (e in NAConvert) {
    levels(HPTest[[e]]) <- c(levels(HPTest[[e]]), 'NA')
    HPTest[[e]][which(is.na(HPTest[[e]]))] <- 'NA'
  }
}

HPTest[,factorVars] <- lapply(HPTest[,factorVars], function(x) as.factor(x))

# Merge month and year
HPTest$time <- (HPTest$YrSold-2006)*12 + HPTest$MoSold

# Impute missing values
HPTest$MSZoning[is.na(HPTest$MSZoning)] <- names(which.max(table(HPTest$MSZoning)))
HPTest$LotFrontage[is.na(HPTest$LotFrontage)] <- median(HPTest$LotFrontage, na.rm=T)
HPTest$Utilities[is.na(HPTest$Utilities)] <- names(which.max(table(HPTest$Utilities)))
HPTest$Exterior1st[is.na(HPTest$Exterior1st)] <- names(which.max(table(HPTest$Exterior1st)))
HPTest$Exterior2nd[is.na(HPTest$Exterior2nd)] <- names(which.max(table(HPTest$Exterior2nd)))
HPTest$MasVnrArea[is.na(HPTest$MasVnrArea)] <- as.numeric(names(which.max(table(HPTest$MasVnrArea))))
HPTest$MasVnrType[is.na(HPTest$MasVnrType)] <- 'None'
HPTest$BsmtFinSF1[is.na(HPTest$BsmtFinSF1)] <- 0
HPTest$BsmtFinSF2[is.na(HPTest$BsmtFinSF2)] <- 0
HPTest$BsmtUnfSF[is.na(HPTest$BsmtUnfSF)] <- 0
HPTest$TotalBsmtSF[is.na(HPTest$TotalBsmtSF)] <- 0
HPTest$BsmtFullBath[is.na(HPTest$BsmtFullBath)] <- 0
HPTest$BsmtHalfBath[is.na(HPTest$BsmtHalfBath)] <- 0
HPTest$Electrical[is.na(HPTest$Electrical)] <- names(which.max(table(HPTest$Electrical)))
HPTest$KitchenQual[is.na(HPTest$KitchenQual)] <- names(which.max(table(HPTest$KitchenQual)))
HPTest$Functional[is.na(HPTest$Functional)] <- names(which.max(table(HPTest$Functional)))
HPTest$GarageYrBlt[is.na(HPTest$GarageYrBlt)] <- mean(HPTest$GarageYrBlt, na.rm=T)
HPTest$GarageCars[is.na(HPTest$GarageCars)] <- 0
HPTest$GarageArea[is.na(HPTest$GarageArea)] <- 0
HPTest$SaleType[is.na(HPTest$SaleType)] <- names(which.max(table(HPTest$SaleType)))

# Unseen factor, use mode imputation
HPTest$MSSubClass[!HPTest$MSSubClass %in% levels(HP$MSSubClass)] <- 
  names(which.max(table(HP$MSSubClass)))

# Prediction
preds <- exp(predict(trained.model, HPTest)) + HPTest$MiscVal

# output results to file
res <- data.frame('Id'=HPTest$Id, 'SalePrice'=preds)
write.csv(res, file='submission.csv', row.names=F)

