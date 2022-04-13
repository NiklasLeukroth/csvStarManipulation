import util
import csvHelper
import json


def main():
	default = "./HYG-Database/hygdata_v3.csv"
	resultPath = "./JSON/"
	util.createDirectory(resultPath)
	pathToFile = input("Enter the path to the file, or enter d or D for the default file: ")
	if util.checkIfAvailable(pathToFile) and pathToFile not in ['d', 'D']:
		print("File not found")
		main()
		return

	if pathToFile in ['d', 'D']:
			pathToFile = default

	resultName = "jsonStars"

	data = csvHelper.readFromCSVFile(pathToFile)

	jsonDict = convertCSVToJSON(data)

	file = util.createNewFile(resultPath, resultName, ".json")
	if file == None:
		print("to many json files already in ../JSON/")
		return

	writeToJSONFile(jsonDict, file)


def convertCSVToJSON(data):
	stars = []

	for star in data:
		lat, lon = util.getLatAndLongFromStar(star)
		name = star[6]
		magnitude = star[13]

		tmpDic = {}
		tmpDic['lat'] = lat
		tmpDic['long'] = lon
		tmpDic['name'] = name
		tmpDic['magnitude'] = magnitude

		stars.append(tmpDic)


	result = {}
	result['stars'] = stars
	return result



def writeToJSONFile(jsonDict, file):
    json_string = json.dumps(jsonDict, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    file.write(json_string)

    file.close()


main()