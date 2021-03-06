setwd(normalizePath(dirname(R.utils::commandArgs(asValues=TRUE)$"f")))
source('../../h2o-runit.R')

test.glrm.simplex <- function(conn) {
  m <- 1000; n <- 100; k <- 10
  Log.info(paste("Uploading random uniform matrix with rows =", m, "and cols =", n))
  Y <- matrix(runif(k*n), nrow = k, ncol = n)
  X <- matrix(0, nrow = m, ncol = k)
  for(i in 1:nrow(X)) X[i,sample(1:ncol(X), 1)] <- 1
  train <- X %*% Y
  train.h2o <- as.h2o(conn, train)
  
  Log.info("Run GLRM with quadratic mixtures (simplex) regularization on X")
  initY <- matrix(runif(k*n), nrow = k, ncol = n)
  fitH2O <- h2o.glrm(train.h2o, init = initY, loss = "L2", regularization_x = "Simplex", gamma_x = 1, gamma_y = 0)
  Log.info(paste("Iterations:", fitH2O@model$iterations, "\tFinal Objective:", fitH2O@model$objective))
  fitY <- t(fitH2O@model$archetypes)
  fitX <- h2o.getFrame(fitH2O@model$loading_key$name)

  Log.info("Check that X matrix consists of rows within standard probability simplex")
  fitX.mat <- as.matrix(fitX)
  if(fitH2O@model$objective == "Infinity") {
    expect_false(all(fitX.mat >= 0) && all(apply(fitX.mat, 1, sum) == 1))
  } else {
    expect_true(all(fitX.mat >= 0))
    apply(fitX.mat, 1, function(row) { expect_equal(sum(row), 1, .Machine$double.eps) })
    expect_equal(sum((train - fitX.mat %*% fitY)^2), fitH2O@model$objective)
  }
  testEnd()
}

doTest("GLRM Test: Soft K-means Implementation by Quadratic Mixtures", test.glrm.simplex)