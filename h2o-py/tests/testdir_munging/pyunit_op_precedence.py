import sys
sys.path.insert(1, "../../")
import h2o
import random
import numpy as np

def op_precedence(ip,port):
    # Connect to a pre-existing cluster
    

    a = [[random.uniform(-100,100) for r in range(10)] for c in range(10)]
    b = [[random.uniform(-100,100) for r in range(10)] for c in range(10)]
    c = [[random.uniform(-100,100) for r in range(10)] for c in range(10)]

    A = h2o.H2OFrame(python_obj=a)
    B = h2o.H2OFrame(python_obj=b)
    C = h2o.H2OFrame(python_obj=c)

    np_A = np.array(a)
    np_B = np.array(b)
    np_C = np.array(c)

    s1 = np_A + np_B * np_C
    s2 = np_A - np_B - np_C
    s3 = np_A ** 1 ** 2
    s4 = np.logical_and(np_A == np_B, np_C)
    s5 = np_A == np_B + np_C
    s6 = np.logical_and(np.logical_or(np_A, np_B), np_C)

    print "Check A + B * C"
    S1 = A + B * C
    h2o.np_comparison_check(S1, s1, 10)

    print "Check A - B - C"
    S2 = A - B - C
    h2o.np_comparison_check(S2, s2, 10)

    print "Check A ^ 2 ^ 3"
    S3 = A ** 1 ** 2
    h2o.np_comparison_check(S3, s3, 10)

    print "Check A == B & C"
    S4 = A == B & C
    h2o.np_comparison_check(S4, s4, 10)

    print "Check A == B + C"
    S5 = A == B + C
    h2o.np_comparison_check(S5, s5, 10)

    print "Check A | B & C"
    S6 = A | B & C
    h2o.np_comparison_check(S6, s6, 10)

if __name__ == "__main__":
    h2o.run_test(sys.argv, op_precedence)
