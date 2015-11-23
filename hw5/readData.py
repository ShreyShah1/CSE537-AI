from DecisionTree import Attributes
###############################################
# In this file we have imported data and also
# defining the static mapping in this file.
##############################################

def readData(filePath):
	# Reading file
	fileHandle = open(filePath, 'r')
	attributes = []
	
	lenAttribute = 0
	for line in fileHandle:		
		attribute = line.strip('\n').split(',')
		lenAttribute = len(attribute)
		attributes.append(attribute)
	
	# Attributes List.
	# Uncomment when done.
	attributesList = range(0, lenAttribute - 1)
	# attributesList = [0, 3, 4, 5, 6, 8, 9, 11, 12]
	# Hardcodding the values.
	mapping = [['b', 'a'], 
    			[], 
    			None, 
    			['u', 'y', 'l', 't'], 
    			['g', 'p', 'gg'], 
    			['c', 'd', 'cc', 'i', 'j', 'k', 'm', 'r', 'q', 'w', 'x', 'e', 'aa', 'ff'], 
    			['v', 'h', 'bb', 'j', 'n', 'z', 'dd', 'ff', 'o'],
    			None,
    			['t', 'f'],
    			['t', 'f'],
   				None,
    			['t', 'f'],
    			['g', 'p', 's'],
    			None,
    			None,
    			['+', '-']]

	return Attributes(lenAttribute, len(attributes), attributesList, mapping, attributes)  
