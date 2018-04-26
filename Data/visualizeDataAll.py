from PIL import Image
file = open("resizedData_a.txt", "r")
data = file.read().split(", ")


for img in range(100):
	im= Image.new('RGB', (100, 100))
	imagedata = []

	for i in range(10000):
		pixel = int(data[img*10000+i])
		imagedata.append((pixel, pixel, pixel))



	im.putdata(imagedata)
	im.save('hand'+str(img)+'.png')
