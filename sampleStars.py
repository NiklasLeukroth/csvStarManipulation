import random
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

	resultName = "sampledStars"

	n = int(input("Enter how many stars you want: "))

	if n < 1:
		print("Must select at least 1 element")
		main()
		return

	data = csvHelper.readFromCSVFile(pathToFile)

	length = len(data)

	if n > length:
		print("n exceeds the maximun stars, choose between 1 and " + str(length))
		main()
		return

	sampled = sample(data, n, length)
	file = util.createNewFile(resultPath, resultName, ".csv")
	if file == None:
		print("to many csv files already in ../CSV/")
		return
	csvHelper.writeToCSVFile(sampled, file)




def sample(data, n, length):
	indexList = []
	resultList = []
	resultList.append('')

	for i in range(n):
		rand = -1 
		while rand == -1 or rand in indexList:
			rand = random.randint(0, length - 1)
		resultList.append(data[rand])
		indexList.append(rand)

	return resultList


main()