setwd(normalizePath(dirname(R.utils::commandArgs(asValues=TRUE)$"f")))
source('../../h2o-runit.R')

test.pca.score <- function(H2Oserver) {
  Log.info("Importing arrests.csv data...") 
  arrestsH2O <- h2o.uploadFile(H2Oserver, locate("smalldata/pca_test/USArrests.csv"), destination_frame = "arrestsH2O")
  
  Log.info("Run PCA with transform = 'DEMEAN'")
  fitH2O <- h2o.prcomp(arrestsH2O, k = 4, transform = "DEMEAN")
  print(fitH2O)
  
  Log.info("Project training data into eigenvector subspace")
  predH2O <- predict(fitH2O, arrestsH2O)
  Log.info("H2O Projection:"); print(head(predH2O))
  testEnd()
}

doTest("PCA Test: USArrests with Scoring", test.pca.score)
