import os

os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
# load necessary modules
# MNIST - Digit dataset - handwritten
# Sequential- sequential network model
# Dense - dense network layer
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
from matplotlib import pyplot as plt


# Load the data
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Flatten the images from 28 * 28 pixels to 784 element vector
num_pixels = X_train.shape[1] * X_train.shape[2]
X_train = X_train.reshape((X_train.shape[0], num_pixels)).astype('float32')
X_test = X_test.reshape((X_test.shape[0], num_pixels)).astype('float32')

# Data normalisation
X_train = X_train / 255
X_test = X_test / 255

# Download and create data class list
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)

# Extract amount of classes
num_classes = y_test.shape[1]

# Network model creation
model = Sequential()

# Add first layer, responsible for image data receive - number of neurons = number of pixels
model.add(Dense(num_pixels, input_dim=num_pixels, kernel_initializer='normal', activation='relu'))

# Addition of a second layer responsible for the class - number of neurons = number of classes
model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))

# Model compilation
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Training the model with data
# epoch - iteration count
# batch_size - number of elements from training data taken during a single transition of the learning function
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=1)

# Model testing
scores = model.evaluate(X_test, y_test, verbose=0)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))

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
