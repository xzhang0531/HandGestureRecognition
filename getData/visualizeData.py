from PIL import Image
im= Image.new('RGB', (100, 100))
file = open("resizedData.txt", "r")

data = file.read().split(", ")

imagedata = []

for i in range(10000):
	pixel = int(data[i])
	imagedata.append((pixel, pixel, pixel))



im.putdata(imagedata)
im.save('hand.png')