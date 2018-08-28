#-*- coding: utf-8 -*-
import os, sys, numpy as np
import cPickle as p
sys.path.append('../nn/')
from InitParam import *
from PretrainNetwork import *
import gl


np.random.seed(100)

# load token map
tokenMap = p.load(open('tokenMap.txt'))
tokenNum = len(tokenMap)

#################################
## construct token map

#tokenMap = dict()
#tokenNum = 0
#fin = open(inputfile)
#print tokenNum, tokenMap['BinaryOp']
##
#filedir = '../subtree/'
#flog = file('log.txt', 'w')
#fileNum = 1
#for onefile in os.listdir(filedir):
#  fin = open( filedir + onefile)
#  while True:
#    line = fin.readline().strip('\n\r')
#    if not line:
#        break
#    fin.readline()
#    for token in line.split(' '):
#        if not tokenMap.has_key(token):
#            tokenMap[token] = tokenNum
#            tokenNum += 1    
#  fileNum += 1
#  if fileNum%1000 == 0:
#    #print fileNum
#    fout= file('tokenMap.txt', 'w')
#    flog.write(str(fileNum)+'\n')
#    flog.flush()
#    p.dump(tokenMap, fout)
#    fout.close()
#  fin.close()

#fout = file('tokenMap.txt', 'w')
#import cPickle as p
#p.dump(tokenMap, fout)
#fout.close()

#################################
# configure network 

numFea = gl.numFea
Weights = np.array([])
Biases = np.array([])

Weights, Wleft = InitParam(Weights, num=numFea*numFea)
Weights, Wright= InitParam(Weights, num=numFea*numFea)
Biases,  Btoken = InitParam(Biases,  num=numFea*tokenNum, upper=0.4,lower=0.6)
Biases,  Bidx  = InitParam(Biases, num =numFea)

Weights = Weights.reshape((-1,1))
Biases = Biases.reshape((-1,1))
gradWeights = np.zeros_like(Weights)
gradBiases = np.zeros_like(Biases)

#################################
# construct the network


sys.path.append('../../')
from helper import *
import gl

fin = open(inputfile)

testPositive = []
testNegative = []

filedir = '../../../data/PL/subtree/'
allfiles = os.listdir(filedir)

# construct test sets
print 'constructing the test set'
for idx in range(100):
    fin = open(filedir + allfiles[idx])
    while True:
        line = fin.readline().strip('\n\r')
        if not line:
            break
        tokens = line.split(' ')
        leafCntString = fin.readline().strip('\n\r')
	# test positive
        positive  = ConstructPretrainNet(tokens, leafCntString, Wleft, Wright, Bidx, tokenMap, numFea, tokenNum)
        testPositive.append(positive)
        # test negative
        while True:
            negTokenIdx = np.random.randint(0, len(tokens) )
            negSampleIdx = np.random.randint(0, len(tokenMap) )
            if tokens[negTokenIdx] != tokenMap.keys()[negSampleIdx]:
                break
        tokens[negTokenIdx] = tokenMap.keys()[negSampleIdx]
        negative = ConstructPretrainNet(tokens, leafCntString, Wleft, Wright, Bidx, tokenMap, numFea, tokenNum)
        testNegative.append(negative)
    fin.close()


# testing on the test set
def test(num):

    if num > len(testPositive):
        num = len(testPositive)
    testError = 0
    for idx in range(num):
        tmpError, tmpCost = Cost(tokenMap, testPositive[idx], testNegative[idx], Weights, Biases, noGrad = True)
        testError += tmpError
    return testError/num

trainError = 10000
trainCnt = 1
minTestError = 10000

# testing
#print 'testing (size =', len(testNegative), ')'
#print test()
# for each file
lastError = 10000

flog = open('log', 'w')
for idx in range(1000, len(allfiles) ):
 
    if idx % 100 == 0:
        print '-----------------'
        print 'processed', idx - 1000, 'files'
        testError = test(5000)
        print 'testError =', testError, ' trainError = ', trainError/trainCnt
        print 'mean vector representation', np.mean(Biases[Btoken])
        flog.write('Processed ' + str(idx-1000) + ' files, testError = '+str(testError) + 'trainError = ' + str(trainError) + '\n')
        flog.flush()
        foutParam = open('param', 'w')
        p.dump( np.concatenate( (Weights, Biases)) , foutParam )
        foutParam.close()
        trainError = 0   
        trainCnt = 0
        if testError > lastError * 2:
             gl.alpha *= .95
             print 'alpha shrinking', gl.alpha
        lastError = testError
        if testError < minTestError:
            minTestError = testError
            foutParam = open('param_best', 'w')
            p.dump( np.concatenate( (Weights, Biases)) , foutParam )
            foutParam.close()
 
    fin = open(filedir + allfiles[idx])
    # for each training example
    while True:
        # construct positive
        line = fin.readline().strip('\n\r')
        if not line:
            break
        tokens = line.split(' ')
        leafCntString = fin.readline().strip('\n\r')
        positive  = ConstructPretrainNet(tokens, leafCntString, Wleft, Wright, Bidx, tokenMap, numFea, tokenNum)
        # construct negative
        while True:
            negTokenIdx = np.random.randint(0, len(tokens) )
            negSampleIdx = np.random.randint(0, len(tokenMap) )
            if tokens[negTokenIdx] != tokenMap.keys()[negSampleIdx]:
                break
        tokens[negTokenIdx] = tokenMap.keys()[negSampleIdx]
        negative = ConstructPretrainNet(tokens, leafCntString, Wleft, Wright, Bidx, tokenMap, numFea, tokenNum)
        
        # stochastic gradient descent
        tmperror, tmpcost = Cost(tokenMap, positive, negative,
                     Weights, Biases, gradWeights, gradBiases)
        trainError += tmperror
        trainCnt += 1
    Weights -= gl.alpha * gradWeights
    Biases -= gl.alpha * gradBiases
    gl.alpha *= .999
flog.close()

    
#############################
# stochastic gradient descent with momentum

#if len(positiveNets) != len(negativeNets):
#    print 'Great Error: # of positive samples and negative samples are not equal'
    
trainNum = len(positiveNets)

error = 100000
for ite in xrange(1, 1000):
    lastError = error
    error = 0
    for trainIdx in xrange(trainNum):
        gradWeights *= gl.decay
        gradBiases *= gl.decay
        tmperror, tmpcost = Cost(tokenMap, positiveNets[trainIdx], negativeNets[trainIdx], \
                     Weights, Biases, gradWeights, gradBiases)
        error += tmperror
        
        Weights -= gl.alpha * gradWeights
        Biases -= gl.alpha * gradBiases
    #gl.alpha = 3 / (1 + np.sqrt(ite) ) * (1- gl.momentum)
    if error >= lastError:
        print 'Cuts learning rate' 
        gl.alpha *= .95
    gl.alpha *= 0.999
    print 'Iteration = ',ite, ' Error =', error, 'alpha =', gl.alpha
    #print Weights[0:5]
    


#print '------positive-------'
#FFNN.displayLayers(positive)
#print '------negative-------'
#FFNN.displayLayers(negative)
#print '---------------------'

