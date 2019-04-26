import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D, AveragePooling2D
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.models import model_from_json
import pickle

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


#conv_layers = [[128], [128, 128, 128], [32, 64, 128], [32, 64], [64, 128]]
#conv_layers = [[128, 64, 32], [64, 32], [128, 64]]
#conv_layers = [[16, 32], [16, 32, 64], [16, 32, 64, 128], [16, 32, 64, 128, 256]]
conv_layers = [[64, 64], [100, 100], [150, 150], [200, 200], [32, 32]]

f = open(datadir + "/error.txt", "wt")

for conv_layer in conv_layers:
    # Устанавливаем логирование во время обучения
    NAME = f"{conv_layer}-Conv"
    tensorboard = TensorBoard(log_dir=f"{datadir}/logs/{NAME}")
    
    print(NAME)
    
    model = Sequential()
    
    model.add(Conv2D(conv_layer[0], (3, 3), input_shape = X.shape[1:]))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    iterlayer = iter(conv_layer)
    next(iterlayer)
    
    for i in iterlayer:
        model.add(Conv2D(i, (3, 3), input_shape = X.shape[1:]))
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
                  epochs=2, 
                  validation_split=0, validation_data=test_data,
                  callbacks=[tensorboard])
        
        # serialize model to JSON
        model_json = model.to_json()
        with open(datadir + f"/models/{NAME}.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights(datadir + f"/models/{NAME}.h5")
        print("Saved model to disk")
    except Exception as e:
        # Записать в файл имя ошибочного файла
        f.write(NAME + "\n")
        pass