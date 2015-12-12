import argparse
import math
import readData
import sys
import time

NO_OF_FEATURES = 784
TRAINING_LABELS_PATH = 'traininglabels.txt' 
TRAINING_IMAGES_PATH = 'trainingimages.txt'

TEST_LABELS_PATH = 'testlabels.txt'
TEST_IMAGES_PATH = 'testimages.txt'

class NaiveBayes(object):
	def __init__(self, data, instances):
                self.trainingData = data
		self.totalInstances = instances
		# This will have probability of all the labels.
		self.labelsProbability = []
		# This will have probability of features given the class labels.
		# i.e P(Feature = 1 | Class = 1) 
		self.featureProbability = [[[0, 0, 0] for x in range(NO_OF_FEATURES)] for y in range(NO_OF_FEATURES)]
	
		
        def calProbability(self, A, B):
		#########################################
		# Laplacian smoothing
		########################################
		return float(A + 1)/float(B + 3)

	def getCount(self, num, featureNum, instances):
		count = 0
		for instance in instances:
			if (num == int(instance[featureNum])):
				count = count + 1
		return count		
			
	def naiveBayes(self):
		############################################
		# Calculate Basic Probability for all labels.
		############################################
		for idx, labelInstances in enumerate(self.trainingData):
			self.labelsProbability.append(self.calProbability(len(labelInstances), self.totalInstances))
			for feature in range(784):
				for i in range(0, 3):
					featureProb = self.calProbability(
						self.getCount(i, feature , labelInstances), 
						len(labelInstances)
					)
					self.featureProbability[idx][feature][i] = featureProb

		#print " Labels " + str(self.labelsProbability)
		#print " ############ "  + str(self.featureProbability)
	def predictLabels(self, testingData):
		predictValuesLabels = []
		for i in range(0, len(testingData)):
                	for j in range(0, len(testingData[i])):
                        	 predictValuesLabels.append((i ,self.predictLabel(testingData[i][j])))
		return predictValuesLabels
	
	def accuracy(self, predictedVals):
		digitAccuracy = [[0 for x in range(3)] for y in range(10)]  
		
		for i in range(0,10):
			digitAccuracy[i][0]=i
		correct = 0
		for tup in predictedVals:
			if (tup[0] == tup[1]):
				correct += 1
				digitAccuracy[tup[1]][1] += 1
				digitAccuracy[tup[1]][2] += 1
			else: 	
				digitAccuracy[tup[1]][2] += 1
	    	
		print "Digit	Accuracy:"	
		for tup in digitAccuracy:
			print str(tup[0])+"	"+str(tup[1]*100.0/ tup[2])
					

		return correct * 100.0/len(predictedVals)

	def confusionmatrix(self, predictedVals):
		matrix = [[0 for x in range(12)] for x in range(12)]
		
		for tup in predictedVals:
			matrix[tup[0]][tup[1]] += 1
		
		for i in range(10):
			cost = 0
		 	for j in range(10):
				cost += matrix[i][j]
			matrix[i][10] = cost
			matrix[i][11] = matrix[i][i] * 100.0 / cost

		for i in range(10):
			cost = 0
		 	for j in range(10):
				cost += matrix[j][i]
			matrix[10][i] = cost
			matrix[11][i] = matrix[i][i] * 100.0 / cost

		print 'Predicted/Actual ',
	        for i in range(10):  
	              print i,
        	print 'Total',
		print '%'
	
       	
		for i in range(12):
			if(i<10):	print i,
			if(i == 10): 	print 'Total',
			if(i == 11):	print '%',
			for j in range(12):
			     	if(i == 11 or j == 11):
					print("%.2f" % matrix[i][j]),
				else:
					print matrix[i][j],
			print
				
	
	def predictLabel(self, instance):
		maxSum = -sys.maxint - 1
		predictLabel = ''
		for label in range(0, readData.TOTAL_LABELS):
			####################################
			# Calculate naive bayes probablity given a class label
			# P(X  | class = label)
			####################################
			sum = self.labelsProbability[label]
			for i in range(0, len(instance)):	
				featureProb = self.featureProbability[label][i][instance[i]]
				if (featureProb):
					sum *= featureProb
			
			if maxSum < sum:
				maxSum = sum
				predictLabel = label			

		return predictLabel

def main(args):
	ticks = time.time()
	trainingData = readData.readData(TRAINING_LABELS_PATH, TRAINING_IMAGES_PATH)
	totalInstances = 0
	for i in range(0, len(trainingData)):
                for fV in range(0, len(trainingData[i])):
			totalInstances += 1

	nb = NaiveBayes(trainingData, totalInstances)
	nb.naiveBayes()
	testingData = readData.readData(TEST_LABELS_PATH, TEST_IMAGES_PATH)
	predictedVals = nb.predictLabels(testingData)
	ticks = time.time() - ticks
	print "Total Accuracy: 	"+str(nb.accuracy(predictedVals))
	print "Execution Time: 	"+str(ticks)
	print "Confusion Matrix:\n "
	nb.confusionmatrix(predictedVals)

if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="HomeWork Five")
        parser.add_argument("--input", type=str)
        args = parser.parse_args()
        main(args)


