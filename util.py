import sys
import os.path
import math

deg2Rad = math.pi/180

def createDirectory(directoryPath):
	#check if the directory already exists, else create a new one
	if checkIfAvailable(directoryPath):
		os.makedirs(directoryPath)


def checkIfAvailable(path):
	return not os.path.exists(path)


def getLatAndLongFromStar(star):
	rightAscension = float(star[7])
	declination = float(star[8])

	lon = (rightAscension * 360 / 24 - 180) * deg2Rad
	lat = declination * deg2Rad

	return lat, lon


def createNewFile(path, fileName, fileEnding):
	pathToCheck = path + fileName + fileEnding
	if checkIfAvailable(pathToCheck):
		file = open(pathToCheck, 'w', newline = '')
		return file

	for i in range(100):
		pathToCheck = path + fileName + str(i) + fileEnding
		if checkIfAvailable(pathToCheck):
			file = open(pathToCheck, 'w', newline = '')
			return file

	return None
