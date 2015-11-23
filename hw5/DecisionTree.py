import argparse
import math
import readData

class ClassficationEnum:
	POSITIVE = '+'
	NEGATIVE = '-'

class Attributes(object):	
	def __init__(self, noOfAttributes, noOfInstances, attributesList, mapping, data):
		self.noOfAttributes = noOfAttributes
		self.noOfInstances = noOfInstances
		self.classificationIndex = noOfAttributes - 1
		self.attributesList = attributesList
		self.mapping = mapping
		self.data = data

class TreeNode(object):
	###################################################
	#  Example TreeNode:
	#  (A1, [cc, dd, ee], [TreeNode, TreeNode, TreeNode], false, NULL)
	def __init__(self):
		self.attributeName = None
		self.categoryName = []
		self.categoryVal = []
		self.isLeaf = False
		self.classification = None 		

class DecisionTree(object):	
	def __init__(self):
		self.root = TreeNode()

	def calEntropy(self, positive, negative):
		total = float(positive + negative)
		sum = 0
		if positive:
			sum += (positive/total) * math.log10(positive/total)
		if negative:
			sum += (negative/total) * math.log10(negative/total)
		return sum

	def getInformationGain(self, attribute, categories, data, cIndex):
		# categories Positive and Negatives.
		dictPosNeg = {}
		totalP = 0.0
		totalN = 0.0	

		for instance in data:
			classification = instance[cIndex]
			category = instance[attribute]
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
	def splitData(self, attribute, categories, data):
		spiltedData = {}		
	
		for instance in data:
			category = instance[attribute]
			if category not in spiltedData:
				spiltedData[category] = []

			spiltedData[category].append(instance)
		return spiltedData
			
			
	# Implementing a mixture of ID3 and C4.5 algorithm.
	def makeTree(self, root, attributesList, attributesObject, data):
		# Base case.
		# If data has the same classification no need to go furthur and make it as a Leaf.
		prev = False
		prevClassification = ''
		pure = True
		cIndex = attributesObject.classificationIndex
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
 			categories = attributesObject.mapping[attribute]
 			gain = self.getInformationGain(attribute, categories, data, cIndex)
 			print " Gain " + str(gain)
 			if (maxGain <= gain):
 				maxGain = gain
 				maxAttribute = attribute

 		print " Got max attribute = " + str(maxAttribute) + " gain = " + str(maxGain)

 		root.attributeName = maxAttribute		
 		attributesList.remove(maxAttribute) 	# As this attribute is fixed.
 		##############################################################################################
 		# Seperate the data and recurse.
 		spiltedData = self.splitData(maxAttribute, attributesObject.mapping[maxAttribute], data)

 		for category, attData in spiltedData.iteritems():
 			node = TreeNode()
 			root.categoryName.append(category)
 			root.categoryVal.append(node)
 			self.makeTree(node, attributesList, attributesObject, attData)

 	def printTree(self, root): 		
 		queue = []
 		queue.append(root)
 		queue.append('#')
 		while queue:
 			element = queue.pop(0)
 			if element != '#':
 				print element.attributeName
 				print element.categoryName
 			if element == '#':
 				if queue:
 					queue.append('#')
 					print " New Level "
 				else:
 					break
 			else:
 				for category in element.categoryVal:
 					queue.append(category)

def main(args):
	decisionTree = DecisionTree()	
	attributeObj = readData.readData(args.input)
	decisionTree.makeTree(decisionTree.root, attributeObj.attributesList, attributeObj, attributeObj.data)
	decisionTree.printTree(decisionTree.root)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="HomeWork Five")
	parser.add_argument("--input", type=str)
	args = parser.parse_args()
	main(args)
