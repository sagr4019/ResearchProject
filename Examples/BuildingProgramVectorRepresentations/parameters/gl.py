# -*- coding: utf-8 -*-
"""
Created on Tue May 20 16:01:35 2014

@author: mou
"""

margin = 1
learnRate = .001
momentum = 0.1

# pid 12482 learning rate = .003

decay = momentum/(1-momentum)
alpha = learnRate * (1-momentum)
 
C = 0#.03/17340

C_2 = C/2

numFea = 30
#numCon = 50
#numDis = 60
numOut = 2

# for numerical gradient checking
#numFea = 2
#numCon = 3
#numDis = 4
#numOut = 4