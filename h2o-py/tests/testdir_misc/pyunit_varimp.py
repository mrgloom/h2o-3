import sys
sys.path.insert(1, "../../")
import h2o

def varimp_test(ip,port):
    
    
    train = h2o.import_file(path=h2o.locate("smalldata/iris/iris_wheader.csv"))

    # Run GBM
    my_gbm = h2o.gbm(y=train["class"], x=train[1:4], ntrees=50, learn_rate=0.1, distribution="multinomial")

    should_be_none = my_gbm.varimp()
    assert should_be_none is None, "expected varimp to return None, but returned {0}".format(should_be_none)

    should_be_list = my_gbm.varimp(return_list=True)
    assert len(should_be_list) == 3, "expected varimp list to contain 3 entries, but it has " \
                                     "{0}".format(len(should_be_list))
    assert len(should_be_list[0]) == 4, "expected varimp entry to contain 4 elements (variable, relative_importance, " \
                                        "scaled_importance, percentage), but it has {0}".format(len(should_be_list[0]))

if __name__ == "__main__":
    h2o.run_test(sys.argv, varimp_test)
