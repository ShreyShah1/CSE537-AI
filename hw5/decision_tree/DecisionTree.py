import argparse
import copy
import math
import readData
import pprint

class ClassficationEnum:
	POSITIVE = '+'
	NEGATIVE = '-'

class Attribute(object):	
	def __init__(self, attributeName):
		self.attributeName = attributeName
	
	def calEntropy(self, positive, negative):
		total = float(positive + negative)
		sum = 0
		if positive:
			sum += (positive/total) * math.log(positive/total, 2)
		if negative:
				sum += (negative/total) * math.log(negative/total, 2)
		return sum

class Discrete(Attribute):
		#################################################################
		# (categoriesName, categoriesVal) 
		##################################################################
	def __init__(self, attributeName):
		self.categoriesName = []
		self.categoriesVal = []	
		Attribute.__init__(self, attributeName)

	def getInformationGain(self, data, cIndex):
		# categories Positive and Negatives.
		dictPosNeg = {}
		totalP = 0.0
		totalN = 0.0	

		for instance in data:
			classification = instance[cIndex]
			category = instance[self.attributeName]

			if category not in dictPosNeg:
				# Initialise the dict here.
				dictPosNeg[category] = [0, 0]
            
			if (classification == ClassficationEnum.POSITIVE):
				totalP += 1
				dictPosNeg[category][0] += 1
			elif (classification == ClassficationEnum.NEGATIVE):
				totalN += 1
				dictPosNeg[category][1] += 1
				
		sum = 0
		for category, val in dictPosNeg.iteritems():			
			sum += ((val[0] + val[1]) / (totalP + totalN)) * self.calEntropy(val[0], val[1])			

		#print " Total entropy " + str(self.calEntropy(totalP, totalN))
		return abs(self.calEntropy(totalP, totalN)) - abs(sum)

	###################################################
	# Takes in data, attribute and then gives a 
	# splits the data according to the category.
	#
	# Returns a dict of SplitedData.
	###################################################
	def splitData(self, data):
		spiltedData = {}		
	
		for instance in data:
			category = instance[self.attributeName]

			if category not in spiltedData:
				spiltedData[category] = []

			spiltedData[category].append(instance)
		return spiltedData


class Continous(Attribute):
	def __init__(self, attributeName):
		Attribute.__init__(self, attributeName)
		self.splitVal = None
		self.nextNodes = []

	def getInformationGain(self, data, cIndex):
		# This dict contains all the possible values ch
		# on which we can split.
		dictVal = {}
		maxVal = 0
		sVal = 0
		for instance in data:
			splitVal = instance[self.attributeName]
			
			splitVal = float(splitVal)
			if splitVal not in dictVal:
				curVal = self.getInformationGain1(splitVal, data, cIndex)
				if (maxVal < curVal):
					maxVal = curVal
					sVal = splitVal

		# Setting the splitVal which can used furthur use. 
		self.splitVal = sVal
		return maxVal


	def getInformationGain1(self, splitVal, data, cIndex):
		# categories Positive and Negatives.
		dictPosNeg = {'Left':[0, 0], 
					  'Right':[0, 0]}
		branch = ''
		totalP = 0.0
		totalN = 0.0	

		for instance in data:
			classification = instance[cIndex]
			continousSplitVal = instance[self.attributeName]
			
			continousSplitVal = float(continousSplitVal)
			
			if (continousSplitVal <= splitVal):
				branch = 'Left'
			else:
				branch = 'Right'

			if (classification == ClassficationEnum.POSITIVE):
				totalP += 1
				dictPosNeg[branch][0] += 1
			elif (classification == ClassficationEnum.NEGATIVE):
				totalN += 1
				dictPosNeg[branch][1] += 1
			else:
				print " ### PROBLEM ### "
			return 0
				
		sum = 0
		for branch, val in dictPosNeg.iteritems():			
			sum += ((val[0] + val[1]) / (totalP + totalN)) * self.calEntropy(val[0], val[1])			

		return abs(self.calEntropy(totalP, totalN)) - abs(sum)

	###################################################
	# Takes in data, a splits the data according 
	# to the split point.
	#
	# Returns a dict of SplitedData.
	###################################################
	def splitData(self, data):
		spiltedData = {'Left': [],
					   'Right': []}			
		for instance in data:			
			continousSplitVal = instance[self.attributeName]

			continousSplitVal = float(continousSplitVal)
			if (continousSplitVal <= self.splitVal):
				branch = 'Left'
			else:
				branch = 'Right'
			spiltedData[branch].append(instance)
		return spiltedData

class TreeNode(object):
	###################################################
	#  Example TreeNode:
	#  (A1, [cc, dd, ee], [TreeNode, TreeNode, TreeNode], false, NULL)
	def __init__(self):
		self.attributeObj = None
		self.isLeaf = False
		self.classification = None 		

