from random import randint
import random
import numpy as np
from operator import itemgetter

N = 10000

#def hdv():
#    i = 0
#    lst = []
#    hdv = np.array(lst)
#    while i < N:
#        np.append(hdv, randint(0, 1))
#        if hdv[i] == 0:
#            hdv[i] = -1
#        print(hdv[i])
#
#
#def hdv2():
#    lst = []
#    i = 0
#    while i < N:
#        hdv = np.array(lst)
#        (lst, [[randint(0, 1)]])
#        #print(lst)
#        i += 1
#
#    np.where(lst > 0, lst, -1)
#    print(lst)


def hdv(n):
    hdv = []
    for y in range(n):
        subhdv = []
        for x in range(N):
            posOrNeg = randint(0, 1)
            if posOrNeg == 0:
               subhdv.append(-1)
            else:
                subhdv.append(1)
        #print(subhdv)
        hdv.append(subhdv)
    if n == 1:
        hdv = hdv[0]
    #print(hdv)
    return hdv

def bundle(matrix):
    bundled = []
    for x in range(N):
        tempList = list(map(itemgetter(x), (matrix)))
        sum = 0
        for items in tempList:
            sum = sum + items
    
        if sum == 0:
            bundled.append(0)
        elif sum > 0:
            bundled.append(1)
        else:
            bundled.append(-1)
    
    #print(bundled)
    return bundled

def bind(x, y):
    binded = [x[index] ^ y[index] for index in range(N)]
    for i in range(N):
        if binded[i] == -2:
            binded[i] = -1
        elif binded[i] == 0:
            binded[i] = 1

    #print(binded)
    return binded

#def bind(fullList):
#    i = 0
#    binded = fullList[0]
#    while i < len(fullList):
#        if i > 0:
#            binded = [binded[index] ^ fullList[i][index] for index in range(N)]
#            for i in range(N):
#                if binded[i] == -2:
#                    binded[i] = -1
#                elif binded[i] == 0:
#                    binded[i] = 1
#    return binded

def shift(x, k = 1):
    lst = np.array(x)
    shifted = np.roll(lst, k)
    #print(shifted)
    return shifted

def compare(x, y):
    compared = np.dot(x, y)/(np.linalg.norm(x) * np.linalg.norm(y))
    #print(compared)
    return compared

def rangeHdvs(steps):
    k = len(steps) - 1
    v = hdv(k + 1)
    for i in range(1, k + 1):
        for j in range(0, N):
            v[i][j] = -v[i-1][j] if random.random() < 1 / k else v[i-1][j]
    return v

def testCompareOpposite():
    x = []
    y = []
    for a in range(N):
        x.append(-1)
    for b in range(N):
        y.append(1)
    testCompared = compare(x, y)
    #print(testCompared)
    return testCompared

def testCompareAveragePos():
    x = hdv(1)
    y = []
    for a in range(N):
        y.append(1)
    testCompareAveragePos = compare(x, y)
    #print(testCompareAveragePos)
    return testCompareAveragePos

def testCompareAverageNeg():
    x = hdv(1)
    y = []
    for a in range(N):
        y.append(-1)
    testCompareAverageNeg = compare(x, y)
    #print(testCompareAverageNeg)
    return testCompareAverageNeg

def testSimilarPos():
    x = []
    y = []
    for a in range(N):
        x.append(1)
        y.append(1)
    y[0] = -1
    testCompared = compare(x, y)
    #print(testCompared)
    return testCompared
