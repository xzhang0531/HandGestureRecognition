# HandGestureRecognition

## Overview
Using a Microsoft Kinect with Kinect SDK, we can obtain depth graphs of hands. We then using TensorFlow to build a CNN model to train the model. After training, we put the trained model on serverless platform to do prediction upon request. (gestures will be American sign language)
## Data acquisition and processing
The raw data from Kinect is a 512*424 array, each pixel stores depth information. The first step is to extract the region of interest, which contain the hand inside. We utilize the skeleton tracking system of kinect sdk, to get the positions of hands in the scene. To eliminate the background and foreground information, we apply a depth threshold to discard the entries whose depth values is outside the threshold. Then, we draw a 100 by 100 bounding box at the 2D image plane centered with hand position.
## Model and training
Collect enough hand gestures for training. Then build a CNN model using TensorFlow and train the model. The training part will be done on our own desktop.
## Prediction (serverless)
Once a request with raw data comes, function one triggers to preprocess the raw data and generate a 100*100 matrix centered with hand position.
Then function two triggers after function one finished, using the model to do the prediction.
## Libraries needed
TensorFlow, Kinect SDK, Processing
