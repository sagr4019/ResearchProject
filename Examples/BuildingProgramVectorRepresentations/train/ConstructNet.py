import sys

sys.path.append('../nn/')

import FFNN, gl, Connections as Con, Layers as Lay, numpy as np

def ConstructNet(tokens, leafCntString, Wleft, Wright, Bidx, tokenMap, numFea, tokenNum):
    
    leafCnt = leafCntString.split(' ')
    for idx, cnt in enumerate(leafCnt):
        leafCnt[idx] = int(leafCnt[idx])
    totalLeaf = sum(leafCnt)+.0
    leafCnt = np.array(leafCnt)
    leafCnt = leafCnt / totalLeaf 
    
    
    layers = []
    
    rootLayer = Lay.layer( tokens[0], \
                       range(numFea*tokenNum, numFea*(tokenNum+1) ),\
                       numFea,
                )
    totalChildren = len(tokens)
    for idx in range(1, totalChildren):
        childName = tokens[idx]
        childIdx = tokenMap[childName]
        # cunstruct node (layer)
        childLayer = Lay.layer( name= childName,\
                        Bidx = range(numFea*childIdx, numFea*(childIdx+1)),\
                        numunit = numFea,
                     )
        # add connection
        if totalChildren == 2:
            leftCoef = .5
            rightCoef =.5
        else:
            rightCoef = (idx - 1.0) / (totalChildren-2)
            leftCoef = 1 - rightCoef
        #print idx, len(leafCnt), len(tokens), leafCnt
        leftCoef *= leafCnt[idx-1]
        rightCoef *= leafCnt[idx-1]
        
        if leftCoef != 0:
            leftcon = Con.connection(childLayer, rootLayer, numFea, numFea,\
                         Wleft, leftCoef\
                        )
        if rightCoef != 0:
            rightcon =  Con.connection(childLayer, rootLayer, numFea, numFea,\
                         Wright, rightCoef\
                        )

        layers.append(childLayer)
    # end of each layer
    
    layers.append(rootLayer)
    
    for idx in xrange(0, len(layers)-1):
        layers[idx].successiveUpper = layers[idx+1]
        layers[idx+1].successiveLower = layers[idx]
    return layers
    # layer(self, name, Bidx, numunit, yL = 1, xL = 1)
    # connection(self, xlayer, ylayer, xbegin, xnum, ybegin, ynum, Widx):

# Cost(tokenMap, positive, negative, Weights, Biases, gradWeights, gradBiases, debug=True)

#Cost(tokenMap, positive, negative, Weights, Biases, gradWeights, gradBiases, debug=True)
#   Cost(tokenMap, positive, negative, Weights, Biases, debug=True, noGrad=True)

def Cost(tokenMap, positive, negative,\
          Weights, Biases, gradWeights=None, gradBiases=None, debug=False, noGrad=False):
    
    FFNN.cleanActivation(positive[0])
    FFNN.cleanActivation(negative[0])
    
    # forward propagation
    FFNN.forwardpropagation(positive[0], None, Weights, Biases)
    FFNN.forwardpropagation(negative[0], None, Weights, Biases)
    
    posOut = positive[-1].y
    negOut = negative[-1].y
    numFea = len(posOut)
    posTarIdx = tokenMap[positive[-1].name]
    negTarIdx = tokenMap[negative[-1].name]
    posTar = Biases[ posTarIdx*numFea: numFea*(posTarIdx+1)]
    negTar = Biases[ negTarIdx*numFea: numFea*(negTarIdx+1)]
    
    posDiff = posOut - posTar
    negDiff = negOut - negTar
    
    MSpos = .5*np.sum(posDiff * posDiff)
    MSneg = .5*np.sum(negDiff * negDiff)
    
    costPara = gl.C_2 * ( np.sum(Weights*Weights) + np.sum(Biases*Biases) )
    
    # Error = max{0, MSpos, }
    Error =  gl.margin + MSpos - MSneg
    # want MSpos < MSneg - margin
    if ( not debug and Error <  0):
        return 0, costPara
    elif noGrad:
        return  Error, Error + costPara
    # compute gradient
    FFNN.cleanDerivatives(positive[-1])
    FFNN.cleanDerivatives(negative[-1])

    positive[-1].dE_by_dy = posOut - posTar
    negative[-1].dE_by_dy = negTar - negOut

    FFNN.backpropagation(positive[-1], Weights, Biases, gradWeights, gradBiases)
    FFNN.backpropagation(negative[-1], Weights, Biases, gradWeights, gradBiases)
    
    gradBiases[ posTarIdx*numFea: numFea*(posTarIdx+1)] += posTar - posOut
    gradBiases[ negTarIdx*numFea: numFea*(negTarIdx+1)] += negOut - negTar
    
    gradWeights += gl.C * Weights
    gradBiases += gl.C * Biases
    
    return Error, Error + costPara
    
