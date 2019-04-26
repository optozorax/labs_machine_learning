import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard

import pickle
import time






# Добавляем входные слои
def addInputLayer(X, model, layer_size, kernelSize, poolSize):
    model.add(Conv2D(layer_size, (kernelSize, kernelSize), input_shape=X.shape[1:]))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(poolSize, poolSize)))


# Добавляем выходные слои
def addOutputLayer(model):
    model.add(Dense(1))
    model.add(Activation('sigmoid'))


# Добавляем свёрточные слои
def addConvolutionalLayers(conv_layer, model, layer_size, kernelSize, poolSize):
    for i in range(conv_layer):
        model.add(Conv2D(layer_size, (kernelSize, kernelSize)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(poolSize, poolSize)))


# Добавляем плотные слои
def addDenseLayers(dense_layer, model, layer_sizes):
    for i in range(dense_layer):
        model.add(Dense(layer_sizes))
        model.add(Activation('relu'))



# Подбираем оптимальные параметры
def research():
    
    tBegin = time.time()
    conv_layers = [1, 2, 3]
    dense_layers = [0, 1]
    layer_sizes = [32, 64]
    kernel_sizes = [2, 3]
    pool_sizes = [2, 3]
    
    for conv_layer in conv_layers:
        for dense_layer in dense_layers:
            for layer_size in layer_sizes:
                for kernel_size in kernel_sizes:
                    for pool_size in pool_sizes:
                        time.sleep(0.2)
                        # Визуализация в Tensorboard
                        name = "{}-conv-{}-dense-{}-lsize-{}-ksize-{}-psize-{}".format(conv_layer, dense_layer, layer_size, kernel_size, pool_size, int(time.time()))
                        print(name)
                        tensorboard = TensorBoard(log_dir='logs/{}'.format(name))
                        
                        # Считываем обучающую и тестирующую выборки
                        pickle_in = open("train/X_train.pickle","rb")
                        X_train = pickle.load(pickle_in)
                        pickle_in = open("train/y_train.pickle","rb")
                        y_train = pickle.load(pickle_in)
                        
                        pickle_in = open("test_common/X_test.pickle","rb")
                        X_test = pickle.load(pickle_in)
                        pickle_in = open("test_common/y_test.pickle","rb")
                        y_test = pickle.load(pickle_in)
                    
                        model = Sequential()
                        addInputLayer(X_train, model, layer_size, kernel_size, pool_size)
                        addConvolutionalLayers(conv_layer, model, layer_size, kernel_size, pool_size)
                        model.add(Flatten())
                        addDenseLayers(dense_layer, model, layer_size)
                        addOutputLayer(model)
                        
                        
                        model.compile(loss='binary_crossentropy',
                                      optimizer='adam',
                                      metrics=['accuracy'])
                        
                        batchSize = 10
                        epochsCount = 10
                        model.fit(X_train, y_train,
                                      batch_size=batchSize,
                                      epochs=epochsCount,
                                      validation_split=0.3,
                                      callbacks=[tensorboard],
                                      validation_data=(X_test, y_test))
                        
    tEnd = time.time()
    print('Research took %d seconds' % (tEnd - tBegin))


research()


#
# tensorboard --logdir=logs/ --host localhost --port 8080
#