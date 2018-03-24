# Explainations of the files

## getData.pde (later will be changed to send data through a trigger event, not store as a txt)
This is a Java code for getting the raw data from kinect and detecting the hand postion.
To run this code, you need to install Kinect SDK and Processing.
During executing, press "a" to obtain a raw image.

There will be two output for this file: handPosition.txt, rawData.txt.

## rawData.txt
This file stores the raw data. It contains 512*424 numbers, each number represents a pixel with depth information.
Depth are from 0-4500.
## handPosition.txt
This file stores the hand postion. It contains 3 numbers, representing X, Y and Z of the hand.
## getHandDepth.py (later will be changed to read data from a trigger event)
This will be the first function on the HYPERFAAS.
It takes rawData.txt and handPosition.txt as input, and output a 100*100 depth image(resizedData.txt) with hand centered.

This function will first calculate the comparative hand size according to how far the hand is from the device. Then get the hand area and resize to 100*100. 
This function will also remove the pixels that either too far or too near from the hand.
## visualizeData.py
This file for visualize the 100*100 data.

input: resizedData.txt

output: hand.png
