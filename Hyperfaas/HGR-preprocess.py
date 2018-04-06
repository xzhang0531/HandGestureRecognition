from flask import request

def main():
	rawData = ""
	if request.data:
		rawData = request.get_json().get("rawData")
		handLocation = request.get_json().get("handLocation")
	else:
		return "Error: No data in the request!"

	STANDARD_Z = 1.1072689
	STANDARD_SIZE = 40

	## calculate comparative hand size

	pixels = rawData.split(", ")
	pixels[0] = pixels[0][1:]
	pixels[-1] = pixels[-1][:-1]

	handPos = handLocation.split(", ")
	

	x = int(float(handPos[0]))
	y = int(float(handPos[1]))
	z = float(handPos[2])



	adjustRate = z/STANDARD_Z
	realSize = int(STANDARD_SIZE/adjustRate)

	startX = x - realSize
	endX = x + realSize
	startY = y - realSize
	endY = y + realSize

	## get hand area

	handArea = []

	for i in range(startY, endY):
		for j in range(startX, endX):
			depth = pixels[i * 512 + j]
			handArea.append(depth)

	## resize to 100*100

	length = realSize * 2
	width = realSize * 2
	hand_depth = int(pixels[x+y*512])


	if len(handArea) != length * width:
		return "Error: Cannot resize!"

	adjustRate = float(length)/100

	result = "" 
	
	for i in range(100):
		for j in range(100):
			adjustY = int(float(i) * adjustRate)
			adjustX = int(float(j) * adjustRate)
			value = int(handArea[adjustY*length+adjustX])
			#remove background and foreground
			if (value > hand_depth + 100) | (value < hand_depth - 100):
				result = result + "0" + ", "
			else:
				result = result + str(int(handArea[adjustY*length+adjustX]) - hand_depth + 100) + ", "

	result = result[:-2]

	#return "function works"

	return "{\"data\": \"" + result + "\"}"




