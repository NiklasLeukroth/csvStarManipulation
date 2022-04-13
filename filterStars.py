import csvHelper
import util


def main():
	default = "./HYG-Database/hygdata_v3.csv"
	resultPath = "./CSV/"
	util.createDirectory(resultPath)
	pathToFile = input("Enter the path to the file, or enter d or D for the default file: ")
	if util.checkIfAvailable(pathToFile) and pathToFile not in ['d', 'D']:
		print("File not found")
		main()
		return

	if pathToFile in ['d', 'D']:
			pathToFile = default

	resultName = "filteredStars"

	data = csvHelper.readFromCSVFile(pathToFile)

	filtered = filter(data)

	file = csvHelper.createNewCSVFile(resultPath, resultName, ".csv")
	if file == None:
		print("to many csv files already in ../CSV/")
		return
	csvHelper.writeToCSVFile(filtered, file)


def filter(data):
	result = []
	for row in data:
		if float(row[12]) <= 6.5:
			result.append(row)

	return result


main()