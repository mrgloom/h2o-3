import sys, os
sys.path.insert(1, "../../../")
import h2o

import numpy as np
from sklearn import ensemble
from sklearn.metrics import roc_auc_score

def bernoulliGBM(ip,port):
  
  

  #Log.info("Importing prostate.csv data...\n")
  prostate_train = h2o.import_file(path=h2o.locate("smalldata/logreg/prostate_train.csv"))

  #Log.info("Converting CAPSULE and RACE columns to factors...\n")
  prostate_train["CAPSULE"] = prostate_train["CAPSULE"].asfactor()

  #Log.info("H2O Summary of prostate frame:\n")
  #prostate.summary()

  # Import prostate_train.csv as numpy array for scikit comparison
  trainData = np.loadtxt(h2o.locate("smalldata/logreg/prostate_train.csv"), delimiter=',', skiprows=1)
  trainDataResponse = trainData[:,0]
  trainDataFeatures = trainData[:,1:]

  ntrees = 100
  learning_rate = 0.1
  depth = 5
  min_rows = 10
  # Build H2O GBM classification model:
  #Log.info(paste("H2O GBM with parameters:\ndistribution = 'bernoulli', ntrees = ", ntrees, ", max_depth = 5,
  # min_rows = 10, learn_rate = 0.1\n", sep = ""))
  gbm_h2o = h2o.gbm(x=prostate_train[1:], y=prostate_train["CAPSULE"], ntrees=ntrees, learn_rate=learning_rate,
                    max_depth=depth, min_rows=min_rows, distribution="bernoulli")

  # Build scikit GBM classification model
  #Log.info("scikit GBM with same parameters\n")
  gbm_sci = ensemble.GradientBoostingClassifier(learning_rate=learning_rate, n_estimators=ntrees, max_depth=depth,
                                                min_samples_leaf=min_rows, max_features=None)
  gbm_sci.fit(trainDataFeatures,trainDataResponse)

  #Log.info("Importing prostate_test.csv data...\n")
  prostate_test = h2o.import_file(path=h2o.locate("smalldata/logreg/prostate_test.csv"))

  #Log.info("Converting CAPSULE and RACE columns to factors...\n")
  prostate_test["CAPSULE"] = prostate_test["CAPSULE"].asfactor()

  # Import prostate_test.csv as numpy array for scikit comparison
  testData = np.loadtxt(h2o.locate("smalldata/logreg/prostate_test.csv"), delimiter=',', skiprows=1)
  testDataResponse = testData[:,0]
  testDataFeatures = testData[:,1:]

  # Score on the test data and compare results

  # scikit
  auc_sci = roc_auc_score(testDataResponse, gbm_sci.predict_proba(testDataFeatures)[:,1])

  # h2o
  gbm_perf = gbm_h2o.model_performance(prostate_test)
  auc_h2o = gbm_perf.auc()

  #Log.info(paste("scikit AUC:", auc_sci, "\tH2O AUC:", auc_h2o))
  assert auc_h2o >= auc_sci, "h2o (auc) performance degradation, with respect to scikit"

if __name__ == "__main__":
  h2o.run_test(sys.argv, bernoulliGBM)
