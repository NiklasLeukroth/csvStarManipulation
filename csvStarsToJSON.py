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
		radius = 3000
		lat, lon = util.getLatAndLongFromStar(star)
		position = [radius * math.cos(lat) * math.cos(lon), radius * math.cos(lat) * math.sin(lon), radius * math.sin(lat)]
		name = star[6]
		if name == "":
			name = "star" + str(counter)
			counter += 1
		magnitude = star[13]

		tmpDic = {}
		tmpDic['position'] = position
		tmpDic['name'] = name
		tmpDic['magnitude'] = magnitude
		tmpDic['geometry'] = "star"
		tmpDic['scale'] = [1,1,1]
		tmpDic['material'] = str(name + "_material")
		tmpDic['color'] = [round(i / 255, 3) for i in convertBVToRG(star[16])]

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
		#magnitude = 0.1 + round(magnitude / 2.65, 3)
		magnitude = 0.1 + round(magnitude / 10, 3)

		tmpDic = {}
		tmpDic['emission_enabled'] = True
		tmpDic['emission_energy'] = magnitude
		tmpDic['name'] = str(name + "_material")
		tmpDic['emission'] = entry['color']
		entry.pop('color')
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


def convertBVToRG(bvIndex):
	if bvIndex == '':
		return [255,255,255]
	bvIndex = float(bvIndex)

	#Colors based on http://www.science-bbs.com/16-astro/f276016b19867881.htm
	#bluish white
	if bvIndex < 0.0:
		return [219, 235, 245]
	#pure white
	if bvIndex < 0.3:
		return [245 ,245 ,245]
	#yellowish white
	if bvIndex < 1.0:
		return [240 ,243 ,177]
	#orangeish white
	if bvIndex < 1.5:
		return [243 ,219 ,165]
	#Redish white
	return [243 ,190 ,165]

main()