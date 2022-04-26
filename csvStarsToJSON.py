import util
import csvHelper
import json
import math


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

	objects = createObjects(data)
	materials = createMaterials(objects)
	geometry = createGeometry(objects)
	config = {}
	config['modelDir'] = "geometry/solarSystem/stars/"


	result = {}
	result['objects'] = objects
	result['materials'] = materials
	result['geometries'] = geometry
	result['config'] = config
	return result


def createObjects(data):
	objects = []
	counter = 0

	for star in data:
		lat, lon = util.getLatAndLongFromStar(star)
		position = [math.cos(lat) * math.cos(lon), math.cos(lat) * math.sin(lon), math.sin(lat)]
		name = star[6]
		if name == "":
			name = "star" + str(counter)
			counter += 1
		magnitude = star[13]

		tmpDic = {}
		tmpDic['position'] = position
		tmpDic['name'] = name
		tmpDic['magnitude'] = float(magnitude)
		tmpDic['geometry'] = "star"
		tmpDic['scale'] = [1,1,1]
		tmpDic['material'] = str(name + "_material")

		objects.append(tmpDic)

	return objects


def createMaterials(objects):
	materials = []

	for entry in objects:
		name = entry['name']
		magnitude = float(entry['magnitude'])

		#the lowest magnitude in the set is -1.44
		#the highest magnitude in the set is 6.5
		#the highest possible emmision is supposed to be 3, hence /2.65 => 7.94/2.65 ~ 3

		magnitude += 1.44
		magnitude =  7.94 - magnitude
		magnitude = magnitude / 2.65

		tmpDic = {}
		tmpDic['emission_enabled'] = True
		tmpDic['emission_energy'] = magnitude
		tmpDic['name'] = str(name + "_material")
		tmpDic['emission'] = [255,255,255]
		tmpDic['use_as_albedo'] = True

		materials.append(tmpDic)

	return materials


def createGeometry(objects):
	geometry = []


	tmpDic = {}
	tmpDic['name'] = "star"
	tmpDic['type'] = "mesh"
	tmpDic['path'] = "star.glb"

	geometry.append(tmpDic)

	return geometry


def writeToJSONFile(jsonDict, file):
    json_string = json.dumps(jsonDict, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    file.write(json_string)

    file.close()


main()