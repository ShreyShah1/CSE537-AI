################################################
## this files read data from training data file
###############################################
import copy
TOTAL_LABELS = 10

def readData(labels, images):
	
	###reading from training label file

	labels = [line.rstrip('\n') for line in open(labels)]

	### reading from training images file

	imageData = [line.rstrip('\n') for line in open(images)]

	data = [[] for x in range(TOTAL_LABELS)] 

	counter = 0
	row = 0
	tempData = []
	for i in range(0,len(imageData)):

		if(counter == 0):
			tempData = []			
			
		for j in range(0,28):
			if(imageData[i][j] == ' '):
				tempData.append(0)
			if(imageData[i][j] == '#'):
				tempData.append(1) 
			if(imageData[i][j] == '+'):
				tempData.append(2)
			counter = counter + 1
	
	 	if(counter == 784):	
			counter = 0
			classification = int(labels[row])
			row = row + 1
			data[classification].append(copy.deepcopy(tempData))
			
	return data
