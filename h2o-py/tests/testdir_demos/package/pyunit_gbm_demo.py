import sys
sys.path.insert(1, "../../../")
import h2o

def demo_gbm(ip,port):

    h2o.demo(func="gbm", interactive=False, test=True)

if __name__ == "__main__":
    h2o.run_test(sys.argv, demo_gbm)
