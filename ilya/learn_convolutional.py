import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
import pickle

#-----------------------------------------------------------------------------
# Обучаем модель
datadir = "D:/My/programs/labs_machine_learning/ilya"

X = pickle.load(open(datadir + "/processed/X_train.pickle", "rb"))
y = pickle.load(open(datadir + "/processed/y_train.pickle", "rb"))

#X = pickle.load(open(datadir + "/test/X_test.pickle", "rb"))
#y = pickle.load(open(datadir + "/test/y_test.pickle", "rb"))

model = Sequential()
model.add(Conv2D(64, (3, 3), input_shape = X.shape[1:]))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))

model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss="binary_crossentropy", 
             optimizer="adam", 
             metrics=['accuracy'])

model.fit(X, y, batch_size=32, epochs=5, validation_split=0.1)

#-----------------------------------------------------------------------------
# Тестируем модель
X_test = pickle.load(open(datadir + "/test/X_test.pickle", "rb"))
y_test = pickle.load(open(datadir + "/test/y_test.pickle", "rb"))

y_predicted = model.predict_classes(X_test)

y1 = np.asarray([y_test])
y2 = y_predicted.transpose()
y3 = y1 == y2

test_acc = 100.0 * np.sum(y3) / y1.size

print("Accuracy on test data: ", test_acc, "%")