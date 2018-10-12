import numpy as np
import copy

def addlist(l, e):
    if not l :
        l = []
        l.append(e)
    else:
        l.append(e)
    return l


def computeMSE(output, target):
    numOutput, numData = target.shape
    # Error = .5 (y - 5)^2
    y_t = output - target
    Error =  .5 * np.sum( y_t * y_t )
    return Error / numData
    
def numericalGradient(f, x, theta):
    import numpy as np
    delta = 0.01
    gradTheta = np.zeros_like(theta)
    for idx in xrange(len(theta)):        
        tmpTheta = copy.copy(theta)
        tmpTheta[idx] += delta
        fplus = f(x, tmpTheta)
        tmpTheta[idx] -= 2*delta
        fminus = f(x, tmpTheta)
        gradTheta[idx] = (fplus - fminus) / 2 / delta
    return gradTheta

def checkGradient(numGrad, anaGrad, THRES = 0.01, verbose=True):
    
    toselect = abs(numGrad)>1e-8
    numGrad = numGrad[toselect]
    anaGrad = anaGrad[toselect]
    
    ratio = numGrad / anaGrad
    if verbose:
        print ratio
    ratio = ratio[ ~np.isnan(ratio),]
    print 'The max ratio is', max(ratio),'and the min ratio is', min(ratio)
    
    
    if max(ratio) < 1 + THRES and min(ratio) > 1 - THRES:
        print 'Numerical gradient checking passed with non-zero gradient # =', len(toselect) 
        return True
    else:
        print 'Numercial gradient checking failed'
        return False
    

