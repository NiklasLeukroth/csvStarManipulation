import sys
import os.path

def createDirectory(directoryPath):
	#check if the directory already exists, else create a new one
	if checkIfAvailable(directoryPath):
		os.makedirs(directoryPath)


def checkIfAvailable(path):
	return not os.path.exists(path)
