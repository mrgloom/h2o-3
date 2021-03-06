####### This tests weights in deeplearning for tweedie by comparing results with expected behaviour  ######

setwd(normalizePath(dirname(R.utils::commandArgs(asValues=TRUE)$"f")))
source('../../h2o-runit.R')

test <- function(h) {

	data = read.csv(file =locate("smalldata/glm_test/cancar_logIn.csv"),header = T)
	data$Merit <- factor(data$Merit)
	data$Class <- factor(data$Class)
	data$C1M3 <-factor(data$Class == 1 & data$Merit == 3 )
	data$C3M3 <-factor(data$Class == 3 & data$Merit == 3 )
	data$C4M3 <-factor(data$Class == 4 & data$Merit == 3 )
	data$C1M2 <-factor(data$Class == 1 & data$Merit == 2 )
	Loss = data$Cost/data$Insured
	data = data.frame(Loss,data)
	cancar = as.h2o(data,destination_frame = "cancar")
	
	#Expect deviance to be better for model with weights
	
	#Without weights
	#library(gbm)
	#gg = gbm(formula = Loss~Class+Merit + C1M3 + C4M3, distribution = "tweedie",data = data,
      #   n.trees = 50,interaction.depth = 1,n.minobsinnode = 1,shrinkage = 1,bag.fraction = 1,
      #  train.fraction = 1,verbose=T)
	#gg$train.error  #0.0009
	#pr = predict(gg,newdata = data,type = "response")# mean = 0.04420; min = 0.02292; max = 0.07156; 
	myX = c( "Merit", "Class","C1M3","C4M3")
	hh = h2o.deeplearning(x = myX,y = "Loss",distribution ="tweedie",hidden = c(1),epochs = 1000,train_samples_per_iteration = -1,
                      reproducible = T,activation = "Tanh",balance_classes = F,force_load_balance = F,
                      seed = 2353123,tweedie_power = 1.5,score_training_samples = 0,score_validation_samples = 0,
                      training_frame = cancar) 

	mean_deviance = hh@model$training_metrics@metrics$mean_residual_deviance
	expect_equal(mean_deviance,0.001300774016)
	ph = as.data.frame(h2o.predict(hh,newdata = cancar)) 
	expect_equal(0.04422983122, mean(ph[,1]) )
	expect_equal(0.02490190401, min(ph[,1]) )
	expect_equal(0.07329475487, max(ph[,1]) )
	
	#With weights
	#gg = gbm(formula = Loss~Class+Merit + C1M3 + C4M3, distribution = "tweedie",data = data,
      #   n.trees = 50,interaction.depth = 1,n.minobsinnode = 1,shrinkage = 1,bag.fraction = 1,
      #   weights = data$Insured,train.fraction = 1,verbose=T)
	#gg$train.error  #0.0001  
	#pr = predict(gg,newdata = data,type = "response") #mean = 0.04278; min = 0.02288; max = 0.07294 ; 
	
	hh = h2o.deeplearning(x = myX,y = "Loss",distribution ="tweedie",hidden = c(1),epochs = 1000,train_samples_per_iteration = -1,
                      reproducible = T,activation = "Tanh",balance_classes = F,force_load_balance = F,
                      seed = 2353123,tweedie_power = 1.5,score_training_samples = 0,score_validation_samples = 0,
                      weights_column = "Insured",training_frame = cancar) 
	hh@model$training_metrics@metrics$mean_residual_deviance  #0.0001958009   0.001300774
	mean_deviance = hh@model$training_metrics@metrics$mean_residual_deviance
	expect_equal(mean_deviance,0.000195800852)
	ph = as.data.frame(h2o.predict(hh,newdata = cancar)) #mean = 0.04399   mean = 0.04423 
	expect_equal(0.04398729972, mean(ph[,1]) )
	expect_equal(0.02274282792, min(ph[,1]) )
	expect_equal(0.07215634338, max(ph[,1]) )
		
	testEnd()
}
doTest("Deeplearning weight Test: deeplearning w/ weights for tweedie distribution", test)

