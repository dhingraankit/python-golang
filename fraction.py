import os
import sys
from fractions import Fraction 


def reducedFractionSums(expressions):
    outputArray = []
    for element in expressions[1:]:
    	inputString = element.split('+')
    	someSum = 0
    	for element in inputString:
    		x,y = element.split('/')
    		fractioned = int(x)/int(y)
        	someSum = someSum + fractioned
    	outputArray.append(someSum)
    return outputArray

#Opening a text file and reading its lines
with open("Fraction_input.txt") as f:
    data = f.readlines()

#Printing what all is present in the text file
print("Data: ", data)

#Applying function over the text file to get the desired result
print("Output Array: ", reducedFractionSums(data))
