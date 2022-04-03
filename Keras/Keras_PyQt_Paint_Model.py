
# Implementation of prediction and model loading support

import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
from keras.models import model_from_json
from keras.models import load_model
import numpy, cv2
import numpy as np

from PyQt5.QtGui import QImage, QPainter, QPen, QBrush, QPixmap

def qimage_to_array(image):
    """
    A function that converts a QImage object to a numpy array
    """
    image = image.convertToFormat(QImage.Format_Grayscale8)
    ptr = image.bits()
    ptr.setsize(image.byteCount())
    numpy_array = np.array(ptr).reshape(image.height(), image.width(), 1)

    # using the OpenCV library to display the image after conversion
    cv2.imshow('Check if the function works!', numpy_array)
    return numpy_array
    



def predict(image, model):
    """
    A function that uses the loaded neural network model to predict the sign in the image

    Appropriate code to handle the loaded model should be added here
    """
    numpy_array = qimage_to_array(image)

    # use of the OpenCV library to resize the image to the size of the images used in the MNIST file
    numpy_array = cv2.resize(numpy_array, (28,28))

    # using the OpenCV library to display the image after conversion
    cv2.imshow('Check if the function works!!', numpy_array)

    return 0


def get_model():
    """
    Function that loads the learned model of the neural network

     You should add the appropriate code for loading of the model and weights
    """
    return None  