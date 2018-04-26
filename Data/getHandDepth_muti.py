File = open("rawData_d.txt","r")
File2 = open("handPosition_d.txt","r")
File3= open("resizedData_d.txt","w+")

STANDARD_Z = 1.1072689
STANDARD_SIZE = 40
IMAGE_SIZE = 512*424
## calculate comparative hand size

pixels = File.read().split(", ")
image_counter = 0
sample_size = 100


for imageIndex in range(sample_size):

	handPos = File2.readline().split(", ")

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
			depth = pixels[image_counter * IMAGE_SIZE + i * 512 + j]
			handArea.append(depth)

## resize to 100*100

	length = realSize * 2
	width = realSize * 2
	hand_depth = int(pixels[image_counter * IMAGE_SIZE + x+y*512])


	if len(handArea) != length * width:
		print ("Error: Cannot resize")

	adjustRate = float(length)/100
	for i in range(100):
		for j in range(100):
			adjustY = int(float(i) * adjustRate)
			adjustX = int(float(j) * adjustRate)
			value = int(handArea[adjustY*length+adjustX])
			#remove background and foreground
			if (value > hand_depth + 100) | (value < hand_depth - 100):
				File3.write("0" + ", ")
			else:
				File3.write(str(int(handArea[adjustY*length+adjustX]) - hand_depth + 100) + ", ")

	image_counter=image_counter+1




