################################################
## this files read data from training data file
###############################################


def readTrainingData():
	
	###reading from training label file

	labels = [line.rstrip('\n') for line in open('traininglabels.txt')]

	### reading from training images file

	imageData = [line.rstrip('\n') for line in open('trainingimages.txt')]

	trainingData = [[0 for x in range(785)] for x in range(len(labels))] 

	counter = 1
	row = 0

	for i in range(0,len(imageData)):

		if(counter == 1):
			trainingData[row][0]=labels[row]

		for j in range(0,28):
			if(imageData[i][j] == ' '):
				trainingData[0][counter] = 0
			if(imageData[i][j] == '#'):
				trainingData[0][counter] = 1 
			counter = counter + 1
	
	 	if(counter == 785):	
			counter = 1
			row = row + 1	
		
	print 	imageData[6][12]
	print	"len"+str(len(imageData)) 	
	print 	trainingData[12][0]

