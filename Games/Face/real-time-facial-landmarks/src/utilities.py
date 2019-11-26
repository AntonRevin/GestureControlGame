"""
    src.utilities
    Helper functions
"""

def slidingAverage(history, newValue, smoothingLevel):
    if len(history) == smoothingLevel:
        history.pop(0)
    history.append(newValue)
    return mean(history), history

def mean(inputList):
    cumulativeSum = 0
    for val in inputList:
        cumulativeSum += val
    if cumulativeSum != 0:
        return cumulativeSum / len(inputList)
    else:
        return 0
