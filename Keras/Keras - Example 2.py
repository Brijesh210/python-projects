import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

# load necessary modules
# MNIST - Digit dataset - handwritten
# Sequential- sequential network model

from keras.datasets import mnist
from keras.utils import np_utils
from keras import layers
from keras import models
from keras.utils import to_categorical
from matplotlib import pyplot as plt

# Load the data
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Flatten the images and normalize them
train_images = train_images.reshape((60000, 28, 28, 1))
train_images = train_images.astype('float32') / 255

test_images = test_images.reshape((10000, 28, 28, 1))
test_images = test_images.astype('float32') / 255

# Download and create data class list
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

# Network model creation
model = models.Sequential()

# Addition of the first convolution layer of 32 3x3 kernels
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))

# Addition of a layer that reduces the size of the resulting images from the convolution layer
model.add(layers.MaxPooling2D((2, 2)))

# Addition of a second convolution layer
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

# Addition of a 2D to 1D data flattening layer
model.add(layers.Flatten())

# Addition of a dense layer responsible for the class - number of neurons = number of classes
model.add(layers.Dense(10, activation='softmax'))

#Compilation of the model
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Training the model with data
# epoch - iteration count
# batch_size - number of elements from training data taken during a single transition of the learning function
history = model.fit(train_images, train_labels, validation_data=(test_images, test_labels), epochs=5, batch_size=64, verbose=1)

print(history.history)
# learning history ploting
plt.subplot(2, 1, 1)
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')

plt.subplot(2, 1, 2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()