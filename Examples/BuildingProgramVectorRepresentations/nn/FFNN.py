import numpy as np
from helper import *


def cleanDerivatives(layer):
    curLayer = layer
    while curLayer is not None:
        curLayer.dE_by_dz = None
        curLayer.dE_by_dy = None
        curLayer = curLayer.successiveLower

def cleanActivation(layer0):
    curLayer = layer0
    while True:
        curLayer.z = None
        curLayer.y  = None
        if curLayer.successiveUpper is None:
            break
        else:
            curLayer = curLayer.successiveUpper

def fpWrapper(x, theta):
    layer0, X, numW, target = x
    W = theta[0:numW]
    b = theta[numW:]
    cleanActivation(layer0)
    y = forwardpropagation(layer0, X, W, b)
    return computeMSE(target, y)

def forwardpropagation(layer0, X, W, b):
    if X is not None:
        numData = X.shape[1]
        layer0.y = X
        layer0.z = X
    else:
        numData = 1
    curLayer = layer0
    while True:
        curLayer.computeY(b, numData)

        if curLayer.successiveUpper is None:
            return curLayer.y
        for con in curLayer.connectUp:
            con.forwardprop(W, numData)

        curLayer = curLayer.successiveUpper


def backpropagation(outlayer, Weights, Biases, gradWeights, gradBiases):

    numData = outlayer.y.shape[1]
    curLayer = outlayer
    while curLayer is not None: # for each layer
        # dE/dy has size <numOutput> by <numData>
        #if curLayer.dE_by_dz is None and curLayer.z is not None:
        if curLayer.dE_by_dy is None:
            curLayer = curLayer.successiveLower
            continue
        curLayer.updateB(gradBiases)

        # back propogation
        for con in curLayer.connectDown:
            con.backprop(Weights, gradWeights, numData)
        # end of each upward connection
        curLayer = curLayer.successiveLower
    # end of all layers

    pass

