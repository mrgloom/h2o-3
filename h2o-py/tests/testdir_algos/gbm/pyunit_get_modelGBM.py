import sys
sys.path.insert(1, "../../../")
import h2o

def get_modelGBM(ip,port):
  
  

  prostate = h2o.import_file(path=h2o.locate("smalldata/logreg/prostate.csv"))
  prostate.describe()
  prostate[1] = prostate[1].asfactor()
  prostate_gbm = h2o.gbm(y=prostate[1], x=prostate[2:9], distribution="bernoulli")
  prostate_gbm.show()

  prostate_gbm.predict(prostate)
  model = h2o.get_model(prostate_gbm._id)
  model.show()

if __name__ == "__main__":
  h2o.run_test(sys.argv, get_modelGBM)
