import pickle
import numpy as np

# load freezed model
with open("../data/freeze_model/type1-1", "rb") as f:
    [w1, b1, w2, b2, w3, b3, w4, b4] = pickle.load(f)

def relu(x):
    """This function calculate ReLU function"""
    return np.asarray(x) * (np.asanyarray(x) > 0)

def outp(inp):
    """This function calculate output value via model"""
    a1 = relu(np.matmul(inp, w1) + b1)
    a2 = relu(np.matmul(a1, w2) + b2)
    a3 = relu(np.matmul(a2, w3) + b3)
    a4 = np.matmul(a3, w4) + b4
    return a4


def percentage(predict, outp):
    """This function calculate percentage between predicted value
    and actual value"""
    if predict<0:
        return 0.0
    if (abs(predict - outp)/outp)>1:
        return 0.0
    else:
        return 1 - abs(predict - outp)/outp


