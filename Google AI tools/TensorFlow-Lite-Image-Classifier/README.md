# TensorFlow-Lite-Image-Classifier
### Creating an Android App using the pretrained Inception v3 Image Classifier

In this project, I imported the pretrained Inception v3 Image Classifier in an Android Studio App using TensorFlow Lite. <br>

In order to create this project I took reference to the following sources:<br>

- https://www.youtube.com/watch?v=8zQsAl2z4iU
- https://github.com/soum-io/TensorFlowLiteInceptionTutorial

Using this App, we first select the Inception Quantized Classifier (a compressed and less power hungry version of the full Inception Classifier). Successively, we then take a picture of the object we want to classify and finally we crop the picture (the Inception Classifier takes just squared images as inputs). Once we moved to the next window in the App, we can then click on the Classify Image button and our model will return the 3 most likely predictions. <br>

![](./TensorFlowLite.gif)

If you are interested in testing out yourself the App, this is available to download [here](https://github.com/pierpaolo28/Artificial-Intelligence-Projects/blob/master/Google%20AI%20tools/TensorFlow-Lite-Image-Classifier/AndroidImageClassifier.apk). <br>

Some useful downloads used to create this project are:

- https://www.tensorflow.org/lite/models
- https://github.com/jdamcd/android-crop


