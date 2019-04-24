import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D, AveragePooling2D
from tensorflow.keras.callbacks import TensorBoard
import pickle
import time

gpu_options = tf.GPUOptions(allow_growth=True)
session = tf.InteractiveSession(config=tf.ConfigProto(gpu_options=gpu_options))

datadir = "D:/My/programs/labs_machine_learning/ilya"

#-----------------------------------------------------------------------------
# Загружаем тренировочные данные
X = pickle.load(open(datadir + "/processed/X_train.pickle", "rb"))
y = pickle.load(open(datadir + "/processed/y_train.pickle", "rb"))

#X = pickle.load(open(datadir + "/test/X_test.pickle", "rb"))
#y = pickle.load(open(datadir + "/test/y_test.pickle", "rb"))

#-----------------------------------------------------------------------------
# Загружаем тестовые данные
X_test = pickle.load(open(datadir + "/test/X_test.pickle", "rb"))
y_test = pickle.load(open(datadir + "/test/y_test.pickle", "rb"))

test_data = (X_test, y_test)

#-----------------------------------------------------------------------------
# Обучаем модель при различных конфигурациях

#dense_layers = [0, 1, 2]
#conv_layers = [1, 2, 3]
#conv_sizes = [32, 64, 128]
#filter_sizes = [2, 3, 4]

# Отличные конфигурации: 
# 64x2(3x3)+0dense, 2 эпохи, 80%
# 128x3(3x3)+0dense, 1 эпоха, 85%
# 95x3(3x3)+0dense - 87.5%
# 109x3(3x3)+0dense - 87.5% - эта конфигурация менее стабильна, чем две соседние
# 130x3(3x3)+0dense - 87.5%


conv_layers = [3]
conv_sizes = [95, 109, 128, 130]
filter_sizes = [3]

f = open(datadir + "/error.txt", "wt")

for conv_layer in conv_layers:
    for conv_size in conv_sizes:
        for filter_size in filter_sizes:
            # Устанавливаем логирование во время обучения
            NAME = f"({filter_size}x{filter_size}).{conv_size}x{conv_layer}-Conv"
            tensorboard = TensorBoard(log_dir=f"{datadir}/logs/{NAME}")
            
            print(NAME)
            
            model = Sequential()
            model.add(Conv2D(conv_size, (filter_size, filter_size), input_shape = X.shape[1:]))
            model.add(Activation("relu"))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            
            for i in range(conv_layer-1):
                model.add(Conv2D(conv_size, (filter_size, filter_size)))
                model.add(Activation("relu"))
                model.add(MaxPooling2D(pool_size=(2, 2)))
            
            model.add(Flatten())
            
            # При задании больше чем одного плотного слоя, вылетает с нехваткой памяти
            #for i in range(dense_layer):
                #model.add(Dense(64))
                #model.add(Activation('relu'))
            
            model.add(Dense(1))
            model.add(Activation('sigmoid'))
            
            model.compile(loss="binary_crossentropy", 
                         optimizer="adam", 
                         metrics=['accuracy'])
            try:
                model.fit(X, y, 
                          batch_size=8, 
                          epochs=5, 
                          validation_split=0, validation_data=test_data,
                          callbacks=[tensorboard])
            except Exception as e:
                # Записать в файл имя ошибочного файла
                f.write(NAME + "\n")
                pass