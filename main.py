import cnn
import hdc

def generateSteps(step=0.05, rangeBegin=-1, rangeEnd=1):
    steps = []
    i = rangeBegin

    while i <= rangeEnd:
        steps.append(i)
        i = i + step
        i = round(i, 2)
        #print(steps)
    return steps

def fullBind(inputList):
    result = []
    for element in inputList:
        toBind = element[0]
        for item in range(1, len(element)):
            toBind = hdc.bind(toBind, element[item])
        result.append(toBind)
    return result

def genAndEncode(inputNum):
    nnNum = inputNum
    networks = []
    HDVSNetworks = []

    for element in range(nnNum):
        networks.append(cnn.organizeWeights())
        currentNetwork = []
        HDVSNetworks.append(hdc.rangeHdvs(generateSteps()))
    result = fullBind(HDVSNetworks)
    return result

def findClosest(toCompare, generated):
    highest = -1
    closest = 0
    counter = 0
    result = None
    for element in generated:
        newHighest = hdc.compare(toCompare, element)
        if newHighest > highest:
            highest = newHighest
            closest = counter
            result = element
        counter += 1
    print("Closest result element ", str(closest), " at ", str(highest))
    return result



def main():
    genAndEncode(10)
    return 0
