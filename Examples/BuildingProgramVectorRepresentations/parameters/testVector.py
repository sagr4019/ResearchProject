
import copy, numpy as np
import operator
import cPickle as cp
import sys
import gl
from InitParam import *
from cluster import *

np.random.seed(10)

###############################
# load data

tokenMap = cp.load( file('tokenMap.txt'))
tokenNum = len(tokenMap)
numFea = gl.numFea
Weights = np.array([])
Biases = np.array([])

Weights, Wleft = InitParam(Weights, num=numFea*numFea)
Weights, Wright= InitParam(Weights, num=numFea*numFea)
Biases,  Btoken = InitParam(Biases,  num=numFea*tokenNum, upper=0.4,lower=0.6)
Biases,  Bidx  = InitParam(Biases, num =numFea)


numW = len(Weights)

param = cp.load( file('param') )

Weights = param[:numW]
Biases = param[numW:]

def getVecByToken(token):
    idx = tokenMap[token]
    return Biases[idx*numFea:numFea*(idx+1)]
    

     
'''
# plot a subset
def plot1(toplot,color):
    n = len(toplot)
    N = [0]*n
    for i in range(0,n):
        key = toplot[i]
        N[i] = Node(getVecByToken(key).reshape(-1),color[i],name = key)
        
    re = do_clustering(N)
    re.to_dendrogram('hierarchical_cluster(subset).pdf')
    
    
toplot = ['BinaryOp', 'ID', 'Constant', 'ArrayRef', 'For', 'If', 'While', 
'DoWhile', 'Break', 'FuncDecl', 'ArrayDecl', 'PtrDecl']

#Binary Op, ID, Constant, ArrayRef, For, If, While, DoWhile, Break, FuncDecl, ArrayDecl, PtrDecl
color = [0,0,0,0,1,1,1,1,1,2,2,2]
plot1(toplot,color)

'''

################################################
# hierarchical clustering

count = 0
N = [0]*44

keys = tokenMap.keys()
for key in keys:
    N[count] = Node(getVecByToken(key).reshape(-1),0,name = key)
    count +=1   
    #print count,key
    #print getVecByToken(key).reshape(-1)
    
    
re = do_clustering(N)
re.to_dendrogram('hierarchical clustering.pdf')
    


###########################################
# nearest neighbor and k-means clustering
'''
keys = []
tokenVec = []
for key in tokenMap.keys():
     keys.append(key)
     tokenVec.append(getVecByToken(key).reshape(-1) )
     
tokenVec = np.array(tokenVec)


def findNearestByVec(tokenMap, vec):
    for i in tokenMap.keys():
        tokenDist = copy.copy(tokenMap)
        for key in tokenDist.keys():
            tmpVec = getVecByToken(key)
            dist = sum( (tmpVec - vec) ** 2 )
            tokenDist[key] = dist
    #return tokenDist
    sorted_x = sorted(tokenDist.iteritems(), key=operator.itemgetter(1))
    print sorted_x
    print '--------------end---------'
    return tokenDist

print '++--'
vec1 = getVecByToken('ArrayRef')
vec2 = getVecByToken('StructRef')
vec3 = getVecByToken('Struct')
findNearestByVec( tokenMap, vec1 +  vec3 -  vec2)
#print getVecByToken('BinaryOp')

findNearestByVec(tokenMap, getVecByToken('For'))   
#findNearestByVec(tokenMap, getVecByToken('While'))
#findNearestByVec(tokenMap, getVecByToken('ID'))
#findNearestByVec(tokenMap, getVecByToken('Constant'))
#findNearestByVec(tokenMap, getVecByToken('BinaryOp'))
#findNearestByVec(tokenMap, getVecByToken('UnaryOp'))
'''