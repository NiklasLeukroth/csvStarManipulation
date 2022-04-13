import csv
import util


def readFromCSVFile(path):
	file = open(path, 'rt', newline='')
	reader = csv.reader(file, delimiter=',')

	data = []
	firstRow = True

	for row in reader:
		if(firstRow):
			firstRow = False
			continue
		data.append(row)

	file.close()

	return data


def writeToCSVFile(data, file):
	writer = csv.writer(file, delimiter=',')

	for row in data:
		writer.writerow(row)


	file.close()
