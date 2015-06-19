import sys
sys.path.insert(1, "../../")
import h2o

def screeplot_test(ip,port):
    # Connect to h2o
    h2o.init(ip,port)

    australia = h2o.upload_file(h2o.locate("smalldata/pca_test/AustraliaCoast.csv"))
    australia_pca = h2o.prcomp(x=australia[0:8], k = 4, transform = "STANDARDIZE")
    australia_pca.screeplot(type="barplot", show=False)
    australia_pca.screeplot(type="lines", show=False)

if __name__ == "__main__":
    h2o.run_test(sys.argv, screeplot_test)