class DecisionTree(object):	
	def __init__(self):
		self.root = TreeNode()

	# Implementing a mixture of ID3 and C4.5 algorithm.
	def makeTree(self, root, cIndex, attributesList, data):
		# Base case.
		# If data has the same classification no need to go furthur and make it as a Leaf.
		prev = False
		prevClassification = ''
		pure = True
		for instance in data:	
			curClassification = instance[cIndex]
			if prev and curClassification != prevClassification:
 				pure = False
 				break
 			prev = True
 			prevClassification = curClassification

 		if pure or len(data) == 1:
 			root.isLeaf = True
 			root.classification = prevClassification
 			return

 		# Base case ends. 
 		###########################################################################################
		# Initializing it so that 
		maxAttribute = ''
		maxGain = 0
 		## Calculate attribute with max entropy.
 		for attribute in attributesList: 			
 			gain = attribute.getInformationGain(data, cIndex)
 			if (maxGain <= gain):
 				maxGain = gain
 				maxAttribute = attribute

 		root.attributeObj = maxAttribute
 		if (maxAttribute == ''):
			root.isLeaf = True
			root.classification = self.getMajorityClassification(data, cIndex)
 			return 

 #		print " Trying to remove attribute " + str(maxAttribute.attributeName)
 		attributesList.remove(maxAttribute) 	# As this attribute is fixed.
 		##############################################################################################
 		# Seperate the data and recurse.
 		spiltedData = maxAttribute.splitData(data) 		
		for category, attData in spiltedData.iteritems():
			node = TreeNode()
			
			if (type(maxAttribute).__name__ == 'Discrete'):
				root.attributeObj.categoriesName.append(category)
				root.attributeObj.categoriesVal.append(node)
			else:
				root.attributeObj.nextNodes.append(node)

			self.makeTree(node, cIndex, copy.deepcopy(attributesList), attData)
	

 	def printTree(self, root): 		
 		queue = []
 		queue.append(root)
 		queue.append('#')
		print " ROOT = " + str(root.attributeObj.attributeName) 
 		while queue:
 			element = queue.pop(0)
 			
 			if element == '#':
 				if queue:
 					queue.append('#')
 					print " ************************************************** "  
 				else:
 					break
 			elif element.isLeaf == False: 					
				if (type(element.attributeObj).__name__ == 'Discrete'):
					for idx, category in enumerate(element.attributeObj.categoriesVal):
						print  str(element.attributeObj.categoriesName[idx]),
						if category.isLeaf == False:
							print " " + str(category.attributeObj.attributeName),
						else:
							print " " + str(category.classification),	
						queue.append(category)
				else:
					print 	str(element.attributeObj.splitVal),
					for data in element.attributeObj.nextNodes: 
						if data.isLeaf == False:
							print " " + str(data.attributeObj.attributeName),
						else:
							print " " + str(data.classification),
						queue.append(data)
				
			else:
				print element.classification,

	def getMajorityClassification(self, data, cIndex):
		if len(data) == 0:
			return "ERROR"
		positive = 0
		negative = 0
		for instance in data:
			classification = instance[cIndex]
			if classification == ClassficationEnum.POSITIVE:
				positive += 1
			else:
				negative += 1
		if (positive > negative):
			return ClassficationEnum.POSITIVE
		else:
			return ClassficationEnum.NEGATIVE


def accuracy(root, testingData, cIndex):
	predictedVals = []
	for i in range(0, len(testingData)):
			predictedVals.append(predictPosNeg(root, testingData[i], cIndex))
	correct = 0
	for tup in predictedVals:
		if (tup[0] == tup[1]):
			correct += 1
	return correct * 100.0/len(predictedVals)

def predictPosNeg(root, instance, cIndex):	
	if (root.isLeaf == True):
		return (root.classification, instance[cIndex])

	attributeName = root.attributeObj.attributeName	

	curRoot = root.attributeObj
	if (type(curRoot).__name__ == 'Discrete'):
		category = instance[attributeName]
		if (category not in curRoot.categoriesName):
			return ('+','+')
		index  = curRoot.categoriesName.index(category)
		return predictPosNeg(curRoot.categoriesVal[index], instance, cIndex)
	else:
		splitVal = float(instance[attributeName])
		
		if (splitVal <= curRoot.splitVal):
			return predictPosNeg(curRoot.nextNodes[0], instance, cIndex)
		else:	
			return predictPosNeg(curRoot.nextNodes[1], instance, cIndex)

def main(args):
	decisionTree = DecisionTree() 	
	cIndex, attributesList, data = readData.readData(args.input)
	decisionTree.makeTree(decisionTree.root, cIndex, attributesList, data[0:500])
	print accuracy(decisionTree.root, data[500:600], cIndex)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="HomeWork Five")
	parser.add_argument("--input", type=str)
	args = parser.parse_args()
	main(args)
