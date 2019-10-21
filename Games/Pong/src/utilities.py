"""
    src.utilities
    Helper functions
"""

def slidingAverage(history, newValue, smoothingLevel):
    if len(history) == smoothingLevel:
        history.pop()
    history.append(newValue)
    return mean(history), history

def mean(inputList):
    cumulativeSum = 0
    for val in inputList:
        cumulativeSum += val
    if len(inputList) > 0:
        return cumulativeSum / len(inputList)
    else:
        return 0
